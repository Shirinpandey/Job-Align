from app import db
from flask_login import UserMixin 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password1 = db.Column(db.String(150), nullable=False)
    password2 = db.Column(db.String(150), nullable=False)



