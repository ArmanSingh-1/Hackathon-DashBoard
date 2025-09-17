from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

auth = Blueprint('auth', __name__)

# Signup route
@auth.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("auth.signup"))
        
        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.signup"))

        # Check if username or email already exists
        if db.session.query(User).filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.signup"))

        is_first = (User.query.count() == 0)

        # Create a new user
        hashed_password = generate_password_hash(password) # Hash the password using Werkzeug
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.password = hashed_password
        new_user.role = 'admin' if is_first else 'user'  # First user is admin
        db.session.add(new_user)
        db.session.commit()

        if is_first:
            flash("Admin account created successfully! Please log in.", "success")
        else:
            flash("Signup successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# Login route
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Handle form submission
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # fetch user from the database        
        user = User.query.filter_by(username=username).first()

        # Verify user and password
        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            session["role"] = user.role
            flash("Login successful.", "success")
            return redirect(url_for("views.upload"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# Logout route
@auth.route("/logout")
def logout():
    # Clear the session
    session.pop("username", None)
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))


# API endpoint for login
@auth.route("/api/login", methods=["POST"])
def api_login():
    # Handle JSON login request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # If login is successful, update the session
        session["username"] = user.username
        session["role"] = user.role
        return jsonify({"success": True, "redirect_url": url_for("views.upload")})
    else:
        # If login fails, return an error message
        return jsonify({"success": False, "message": "Invalid username or password."})
    

# API endpoint for signup
@auth.route("/api/signup", methods=["POST"])
def api_signup():
    # API endpoint for handling signup.
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # --- Server-side validation ---
    if not all([username, email, password, confirm_password]):
        return jsonify({"success": False, "message": "Please fill out all fields."})

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match."})

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"success": False, "message": "Username or email already exists."})

    # --- Create user if validation passes ---
    is_first = (User.query.count() == 0)

    # Create a new user
    hashed_password = generate_password_hash(password) # Hash the password using Werkzeug
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.password = hashed_password
    new_user.role = 'admin' if is_first else 'user'  # First user is admin
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "redirect_url": url_for("auth.login")})