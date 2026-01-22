from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/TurkuNLP/gpt3-finnish-small"
HF_TOKEN = os.environ.get("HF_TOKEN")  # Lisää tämä Renderin ympäristömuuttujiin

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    try:
        result = response.json()
    except:
        return jsonify({"error": "Invalid response from HuggingFace"}), 500

    return jsonify(result)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

