from datetime import date
from ariadne import convert_camel_case_to_snake, convert_kwargs_to_snake_case
from ariadne import MutationType, make_executable_schema
from api_FLASK_GQL import db
from api_FLASK_GQL.models import Post
import time
from sqlalchemy import select, tuple_, or_, and_
from sqlalchemy.sql import bindparam
from sqlalchemy.sql.expression import literal


@convert_kwargs_to_snake_case
def create_mult_post_resolver(obj, info, posts):
    try:
        # Create a list of dictionaries containing the values for each row to be inserted
        today = date.today()
        rows = []
        for post in posts:
            rows.append({
                'title': post['title'],
                'description': post['description'],
                'created_at': today.strftime("%m-%d-%Y") # 'created_at': post.get('created_at', created_at=today.strftime("%m-%d-%Y"))
            })

        # all_rows = Post.query.all()
        stmt = select([Post.id, Post.title, Post.description])

        #unique listings
        stmt = select([Post.title, Post.description]).group_by(Post.title, Post.description)
        unique_posts = db.session.execute(stmt).fetchall()
        existing_tuples = [(item.title, item.description) for item in unique_posts]

        # new_rows = rows
        new_rows = [row for row in rows if (row['title'], row['description']) not in existing_tuples] #not in existing_tuples]

        print(" ++++ new_rows")
        print(new_rows)
        print("unique_posts")
        print(unique_posts)



        if new_rows != []:
            result = db.session.execute(Post.__table__.insert(), new_rows)
            db.session.flush()
            db.session.commit()

            time.sleep(4)

            ids = result.inserted_primary_key_rows
            # ids = [row[0] for row in result.inserted_primary_key_rows]
            print(ids)
            print(rows) #new_rows ??

            # Create a list of Post objects representing the newly created posts, setting the ids on the objects
            post_list = []
            for i, row in enumerate(rows):
                post_list.append(Post(id = ids[i], title=row['title'], description=row['description'], created_at=row['created_at']))


        payload = {
            "success": True,

            "posts" : new_rows #post_list
        }

    except ValueError as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload
#~~~~~~~~~~~~~~~


# @convert_camel_case_to_snake
@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description):
    try:
        today = date.today()
        post = Post(title=title, description=description, created_at=today.strftime("%m-%d-%Y"))

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

