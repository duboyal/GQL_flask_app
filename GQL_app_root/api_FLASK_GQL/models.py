# app is visible form init filewhich is kinda weird but of 

# basically database models go here 

from api_FLASK_GQL import db #SHOULD WORK

# from app import db

# from .__init__ import db

# from app import db

# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app) # igues this is here and then  gets imported. but is that design?

class Post(db.Model): #inherits from db.Model, and db in general, it inherits from sql alchemy class 
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.Date)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "created_at" : str(self.created_at.strftime('%d-$m-%'))

        }

# I guess we can have more classes and it would be like more tables?