from flask import Blueprint, render_template,request, flash

auth =  Blueprint('auth',__name__)

@auth.route('signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        firstname = request.form.get('Firstname')
        lastname = request.form.get('Lastname')
        password1 = request.form.get('Password')
        password2 = request.form.get('Password2')

        if len(email) < 4:
            flash("Email must be greater than 4 charector", category='error')
        elif len(firstname) < 2 or len(lastname) < 2:
            flash("Name must be greater than 2 charector", category='error')
        elif password1 != password2:
            flash("Passwords dont match", category='error')
 
        elif len(password1) < 7:
            flash("Password must be greater than 7 charector", category='error')
        else:
            flash("Account created", category='success')
 

    return render_template("signup.html")

@auth.route('login', methods = ['GET','POST'])
def login():
    return render_template("login.html")
