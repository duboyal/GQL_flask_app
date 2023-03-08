# app is visible form init filewhich is kinda weird but of 

# basically database models go here 

from api_FLASK_GQL import db #SHOULD WORK
from datetime import datetime

# from app import db

# from .__init__ import db

# from app import db

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app) # igues this is here and then  gets imported. but is that design?

class Post(db.Model): #inherits from db.Model, and db in general, it inherits from sql alchemy class 


    # __tablename__ = 'posts'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title = db.Column(db.String(100), nullable=False)
    # description = db.Column(db.String(255), nullable=False)
    # created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "created_at" : str(self.created_at.strftime('%m-%d-%Y'))

        }
    


#  we can have more classes and it would be like more tables
