from email.policy import default
from sqlalchemy import desc, null
from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_code = db.Column(db.String(20), unique=True, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False)
    deletion_comment = db.Column(db.String(1000), nullable=False)

    def __init__(self, name, description, quantity, product_code):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.product_code = product_code
        self.deleted = False
        self.deletion_comment = "n/a"
