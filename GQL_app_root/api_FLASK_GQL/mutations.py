from datetime import date
from ariadne import convert_camel_case_to_snake, convert_kwargs_to_snake_case
from api_FLASK_GQL import db
from api_FLASK_GQL.models import Post

# @convert_camel_case_to_snake
@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description):
    try:
        today = date.today()
        post = Post(title=title, description=description, created_at=today.strftime("%d-%d-%Y"))

        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError as e:
        payload = {
            "success": False,
            "errors":["unable to add data in post"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id, title, description): #this one requires an id !
    try:
        # today = date.today()
        post = Post.query.get(id)
        if post:
            post.title = title
            post.description = description

        db.session.add(post)
        db.session.commit()

        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except AttributeError as e:
        payload = {
            "success": False,
            "errors":["item {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_post_resolver(obj, info, id): #this one requires an id !
    try:
        today = date.today()
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()


        payload = {
            "success": True,
            "post": post.to_dict() #"post {id} removed"
        }
    except AttributeError as e:
        payload = {
            "success": False,
            "errors":["doc {id} not found"]
        }
    return payload


# -------------------//----------------
# #maybe its too dangerous and i'd rather somehow 
# make a query that would maybe find each id in a range and pass if there are none ?

# @convert_kwargs_to_snake_case
# def delete_all_posts(obj, info):
#     try:
#         db.session.query(Post).delete()

#         post = {
#             "id" :"0", "title":"0", "description":"0", "created_at": "0"
#         }

#         db.session.add(post)
#         db.session.commit()

#         payload = {
#             "success": True,
#             "post": post #"post {id} removed"
#         }
#     except:
#         payload = {
#             "success": False,
#             "errorss": [" couldnt delete everythig"] #"post {id} removed"
#         }

