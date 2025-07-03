from flask import Flask, send_file, jsonify
from analyzer import analyze_trends
from plotter import generate_plot
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "PTT 輿情趨勢分析系統啟動中"

@app.route("/analyze")
def analyze():
    df = analyze_trends()
    return df.to_json(orient="records", force_ascii=False)

@app.route("/plot")
def plot():
    success = generate_plot()
    if success:
        return send_file("static/trend_plot.png", mimetype="image/png")
    return jsonify({"error": "無資料"})

if __name__ == "__main__":
    app.run(debug=True)
