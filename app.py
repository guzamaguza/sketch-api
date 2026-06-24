
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    image = request.files["image"]

    return jsonify({
        "filename": image.filename,
        "message": "Image received"
    })