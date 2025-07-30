from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

# Gemini API key Setup
GEMINI_API_KEY = "AIzaSyCP7ykx5Hlf7uhhw3c-h1uz-x2q3M9yyr8"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# 🔹 Embedded Traya product knowledge 
TRAYA_KNOWLEDGE = """
Traya is a health and wellness brand offering personalized hair care solutions using Ayurveda, Dermatology, and Nutrition.

Key Products:
1. Hair Ras – A herbal supplement promoting hair growth.
2. Scalp Oil – Ayurvedic oil to reduce dandruff and improve scalp health.
3. Hair Food – A protein-based supplement to improve hair strength and reduce hair fall.
4. Defense Shampoo – A mild, sulfate-free shampoo designed to cleanse the scalp without damage.

Traya's approach treats the root cause of hair loss using a mix of diagnosis, diet, lifestyle, and curated product plans.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    # Inject product knowledge into prompt
    prompt = f"""
You are Traya's AI assistant. Respond based only on the context below.

Context:
{TRAYA_KNOWLEDGE}

User: {user_input}
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    response = requests.post(GEMINI_URL, json=payload, headers=headers)

    try:
        response_json = response.json()
        if "candidates" not in response_json:
            print("Gemini API Error:", response_json)
            return jsonify({"reply": "Sorry, something went wrong with the bot response."}), 500

        gemini_reply = response_json["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": gemini_reply})

    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({"reply": "Sorry, the bot had an internal error."}), 500

if __name__ == "__main__":
    app.run(debug=True)