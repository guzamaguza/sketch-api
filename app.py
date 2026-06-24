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

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
Analyze this mechanical sketch.

Return:
- Part type
- Number of holes
- Geometry description
- Estimated dimensions
- Notes
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ]
        )

        return f"<pre>{response.choices[0].message.content}</pre>"

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()