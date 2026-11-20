from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
from src.analytics import analyze_dataset, load_dataset, generate_demo_data

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
app.config["UPLOAD_FOLDER"] = "data/uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"csv"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs("data", exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    path = "data/demo_business_data.csv"
    if not os.path.exists(path):
        generate_demo_data(path)
    df = load_dataset(path)
    result = analyze_dataset(df)
    return render_template("index.html", result=result, filename="Demo business dataset", rows=len(df))

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        flash("Choose a CSV file before submitting.", "error")
        return redirect(url_for("index"))
    file = request.files["file"]
    if not file.filename:
        flash("No file selected.", "error")
        return redirect(url_for("index"))
    if not allowed_file(file.filename):
        flash("Please upload a .csv file.", "error")
        return redirect(url_for("index"))
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    try:
        df = load_dataset(path)
        result = analyze_dataset(df)
        return render_template("index.html", result=result, filename=filename, rows=len(df))
    except Exception as exc:
        flash(f"Could not analyze this file: {exc}", "error")
        return redirect(url_for("index"))

@app.route("/download-demo")
def download_demo():
    path = "data/demo_business_data.csv"
    if not os.path.exists(path):
        generate_demo_data(path)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    pass
