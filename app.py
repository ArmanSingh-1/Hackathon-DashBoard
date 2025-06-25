from flask import Flask, render_template
from utils.Data_Visualizer import generate_graph

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    generate_graph()
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
