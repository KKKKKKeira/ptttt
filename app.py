from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

@app.route("/data")
def data():
    date_filter = request.args.get("date")
    if not os.path.exists("data/trends.csv"):
        return jsonify([])
    df = pd.read_csv("data/trends.csv")
    if date_filter:
        df = df[df["timestamp"].str.startswith(date_filter)]
    return df.to_dict(orient="records")

@app.route("/")
def index():
    return "PTT 輿情系統 API"

if __name__ == "__main__":
    app.run()
