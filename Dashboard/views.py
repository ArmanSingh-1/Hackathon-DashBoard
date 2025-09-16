import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from .models import db, UploadedFile, Feedback
from utils.Data_Visualizer import generate_graph

views = Blueprint('views', __name__)

# Home route
@views.route("/")
def home():
    return render_template("home.html")

# Upload route
@views.route("/upload", methods=["GET", "POST"])
def upload():
    # Ensure user is logged in
    if "username" not in session:
        flash("Please log in to upload files.", "warning")
        return redirect(url_for("auth.login"))

    # Handle file upload
    if request.method == "POST":
        uploaded_file = request.files.get("csv_file")
        
        # Validate file type and presence
        if uploaded_file and uploaded_file.filename and uploaded_file.filename.endswith('.csv'):
            # Secure the filename and define the file path
            filename = secure_filename(uploaded_file.filename)
            # Create upload folder if it doesn't exist
            file_path = os.path.join("datasets/", filename)
            # Ensure the upload directory exists
            os.makedirs("datasets/", exist_ok=True)
            # Save the file to the specified path
            uploaded_file.save(file_path)

            # Save file info to the database
            new_file = UploadedFile()
            new_file.username = session["username"]
            new_file.filename = filename
            new_file.filepath = file_path
            db.session.add(new_file)
            db.session.commit()

            return redirect(url_for("views.dashboard"))
        else:
            flash("Please upload a valid CSV file.", "danger")
            return redirect(url_for("views.upload"))

    return render_template("upload.html")

# Dashboard route
@views.route("/dashboard")
def dashboard():
    # Ensure user is logged in
    if "username" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("auth.login"))

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
@views.route("/feedback", methods=["POST"])
def feedback():
    # Handle feedback submission
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        name = request.form.get("name")
        email = request.form.get("email")

        # Basic validation
        if not feedback_text:
            flash("Feedback cannot be empty.", "danger")
            return redirect(url_for("views.home"))
        
        # Create a new feedback entry
        new_feedback = Feedback()
        new_feedback.feedback_text = feedback_text
        new_feedback.name = name if name else "Anonymous"  # Provide a default if name is empty
        new_feedback.email = email if email else None  # Email can be optional
        db.session.add(new_feedback)
        db.session.commit()

        flash("Thank you for your feedback!", "success")
    return redirect(url_for("views.home"))
