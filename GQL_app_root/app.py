import requests
from datetime import datetime
from flask import jsonify

from flask import Response
from ariadne.explorer import ExplorerPlayground

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
        for post in posts_list:

            print("begining")

            print(post)
            print("items from post")
            print(post.items())
            new_post = Post(
                title=post["title"],
                description=post["description"],
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
        print("------0-0-0-0----")
        print("---------posts_html")
        print(posts_html)
        print("response.text")
        print(response.text)

        # basically here I could TRYYY to get the info out of "item" and stuff
        post_list = [
            {"title": clean(item.get_text()), "description": item.get("href")}
            for item in posts_html
        ]

        # MAYBE HERE
        # post_list = [{"item": item} for item in posts_html]

        return post_list
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def clean(text):
    # Helper function to clean text
    return text.replace("\n", "").replace("$0", "").replace(" ", "")


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
