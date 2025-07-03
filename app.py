from flask import Flask, send_file, jsonify
from analyzer import analyze_trends
from plotter import generate_plot
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    df = analyze_trends()
    return df.to_json(orient="records", force_ascii=False)


if __name__ == "__main__":
    app.run(debug=True)
