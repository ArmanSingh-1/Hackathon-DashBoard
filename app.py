#--- Imports ---
# Flask and related modules
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Environment and OS modules
import os
from dotenv import load_dotenv

# Database and models
from models import db, User, UploadedFile, Feedback

# Data visualization utility function
from utils.Data_Visualizer import generate_graph

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# --- App Configuration ---
app.secret_key = os.environ.get('SECRET_KEY', 'mNF3RzqhKJpYtXbUcVsAo9Ww0fCGZx2n8eHdQ5MgaiLvT7DjYrBElsPO14NMkFquXcAyTZrb6j3h')
app.config["UPLOAD_FOLDER"] = "datasets/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with our Flask app
db.init_app(app)

# --- Routes ---
# Home route
@app.route("/")
def home():
    return render_template("home.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Handle form submission
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        # Basic validation
        if not username or not email or not password or not confirm_password:
            flash("Please fill out all fields.", "danger")
            return redirect(url_for("signup"))
        
        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        # Check if username or email already exists
        if db.session.query(User).filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for("signup"))

        # Create a new user
        hashed_password = generate_password_hash(password) # Hash the password using Werkzeug
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.password = hashed_password
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle form submission
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # fetch user from the database        
        user = User.query.filter_by(username=username).first()

        # Verify user and password
        if user and check_password_hash(user.password, password):
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("upload"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# Logout route
@app.route("/logout")
def logout():
    # Clear the session
    session.pop("username", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))


# Upload route
@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Ensure user is logged in
    if "username" not in session:
        flash("Please log in to upload files.", "warning")
        return redirect(url_for("login"))

    # Handle file upload
    if request.method == "POST":
        uploaded_file = request.files.get("csv_file")
        
        # Validate file type and presence
        if uploaded_file and uploaded_file.filename and uploaded_file.filename.endswith('.csv'):
            # Secure the filename and define the file path
            filename = secure_filename(uploaded_file.filename)
            # Create upload folder if it doesn't exist
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            # Ensure the upload directory exists
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            # Save the file to the specified path
            uploaded_file.save(file_path)

            # Save file info to the database
            new_file = UploadedFile()
            new_file.username = session["username"]
            new_file.filename = filename
            new_file.filepath = file_path
            db.session.add(new_file)
            db.session.commit()

            return redirect(url_for("dashboard"))
        else:
            flash("Please upload a valid CSV file.", "danger")
            return redirect(url_for("upload"))

    return render_template("upload.html")


# Dashboard route
@app.route("/dashboard")
def dashboard():
    # Ensure user is logged in
    if "username" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))

    # Fetch the latest uploaded file for the user
    username = session["username"]
    latest_file = UploadedFile.query.filter_by(username=username).order_by(UploadedFile.id.desc()).first()

    # Generate graph if a file exists
    if latest_file:
        filename = latest_file.filename
        generate_graph(username, filename)
    else:
        filename = None

    return render_template("dashboard.html", username=username, filename=filename)


# Feedback route
@app.route("/feedback", methods=["POST"])
def feedback():
    # Handle feedback submission
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        name = request.form.get("name")
        email = request.form.get("email")

        # Basic validation
        if not feedback_text:
            flash("Feedback cannot be empty.", "danger")
            return redirect(url_for("home"))
        
        # Create a new feedback entry
        new_feedback = Feedback()
        new_feedback.feedback_text = feedback_text
        new_feedback.name = name if name else "Anonymous"  # Provide a default if name is empty
        new_feedback.email = email if email else None  # Email can be optional
        db.session.add(new_feedback)
        db.session.commit()

        flash("Thank you for your feedback!", "success")
    return redirect(url_for("home"))

# Run the app
if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Run the Flask development server
    app.run(debug=True)