from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID")

def get_token():
    url = "https://connect.spotware.com/apps/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get("accessToken")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    action = data.get("action")
    symbol = data.get("ticker", "AUDUSD")
    quantity = data.get("quantity", 3000)

    token = get_token()

    order_type = "BUY" if action == "buy" else "SELL"

    url = f"https://connect.spotware.com/apps/trading/accounts/{ACCOUNT_ID}/orders"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "symbolName": symbol,
        "orderType": "MARKET",
        "tradeSide": order_type,
        "volume": quantity
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

@app.route("/")
def home():
    return "Webhook server is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

Tell me when you've pasted that in and I'll walk you through saving the file.Sonnet 4.6
