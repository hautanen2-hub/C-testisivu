from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")

# UUSI OIKEA OSOITE
MODEL_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

@app.route("/", methods=["GET"])
def home():
    return "API toimii! Lähetä POST /api"

@app.route("/api", methods=["POST"])
def generate():
    data = request.get_json(silent=True)
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' in JSON"}), 400

    prompt = data["prompt"]

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
    except Exception as e:
        return jsonify({"error": "Request to HuggingFace failed", "details": str(e)}), 500

    try:
        return jsonify(response.json())
    except Exception:
        return jsonify({
            "error": "HuggingFace returned non-JSON",
            "raw": response.text
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
