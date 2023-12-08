from api_FLASK_GQL import db
from datetime import datetime

"""
SELECT * FROM posts; 
"""


class Post(db.Model):
    # The __tablename__ attribute is optional. If you don't set it,
    # SQLAlchemy will use a default table name that is the lowercase version
    # of the class name (in this case, 'post').
    __tablename__ = "posts"  # Explicitly naming the table 'posts'

    # The 'id' column is set as the primary key.
    # 'autoincrement=True' is the default behavior for integer primary keys.
    # 'nullable=False' ensures that this field can never be empty in the database.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    # The 'title' column is defined as a string with a maximum length of 100.
    # 'nullable=False' ensures that this field must be provided for the record to be saved.
    title = db.Column(db.String(100), nullable=False)

    # The 'description' column is defined as a string with a maximum length of 255.
    # 'nullable=False' ensures that this field must be provided for the record to be saved.
    description = db.Column(db.String(255), nullable=False)

    # The 'created_at' column is defined as a DateTime.
    # 'nullable=False' ensures that this field must be provided for the record to be saved.
    # 'default=datetime.utcnow' sets the default value of this column to the current UTC time.
    # It is important to use 'datetime.utcnow' and not 'datetime.utcnow()' because you want to
    # pass the actual function to SQLAlchemy, not the result of calling the function at module load time.
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Convert the SQLAlchemy object to a Python dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            # Formatting the datetime object to a string in the format of "mm-dd-yyyy".
            "created_at": self.created_at.strftime("%m-%d-%Y"),
        }


"""
# app is visible form init filewhich is kinda weird but of

# basically database models go here

from api_FLASK_GQL import db  # SHOULD WORK
from datetime import datetime

# from app import db

# from .__init__ import db

# from app import db

# from flask_sqlalchemy import SQLAlchemy


class Post(
    db.Model
):  # inherits from db.Model, and db in general, it inherits from sql alchemy class
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
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at.strftime("%m-%d-%Y")),
        }


#  we can have more classes and it would be like more tables

"""
