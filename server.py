from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Ladataan suomenkielinen malli
malli = "TurkuNLP/gpt3-finnish-small"
generaattori = pipeline("text-generation", model=malli, tokenizer=malli)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")

    vastaus = generaattori(
        prompt,
        max_length=80,
        num_return_sequences=1,
        do_sample=True,
        top_p=0.95,
        temperature=0.8,
    )

    return jsonify({"response": vastaus[0]["generated_text"]})

@app.route("/")
def home():
    return "Tekoälypalvelin toimii!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
