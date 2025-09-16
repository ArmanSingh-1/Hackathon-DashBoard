import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)

    # --- App Configuration ---
    app.secret_key = os.environ.get('SECRET_KEY', 'mNF3RzqhKJpYtXbUcVsAo9Ww0fCGZx2n8eHdQ5MgaiLvT7DjYrBElsPO14NMkFquXcAyTZrb6j3h')
    app.config["UPLOAD_FOLDER"] = "datasets/"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app