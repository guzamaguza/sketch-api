from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Sketch API is running"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "ok"})
