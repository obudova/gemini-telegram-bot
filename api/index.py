import os
import requests
from flask import Flask, request
from google import genai

app = Flask(__name__)

# Retrieve environment variables stored in Vercel
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Initialize Gemini Client
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Process only text messages
    if data and "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        
        try:
            # Query Gemini
            response = gemini_client.models.generate_content(
                model="gemini-3.7-flash",
                contents=user_text,
            )
            reply_text = response.text
        except Exception:
            reply_text = "Sorry, I ran into an error generating a response."

        # Send response back to Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply_text})
        
    return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "Gemini Telegram Bot is active!"