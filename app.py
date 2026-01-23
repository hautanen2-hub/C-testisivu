from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

@app.route("/api", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    r = requests.post(MODEL_URL, headers=headers, json=payload)

    try:
        return jsonify(r.json())
    except:
        return jsonify({"error": "HuggingFace returned non-JSON"}), 500

@app.route("/")
def home():
    return "API toimii!"
