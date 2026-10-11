from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# تنظیم کلید API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/ocr', methods=['POST'])
def ocr_process():
    try:
        # کد پردازش تصویر و اتصال به جمینای
        return jsonify({"status": "success", "message": "ارتباط برقرار شد"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

