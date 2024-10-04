import requests
from datetime import datetime
from flask import jsonify
import re

from flask import Response
from ariadne.explorer import ExplorerPlayground

from flask import Flask
from flask_cors import CORS


# selly
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import (
    DesiredCapabilities,
)

from selenium.webdriver.chrome.options import Options


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
CORS(app)

# GraphQL schema setup
type_defs = load_schema_from_path(
    "api_FLASK_GQL/schema.graphql"
)  # backend/api_FLASK_GQL/schema.graphql
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


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Use ExplorerPlayground and pass an argument '_' as the schema or a context string
    playground_html = ExplorerPlayground().html("_")
    return Response(playground_html, mimetype="text/html")


@app.route("/scrape-craigslist", methods=["GET"])
def scrape_craigslist():
    # Scrape Craigslist and add the data to the database
    # one cool thing is that when we hit this get request its on the top
    # like top request is the most recent
    try:
        posts_list = return_posts()

        # TO REINTRODUCE THIS I NEED TO TEAR DOWN THE DATABASE
        # Everything below is going to need to
        # be changed and updated in to the schema
        # to have, tilte, description, url, datetime - 4 fields

        # COMMENTED OUT FOR NOW!
        # for post in posts_list:
        #     print("begining")

        #     print(post)
        #     print("items from post")
        #     print(post.items())
        #     new_post = Post(
        #         title=post["title"],
        #         description=post["description"],
        #         url=post["url"],
        #         created_at=datetime.now(),
        #     )
        #     print("-------0o0-------")
        #     print("hey")
        #     print(dir(new_post))
        #     db.session.add(new_post)
        #     # db.session.commit()
        # db.session.commit()

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

        soup = BeautifulSoup(response.text, "html.parser")
        posts_html = soup.find_all("a")  # , {"class": "result-title hdrlnk"})

        print("\n\n----- START ---")
        print("------z00z---posts_html")

        # ---------------------

        post_list = []
        for item in posts_html[2:11]:
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
