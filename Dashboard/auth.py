from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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