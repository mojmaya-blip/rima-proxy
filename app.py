import os
from io import BytesIO

import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024  # 15 MB

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.get("/")
def health():
    return jsonify({"ok": True, "service": "rima-proxy-server"})

@app.post("/analyze")
def analyze_image():
    if not API_KEY:
        return jsonify({"error": "Server is missing GEMINI_API_KEY."}), 500
    uploaded = request.files.get("image")
    if uploaded is None or not uploaded.filename:
        return jsonify({"error": "Upload an image using the 'image' field."}), 400
    prompt = request.form.get("prompt", "Describe this image in Persian.").strip()
    if not prompt:
        prompt = "Describe this image in Persian."
    try:
        image_bytes = uploaded.read()
        image = Image.open(BytesIO(image_bytes))
        image.verify()
        image = Image.open(BytesIO(image_bytes))
        if image.format not in {"JPEG", "PNG", "WEBP", "GIF", "BMP"}:
            return jsonify({"error": "Unsupported image format."}), 400
        response = genai.GenerativeModel(MODEL_NAME).generate_content([prompt, image])
        return jsonify({"result": response.text})
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "The uploaded file is not a valid supported image."}), 400
    except Exception as exc:
        app.logger.exception("Gemini request failed")
        return jsonify({"error": "Gemini request failed.", "details": str(exc)}), 502

@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Image exceeds the 15 MB upload limit."}), 413

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
