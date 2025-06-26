from flask import Blueprint, render_template,request, flash, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from extension import db 
from flask_login import login_user,login_required, logout_user, current_user

auth =  Blueprint('auth',__name__)

@auth.route('signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('Email')
        firstname = request.form.get('Firstname')
        lastname = request.form.get('Lastname')
        password1 = request.form.get('Password')
        password2 = request.form.get('Password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already signed in', category= 'error')
        elif len(email) < 4:
            flash("Email must be greater than 4 charector", category='error')
        elif len(firstname) < 2 or len(lastname) < 2:
            flash("Name must be greater than 2 charector", category='error')
        elif password1 != password2:
            flash("Passwords dont match", category='error')
 
        elif len(password1) < 7:
            flash("Password must be greater than 7 charector", category='error')
        else:
            new_user = User(email = email , firstname = firstname, lastname = lastname, password_hash = generate_password_hash(password1, method = 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            

            flash("Account created", category='success')
            return redirect(url_for('index'))  
        
    return render_template("signup.html", user = current_user)

@auth.route('login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user, remember=True)
                flash('Logged in succesfully', category='success')
                return redirect(url_for('index')) 
            else:
                flash('Password isnt correct',category='error')
        else:
            flash('Email dont match',category='error')

    return render_template("login.html", user = current_user)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')  
    return redirect(url_for('auth.login'))
