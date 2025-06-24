# app.py
from flask import Flask, render_template, request, redirect
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.Transformer import Transformer_Map
from utils.Data_Visualizer import generate_graph

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "datasets"
app.config["ALLOWED_EXTENSIONS"] = {"csv"}

# Utility Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def normalize_columns(df):
    df.columns = [Transformer_Map.get(col.lower().strip(), col) for col in df.columns]
    return df

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(file_path)
            return redirect("/dashboard")
    return render_template("upload.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.endswith(".csv")]
    selected_file = files[0] if files else None

    if request.method == "POST":
        selected_file = request.form.get("selected_file", selected_file)

    if selected_file:
        df = pd.read_csv(os.path.join(app.config["UPLOAD_FOLDER"], selected_file))
        df = normalize_columns(df)
        table_html = df.head().to_html(classes='table table-bordered', index=False)
    else:
        table_html = "No CSV files found. Please upload one."

    # List all graph images
    graph_dir = "static/graphs"
    graph_images = [f for f in os.listdir(graph_dir) if f.endswith(".png")]

    return render_template("dashboard.html",
                           tables=[table_html],
                           files=files,
                           selected_file=selected_file,
                           graph_images=graph_images)

if __name__ == "__main__":
    app.run(debug=True)