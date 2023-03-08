
import os, sys

#'/Users/ali/Desktop/scraping/myenv1/lib/python3.7/site-packages'
sys.path.insert(0, '/Users/ali/Desktop/scraping/myenv1/lib/python3.7/site-packages') # cool so this fixed it, I think it was looking for another place in the python path first .....
# sys.path.insert(0, '/Users/ali/Desktop/scraping/myenv1/lib/python3.7')
selenium_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/ali/Desktop/scraping/myenv1/lib/python3.7/site-packages/selenium/__init__.py'))
sys.path.append(selenium_dir)
sys.path.append(".")
#'/Users/ali/Desktop/scraping/myenv1/lib/python3.7/site-packages'



from api_FLASK_GQL import app, db
from api_FLASK_GQL import models
import json, sys
# from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from api_FLASK_GQL.models import Post

from flask import request, jsonify
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType

from ariadne.constants import PLAYGROUND_HTML

import random
import time

from bs4 import BeautifulSoup
from time import sleep
## import chromedriver_binary 
from selenium import webdriver





# --- resolvers in queries.py

from api_FLASK_GQL.queries import listPosts_resolver, getPost_resolver
from api_FLASK_GQL.mutations import create_post_resolver ,update_post_resolver , delete_post_resolver ,create_mult_post_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listPosts", listPosts_resolver)
query.set_field("getPost", getPost_resolver)

mutation.set_field("createMultPost", create_mult_post_resolver)
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers) #must aadd query


# ----- basically we only have these two routes in GQL!!!

# GraphQL user interface
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

#haandle post queries
@app.route("/graphql", methods=["POST"])
def graphql_server():

    # when you get the request back for /graphql Post which is tied to a mutaation prrobably from make execultable schema and graphql_sync

    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    #currently the result from graphQLsync is messsed up
    print("result")
    print(result)
    status_code = 200 if success else 400
    return jsonify(result),status_code
    # return jsonify(data),status_code



@app.route('/second')
def helloGraphQL2():
    return "yaaay2 ---------- my first gql"


#------------------ this is either here ir in init, like if no database maade yet
# current_date = datetime.today().date()
# new_post = Post(title = "Post1", description = "TEST TEST TESTing", created_at = current_date) 
# with app.app_context():
#     db.create_all()
#     db.session.add(new_post) #basically i can probably just get rid of this line 
#     db.session.commit()
#------------driver code 

def return_posts():
    # --------------tried from cl_module--
    url = 'https://newyork.craigslist.org/search/act#search=1~list~0~38'
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(3)
    soup = BeautifulSoup(browser.page_source, 'html.parser') 
    # posts_html= soup.find_all('li', {'class': 'cl-search-result'})
    posts_html= soup.find_all('a', {'class': 'titlestring'})
    post_list = []
    for item in posts_html:
        # print(item)
        title = str(item).split('>')[-2].replace('</a','')
        description = str(item.get('href'))
        post_list.append({'title':title , 'description':description })
    return post_list



def return_query(posts_list):
    '''
    take in a list of title and descrription
    feed in list of craigslist post 
    and construct the query here
    '''

    str_1 = 'mutation { createMultPost(posts: ['
    for i in range(0,len(posts_list)):
        str0 = '{ title: " '+posts_list[i]["title"]+'", description: " '+posts_list[i]["description"]+'", created_at: "2022-03-02" },'
        str_1 += str0
    str_1 = str_1.strip(',')
    str_1 = str_1+"] ) {posts {title description created_at}}}" # for some reason id is returning null here - {posts {id title description created_at}}}

    return str_1



posts_list = return_posts()
query = return_query(posts_list)
post_data = {'query': query, 'variables': None}


with app.test_request_context('/graphql', method='POST', json=post_data):
    # this function call 
    response = app.view_functions['graphql_server']() 
    print(response)

# Access the response data
# response_data = response.get_json() # NO because the response data is a tuple
# status_code = response.status_code
print(" -999- ")
print(response)


