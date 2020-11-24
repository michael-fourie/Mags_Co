from qa327 import app
from flask_sqlalchemy import SQLAlchemy

"""
This file defines all models used by the server
These models provide us a object-oriented access
to the underlying database, so we don't need to 
write SQL queries such as 'select', 'update' etc.
"""


db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    """
    A user model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # added attributes:
    # do not include primary key because balance does not have to be unique
    balance = db.Column(db.Integer)

class Form(db.Model):
    """
    A form model which hold form information
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)  # owner of ticket
    name = db.Column(db.String(1000))               # name of ticket
    quantity = db.Column(db.Integer)                # quantity of this ticket
    price = db.Column(db.Integer)                   # price of ticket of this type
    date = db.Column(db.String(50))                 # expiration date

    instances =[]

    def __init__self(self):
        self.instances.append(self)

# Added:
class Ticket(db.Model):
    """
    A ticket model which holds information about a ticket
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)  # owner of ticket
    name = db.Column(db.String(1000))               # name of ticket
    quantity = db.Column(db.Integer)                # quantity of this ticket
    price = db.Column(db.Integer)                   # price of ticket of this type
    date = db.Column(db.String(50))                 # expiration date

    instances = []

    def __init__self(self):
        self.instances.append(self)  # allows this class to be in the form of an iterable
                                    # list of objects of type Ticket


# it creates all the SQL tables if they do not exist
with app.app_context():
    db.create_all()
    db.session.commit()
