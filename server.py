from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

HF_API_URL = "https://router.huggingface.co/models/gpt2"
HF_TOKEN = os.environ.get("HF_TOKEN")

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
        return jsonify({"error": "HuggingFace returned non-JSON"}), 500

    if isinstance(result, list):
        return jsonify({"response": result[0].get("generated_text", "")})

    if isinstance(result, dict):
        return jsonify(result)

    return jsonify({"error": "Unexpected response format"}), 500


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
