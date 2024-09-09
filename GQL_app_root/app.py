import requests
from datetime import datetime
from flask import jsonify
import re

from flask import Response
from ariadne.explorer import ExplorerPlayground


# selly
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import (
    DesiredCapabilities,
)

from selenium.webdriver.chrome.options import Options


# Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode to save resources
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu")  # Disable GPU to save resources
# chrome_options.add_argument(
#     "--remote-debugging-port=9222"
# )  # Required for headless Chrome


from bs4 import BeautifulSoup
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    ObjectType,
)
from ariadne.explorer import ExplorerApollo


# Import the create_app function and db object from the api_FLASK_GQL package
from api_FLASK_GQL import create_app, db
from api_FLASK_GQL.models import Post
from api_FLASK_GQL.queries import listPosts_resolver, getPost_resolver
from api_FLASK_GQL.mutations import (
    create_post_resolver,
    update_post_resolver,
    delete_post_resolver,
    create_mult_post_resolver,
)

# Create an instance of the Flask application
app = create_app()

# GraphQL schema setup
type_defs = load_schema_from_path("schema.graphql")
query = ObjectType("Query")
mutation = ObjectType("Mutation")

# Set resolvers for GraphQL queries and mutations
query.set_field("listPosts", listPosts_resolver)
query.set_field("getPost", getPost_resolver)

mutation.set_field("createMultPost", create_mult_post_resolver)
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

# Make the GraphQL schema executable
schema = make_executable_schema(type_defs, query, mutation)

# Connect to the Selenium server running in Docker
# Connect to the Selenium server running in Docker

# driver = webdriver.Remote(
#     command_executor="http://selenium:4444",  # Replace with your actual Selenium server URL
#     options=chrome_options,  # Use options instead of desired_capabilities
# )


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     # Return the GraphQL playground interface
#     return ExplorerApollo(title="Ariadne GraphQL")


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     # Create an instance of the ExplorerApollo and render it as HTML
#     explorer = ExplorerApollo(title="Ariadne GraphQL")
#     return Response(explorer.render(), mimetype="text/html")


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     # Return the Ariadne GraphQL playground
#     return ExplorerPlayground().render_response()


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     # Return the HTML for the Ariadne Explorer Playground directly
#     playground_html = ExplorerPlayground().html()
#     return Response(playground_html, mimetype="text/html")


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Use ExplorerPlayground and pass an argument '_' as the schema or a context string
    playground_html = ExplorerPlayground().html("_")
    return Response(playground_html, mimetype="text/html")


# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#     # Execute GraphQL queries
#     data = request.get_json()
#     success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
#     status_code = 200 if success else 400
#     return jsonify(result), status_code


@app.route("/scrape-craigslist", methods=["GET"])
def scrape_craigslist():
    # Scrape Craigslist and add the data to the database
    # one cool thing is that when we hit this get request its on the top
    # like top request is the most recent
    try:
        posts_list = return_posts()

        # Everything below is going to need to
        # be changed and updated in to the schema
        # to have, tilte, description, url, datetime - 4 fields

        for post in posts_list:
            print("begining")

            print(post)
            print("items from post")
            print(post.items())
            new_post = Post(
                title=post["title"],
                description=post["description"],
                url=post["url"],
                created_at=datetime.now(),
            )
            print("-------0o0-------")
            print("hey")
            print(dir(new_post))
            db.session.add(new_post)
            # db.session.commit()
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Posts added to database",
                    "posts_list": posts_list,
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


def return_posts():
    # Function to scrape Craigslist
    try:
        url = "https://newyork.craigslist.org/search/act"
        response = requests.get(url)
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        posts_html = soup.find_all("a")  # , {"class": "result-title hdrlnk"})

        print("\n\n----- START ---")
        print("------z00z---posts_html")

        # ---------------------
        #  RDY
        post_list = []
        for item in posts_html[2:7]:
            # Extract title and description
            title = clean(item.get_text())
            url1 = item.get("href")

            body = item.find("body")
            # print(dir*)

            response = requests.get(url1)
            soup2 = BeautifulSoup(response.text, "html.parser")

            date_paragraphs = soup2.find_all("p", id="display-date")

            #######################################
            posting_body = soup2.find("section", id="postingbody")
            # Extract the text content of the section
            if posting_body:
                text_content = str(posting_body.get_text(separator=" ", strip=True))
                text_content = text_content.replace("QR Code Link to This Post", "")
                print
            else:
                text_content = None
                print("No posting body found.")
            #######################################

            # date_paragraphs_time = str(soup2.find_all("p", id="display-date").find("time"))
            date_paragraph = date_paragraphs[0]

            time_tag = date_paragraph.find("time")
            datetime_value = (
                time_tag.get("datetime")
                if time_tag and time_tag.has_attr("datetime")
                else None
            )

            post_list.append(
                {
                    "title": title,
                    "url": str(url1),
                    "description": text_content,
                    "created_at": datetime_value,
                }
            )
        return post_list

    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def clean(text):
    # Helper function to clean text
    ret_str = text.replace("\n", "").replace("$0", "")  # .replace(" ", "_")
    raw_str = re.sub(r" {3,}", " | ", ret_str)
    title = raw_str.split("|")[0].strip()
    loc = raw_str.split("|")[1].strip()
    ret_str = f"{title} ({loc})"
    return ret_str


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=8000)


# import requests
# from datetime import datetime
# from flask import Flask, request, jsonify
# from bs4 import BeautifulSoup
# from flask_sqlalchemy import SQLAlchemy
# from ariadne import (
#     load_schema_from_path,
#     make_executable_schema,
#     graphql_sync,
#     ObjectType,
# )
# from ariadne.explorer import ExplorerApollo
# from api_FLASK_GQL
# from api_FLASK_GQL.models import Post  # Update import based on your project structure
# from api_FLASK_GQL.queries import listPosts_resolver, getPost_resolver
# from api_FLASK_GQL.mutations import (
#     create_post_resolver,
#     update_post_resolver,
#     delete_post_resolver,
#     create_mult_post_resolver,
# )

# # Initialize Flask app
# app = Flask(__name__)
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "your_database_uri"  # Replace with your actual URI
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# # GraphQL schema setup
# type_defs = load_schema_from_path("schema.graphql")
# query = ObjectType("Query")
# mutation = ObjectType("Mutation")

# query.set_field("listPosts", listPosts_resolver)
# query.set_field("getPost", getPost_resolver)

# mutation.set_field("createMultPost", create_mult_post_resolver)
# mutation.set_field("createPost", create_post_resolver)
# mutation.set_field("updatePost", update_post_resolver)
# mutation.set_field("deletePost", delete_post_resolver)

# schema = make_executable_schema(type_defs, query, mutation)


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     return ExplorerApollo(title="Ariadne GraphQL")


# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#     data = request.get_json()
#     success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
#     status_code = 200 if success else 400
#     return jsonify(result), status_code


# @app.route("/scrape-craigslist", methods=["GET"])
# def scrape_craigslist():
#     try:
#         posts_list = return_posts()
#         for post in posts_list:
#             new_post = Post(
#                 title=post["title"],
#                 description=post["description"],
#                 created_at=datetime.now(),
#             )
#             db.session.add(new_post)
#         db.session.commit()
#         return (
#             jsonify(
#                 {
#                     "success": True,
#                     "message": "Posts added to database",
#                     "posts_list": posts_list,
#                 }
#             ),
#             200,
#         )
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500


# # Scraping function
# def return_posts():
#     try:
#         url = "https://newyork.craigslist.org/search/act"
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         posts_html = soup.find_all("a")
#         post_list = [
#             {"title": clean(item.get_text()), "description": item.get("href")}
#             for item in posts_html
#         ]
#         return post_list
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return []


# def clean(text):
#     return text.replace("\n", "").replace("$0", "").replace(" ", "")


# # Main execution
# if __name__ == "__main__":
#     db.create_all()  # Create database tables if they don't exist
#     app.run(debug=True, host="0.0.0.0", port=8000)

"""
import os
import sys
import json
import time
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from api_FLASK_GQL import app, db, models
from api_FLASK_GQL.models import Post
from api_FLASK_GQL.queries import listPosts_resolver, getPost_resolver
from api_FLASK_GQL.mutations import (
    create_post_resolver,
    update_post_resolver,
    delete_post_resolver,
    create_mult_post_resolver,
)
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    graphql_sync,
    snake_case_fallback_resolvers,
    ObjectType,
)
from ariadne.explorer import ExplorerPlayground

from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# from ariadne.constants import PLAYGROUND_HTML
# from ariadne import graphql_playground

# Initialize Flask app
app = Flask(__name__)

# GraphQL schema setup
type_defs = load_schema_from_path("schema.graphql")
query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listPosts", listPosts_resolver)
query.set_field("getPost", getPost_resolver)

mutation.set_field("createMultPost", create_mult_post_resolver)
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)
from flask import Response

from ariadne.explorer import ExplorerApollo


# @app.route("/graphql", methods=["GET"])
# def playground():
#     return graphql_playground()


# got to figure out this playground
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # return "Test"

    return ExplorerApollo(title="Ariadne GraphQL")  # schema=schema)


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     # Generate HTML for the playground
#     playground_html = ExplorerPlayground().render()
#     # Create a response object with the HTML content
#     return Response(playground_html, mimetype="text/html")


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    print("result", result)
    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route("/second")
def helloGraphQL2():
    return "yaaay2 ---------- my first gql"


# Scraping function
def return_posts():
    try:
        print("-------am i here")
        url = "https://newyork.craigslist.org/search/act"
        response = requests.get(url)
        print("\n--------response")
        print(response.text)
        print("\n-------- end here --------\n")
        soup = BeautifulSoup(response.text, "html.parser")
        # posts_html = soup.find_all("a", {"class": "result-title hdrlnk"})
        posts_html = soup.find_all("a")  # , {"class": "result-title hdrlnk"})

        print("====hey yo yo====")
        print(type(posts_html))
        print(dir(posts_html))
        # print(posts_html.count())
        # print("***** DIR *****")
        # print(dir(soup))

        def clean(str):
            return str.replace("\n", "").replace("$0", "").replace(" ", "")

        post_list = [
            {"title": clean(item.get_text()), "description": item.get("href")}
            # item.get_text()
            for item in posts_html
        ]

        # print("\n\n+++post_list\n\n")
        # for item in post_list:
        #     print(item["title"] + "\n------------------\n")

        return post_list

    except Exception as e:
        print(f"Error occurred: {e}")
        return []


@app.route("/scrape-craigslist", methods=["GET"])
def scrape_craigslist():
    try:
        # Scrape Craigslist
        posts_list = return_posts()

        print("-----0000000000000000-----")
        # print(posts_list)

        # Add each post to the database
        for post in posts_list:
            print(post)
            new_post = Post(
                title=post["title"],
                description=post["description"],
                created_at=datetime.now(),
            )
            db.session.add(new_post)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Posts added to database",
                    "posts_list": posts_list,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Main execution...
if __name__ == "__main__":
    # app.run(debug=True)  # You can add 'debug=True' for development purposes
    # app = GraphQL(schema, debug=True)
    app.run(debug=True, host="0.0.0.0", port=8000)


## Helper function to construct query
# def return_query(posts_list):
#     query_str = "mutation { createMultPost(posts: ["
#     for post in posts_list:
#         post_str = f'{{ title: "{post["title"]}", description: "{post["description"]}", created_at: "2022-03-02" }},'
#         query_str += post_str
#     query_str = query_str.rstrip(",") + "] ) {posts {title description created_at}}}"
#     return query_str


# # Main execution
# if __name__ == "__main__":
#     posts_list = return_posts()
#     query = return_query(posts_list)
#     post_data = {"query": query, "variables": None}

#     with app.test_request_context("/graphql", method="POST", json=post_data):
#         response = app.view_functions["graphql_server"]()
#         print("Response:", response)

"""
