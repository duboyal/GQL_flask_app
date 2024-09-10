from .models import Post
import json
from ariadne import convert_kwargs_to_snake_case

def listPosts_resolver(obj, info):
    
    try:
        posts = [post.to_dict() for post in Post.query.all()]
        # posts = Post.query.all()

        print(posts)
        #prepare payload
        payload = { 
            "success":True,
            "errors": ["False"], #before was False
            "posts": posts #json.dumps(posts)
            }
        print("\nheyyy\n\n")
        print(payload)
        return payload

    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
        return payload

#ca,mel case to sanke case

@convert_kwargs_to_snake_case #all incoming queries from camel to snake
def getPost_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        payload = {
            "success":True,
            "post": post.to_dict() #single post thing
        }

    except Exception as error:
        payload = {
            "success":False,
            "errors":["post item {id} not found"]
        }
        return payload