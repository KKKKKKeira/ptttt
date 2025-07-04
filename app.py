from flask import Flask, jsonify, render_template, request
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
    date_filter = request.args.get("date")
    if not os.path.exists("data/trends.csv"):
        return jsonify([])
    df = pd.read_csv("data/trends.csv")
    if date_filter:
        df = df[df["timestamp"].str.startswith(date_filter)]
    return df.to_dict(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
