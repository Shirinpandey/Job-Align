from flask import Blueprint

auth =  Blueprint('auth',__name__)

@auth.route('signup')
def signup():
    return '<p>HELLO</p>'

@auth.route('login')
def login():
    return '<p>HELLO Login</p>'
