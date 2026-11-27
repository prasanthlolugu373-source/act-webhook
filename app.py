import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN ="9292698408:AAFX4ezBffrqLg3TJpB1zlcQNkchZxV7jRg"
CHAT_ID = "8224846112"
VERIFY_TOKEN = "act_prasanth_verify"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                contacts = {c["wa_id"]: c.get("profile", {}).get("name", "Customer") for c in value.get("contacts", [])}
                for msg in value.get("messages", []):
                    sender = msg.get("from")
                    name = contacts.get(sender, "Customer")
                    text = msg.get("text", {}).get("body") or msg.get("button", {}).get("text") or "[Non-text message]"
                    alert = f"🔥 *New ACT Fibernet Lead!*\n\n👤 *Name:* {name}\n📞 *Number:* +{sender}\n💬 *Reply:* {text}"
                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={"chat_id": CHAT_ID, "text": alert}
                    )
    except Exception as e:
        print("Error:", e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
