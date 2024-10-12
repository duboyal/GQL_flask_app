from flask import Flask, jsonify
import boto3
import datetime
import request

# Initialize DynamoDB connection
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")


def create_app():
    app = Flask(__name__)

    # Define your DynamoDB table (ensure the table already exists in your AWS account)
    table = dynamodb.Table("CL_DynamoDBTable")

    @app.route("/save-posts", methods=["POST"])
    def save_posts():
        # Example of saving posts to DynamoDB
        posts_list = request.json.get("posts_list", [])

        for post in posts_list:
            # Check if the post already exists in DynamoDB using its unique key (url)
            response = table.get_item(
                Key={
                    "url": post[
                        "url"
                    ]  # Assuming 'url' is the partition key in DynamoDB
                }
            )

            if "Item" not in response:
                # Post doesn't exist, save it to DynamoDB
                table.put_item(
                    Item={
                        "url": post["url"],  # Unique key (Partition Key)
                        "title": post["title"],
                        "description": post["description"],
                        "created_at": post["created_at"]
                        or datetime.utcnow().isoformat(),
                    }
                )
        return jsonify({"message": "Posts added to DynamoDB"}), 200

    return app


# BELOW IS IF YOU WANNA SET UP RDS
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


# def create_app():
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_DATABASE_URI"] = (
#         "postgresql://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"
#     )
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     db.init_app(app)

#     with app.app_context():
#         db.create_all()

#     return app


"""
from flask import Flask
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"
with app.app_context():
     db.create_all()
"""
