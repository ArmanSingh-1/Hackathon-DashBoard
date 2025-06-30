from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from utils.Data_Visualizer import generate_graph

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["UPLOAD_FOLDER"] = "datasets/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///segmentation_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(300), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("upload"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out.", "info")
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        flash("Please log in to upload files.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        uploaded_file = request.files.get("csv_file")
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            uploaded_file.save(file_path)

            new_file = UploadedFile(username=session["username"], filename=filename, filepath=file_path)
            db.session.add(new_file)
            db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("upload.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))

    username = session["username"]
    latest_file = UploadedFile.query.filter_by(username=username).order_by(UploadedFile.id.desc()).first()

    if latest_file:
        filename = latest_file.filename
        generate_graph(username, filename)
    else:
        filename = None

    return render_template("dashboard.html", username=username, filename=filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if not exist
    app.run(debug=True)
