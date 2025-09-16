# utilizing Flask-SQLAlchemy for database models
from flask_sqlalchemy import SQLAlchemy
import datetime

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# User model for login/signup
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Model for uploaded files
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

# Model for feedback submissions
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True) # Optional
    email = db.Column(db.String(120), nullable=True) # Optional
    feedback_text = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))