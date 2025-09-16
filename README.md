# 📊 Customer Insights Dashboard

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A data visualization dashboard built using **Flask**, **Pandas**, **Matplotlib**, and **Seaborn**. It analyzes and visualizes customer purchasing behavior from a CSV dataset and displays key insights via a clean and simple web interface.

🔗 GitHub Repository: [Hackathon-DashBoard](https://github.com/ArmanSingh-1/Hackathon-DashBoard)

---

## 🚀 Features

- 🔍 Scatter plot: Income vs Purchase Amount (colored by Loyalty Score)
- 🔄 Scatter plot: Loyalty Score vs Purchase Frequency (colored by Region)
- 🧾 Bar plot: Region-wise Average Purchase by Age Group
- 🧠 Data preprocessing using Pandas
- 🌐 Frontend rendered using Flask + Jinja2
- 📂 All charts auto-generated and served from `/static`

---

## ⚙️ How to Run Locally

1. **Clone the repository**:

```bash
git clone https://github.com/ArmanSingh-1/Hackathon-DashBoard.git
cd Hackathon-DashBoard
```

2. **Create a virtual environment and activate it**:

```bash

python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
```

2. **Install required packages**:

```bash
pip install -r requirements.txt
```

3. **Run the Flask application**:

```bash
python app.py
```

4. **Visit your local server**:

```
http://127.0.0.1:5000/
```

---

## 📸 Dashboard Snapshots


- `static/income_vs_purchase.png`
- `static/loyalty_score_vs_purchase_frequency.png`
- `static/region_avg_spending.png`

---

## 📌 Technologies Used

- Flask (Python web framework)
- Pandas (data analysis)
- Matplotlib & Seaborn (visualization)
- Jinja2 (HTML templating)
- HTML/CSS

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---
