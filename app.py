from flask import Flask, render_template
from auth import auth
from job import job
from search import search 
from os import path
from extension import db, DB_NAME
from search import load_jobs_once
from flask_login import LoginManager, current_user
import openai, os

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
    app.config['ALLOWED_EXTENSIONS'] = ['.txt', '.pdf']
    app.config['UPLOAD_DIRECTORY'] = 'job'  # Ensure this folder exists
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(job, url_prefix='/job')
    app.register_blueprint(search, url_prefix='/search')

    # Route for home page
    @app.route('/')
    def index():
        return render_template('home.html', user = current_user)
    from models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    with app.app_context():
        load_jobs_once() 

    return app

def create_database(app):
    from models import User
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created.')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
