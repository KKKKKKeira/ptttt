from flask import Flask, jsonify, render_template
from analyzer import analyze_trends
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    df = analyze_trends()
    return df.to_json(orient="records", force_ascii=False)

@app.route("/data")
def data():
    if not os.path.exists("data/trends.csv"):
        return jsonify([])
    df = pd.read_csv("data/trends.csv")
    return df.to_dict(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
