from flask import Flask, render_template
from Data_Visualizer import generate_graph

app = Flask(__name__)

@app.route('/')
def home():
    generate_graph()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
