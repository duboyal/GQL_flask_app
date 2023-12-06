# this file will hold all the api relation configuration files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from .models import Post ----> this cause huge circular error

from flask import redirect
from datetime import datetime

# from ariadne.constants import PLAYGROUND_HTML

# from models import Post. # NO idea why this doesnt work


app = Flask(__name__)  # basically boiler plate our instance of flask

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"

app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)  # igues this is here and then  gets imported. but is that design?


# -----------
# can this go in init?? the entry point is here ... hmmm
# current_date = datetime.now() #today().date()
# new_post = Post(title = "Post1", description = "yayayay trying", created_at = current_date)
# with app.app_context():
#     db.create_all()
#     db.session.add(new_post) #basically i can probably just get rid of this line
#     db.session.commit()
# # -----------


# create a simple route
@app.route("/")
def helloGraphQL():
    # return "yaaay ---------- my first gql"
    return PLAYGROUND_HTML, 200


"""
from flask import Flask
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://facpyhlx:HbI0qMR5DTPgmWMP4s5cvhj9H0Im0g_H@baasu.db.elephantsql.com/facpyhlx"
with app.app_context():
     db.create_all()
"""
