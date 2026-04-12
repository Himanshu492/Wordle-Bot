from flask import Flask, request, jsonify
import requests
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def telegram_post(method, data):
    url = f"{API_URL}/{method}"
    response = requests.post(url, json=data)
    return response.json()


def send_message(chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    response = telegram_post("sendMessage", data)
    return response


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != WEBHOOK_SECRET:
        return jsonify({"status": "forbidden"}), 403
    
    update = request.get_json(silent=True)
    if not update:
            return jsonify({"status": "bad request"}), 400

    message = update.get("message")
    if not message:
        return jsonify({"ok": True})
    
    chat = message.get("chat")
    chat_id = chat.get("id")
    text = message.get("text")

    if not chat_id:
         return jsonify({"ok": True})
    
    if text == "/start":
        welcome_msg = (
            "🎮 <b>Welcome to the Wordle Bot!</b>\n\n"
            "Send me the result of each guess, and I’ll try to solve the word in <b>under 6 tries</b>. 🧠\n\n"
            "<b>Format</b>\n"
            "Use a 5-letter string after each guess:\n\n"
            "🟩 <b>G</b> = Correct letter, correct spot\n"
            "🟨 <b>Y</b> = Correct letter, wrong spot\n"
            "⬛ <b>X</b> = Letter not in the word\n\n"
            "<b>Example</b>\n"
            "<code>XXYXG</code>\n\n"
            "If I solve it, send <code>found</code> 🎉\n\n"
            "Let’s begin."
        )

        send_message(chat_id, welcome_msg)
    else:
        send_message(chat_id, "Please use /start to begin the game.")

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)