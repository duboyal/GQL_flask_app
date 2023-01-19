
from api_FLASK_GQL import app, db
from api_FLASK_GQL import models
# from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from api_FLASK_GQL.models import Post

from flask import request, jsonify
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType

from ariadne.constants import PLAYGROUND_HTML




# --- resolvers in queries.py

from api_FLASK_GQL.queries import listPosts_resolver, getPost_resolver
from api_FLASK_GQL.mutations import create_post_resolver ,update_post_resolver , delete_post_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listPosts", listPosts_resolver)
query.set_field("getPost", getPost_resolver)


mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)
#-----


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
    data = request.get_json()
    # print("\n\n this \n")
    # print(type(data))

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    print("result")
    print(result)
    status_code = 200 if success else 400
    return jsonify(result),status_code
    # return jsonify(data),status_code






@app.route('/second')
def helloGraphQL2():
    return "yaaay2 ---------- my first gql"


#---------------------------
# db = SQLAlchemy(app) NO THATS IN INIT
#init also has 

# current_date = datetime.now() #today().date()
# new_post = Post(title = "Post1", description = "yayayay trying", created_at = current_date) # can prrob get rid of tjis line too, maybe was for testing 
# # # ---------------------------
# # # OK so this is actually editing the table 
# # # basically my only gap in understanding is why the init file cant see Posts from model

# # # can this go in init?? the entry point is here ... hmmm
# with app.app_context():
#     db.create_all()
#     db.session.add(new_post) #basically i can probably just get rid of this line 
#     db.session.commit()


# can this go in init?? the entry point is here ... hmmm
# current_date = datetime.now() #today().date()

current_date = datetime.today().date()
new_post = Post(title = "Post1", description = "TEST TEST TESTing", created_at = current_date) 
with app.app_context():
    db.create_all()
    db.session.add(new_post) #basically i can probably just get rid of this line 
    db.session.commit()