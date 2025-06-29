from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from utils.Data_Visualizer import generate_graph

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017")
db = client['Segmentation_Dashboard']
users_collection = db['users']

app.config["UPLOAD_FOLDER"] = "datasets/"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'username' not in session:
        flash("Please log in to upload files.", "warning")
        return redirect(url_for('login'))
    if request.method == "POST":
        uploaded_file=request.files.get("csv_file")
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
            uploaded_file.save(file_path)

            db.uploaded_files.insert_one({
                "username": session.get("username"),
                "filename": filename,
                "filepath": file_path
            })
            return redirect(url_for('dashboard'))

    return render_template("upload.html")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    username = session['username']

    latest_file = db.uploaded_files.find_one(
        {"username": username},
        sort=[("_id", -1)]
    )

    if latest_file:
        filename = latest_file['filename']
        generate_graph(username, filename)
    else:
        filename = None

    return render_template('dashboard.html', username=username, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)