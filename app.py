from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import base64
import os

app = Flask(__name__)

# OpenAI client (uses Render environment variable: OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/")
def home():
    return """
    <h1>Sketch to CAD MVP</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Analyze Sketch</button>
    </form>
    """


@app.route("/test")
def test():
    return jsonify({"status": "ok"})


@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    image_bytes = image.read()

    # Convert image to base64 for GPT Vision
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
You are a mechanical design assistant.

Analyze this hand sketch and extract:

1. Part type (e.g., L-bracket, plate, housing)
2. Number of holes and their approximate layout
3. Key geometric features (faces, bends, symmetry)
4. Any visible dimensions
5. If unclear, explicitly say "assumption required"

Return results in a clean structured format like:

Part Type:
Features:
Holes:
Estimated Dimensions:
Notes:
"""
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_b64}"
                    }
                ]
            }]
        )

        return f"<pre>{response.output_text}</pre>"

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run()