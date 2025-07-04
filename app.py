from flask import Flask, jsonify, request, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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
    app.run()
