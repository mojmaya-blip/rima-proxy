from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# مسیر اصلی برای تست سلامت سرور
@app.route('/', methods=['GET'])
def home():
    return "Server is running perfectly!"

# این همان مسیری است که خطای 501 می‌دهد؛ باید متد POST را قبول کند
@app.route('/api/ocr', methods=['POST', 'GET'])
def ocr_process():
    if request.method == 'POST':
        return jsonify({"status": "success", "message": "POST request received successfully"}), 200
    return jsonify({"status": "ready", "message": "Server is listening, please send POST request"}), 200

if __name__ == '__main__':
    app.run()
