from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_notification(message):
    if DISCORD_WEBHOOK_URL:
        payload = {"content": message}
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Bot di Trading attivo e in ascolto sui Webhook!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    action = data.get("action", "ALERT")
    ticker = data.get("ticker", "BTC/USDT")
    price = data.get("price", "N/A")

    msg = f"🚀 **SEGNALE WEBHOOK RICEVUTO!** 🚀\n**Azione:** {action}\n**Asset:** {ticker}\n**Prezzo:** ${price}"
    send_discord_notification(msg)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
