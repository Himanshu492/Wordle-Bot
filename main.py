from flask import Flask, request, jsonify
import requests
import os
from pymongo import MongoClient
import dotenv
from database_utils import delete_record, get_record, insert_record, update_record
from wordle_logic import get_next_guess, not_valid_result, update_game_state

dotenv.load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
MONGO_URI = os.environ.get('MONGO_URI')

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

client = MongoClient(MONGO_URI)
db = client["wordle"]
pending = db["pending"]
FIRST_GUESS = "slate"
MAX_GUESSES = 6

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "guesses.txt"), "r") as f:
    dictionary = [line.strip() for line in f.readlines()]


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


def update_game(chat_id, guess, space, found, tries):
    update_record({"chat_id": chat_id},
        {
            "guess": guess,
            "space": space,
            "found": found,
            "tries": tries
        },
        pending
    )


def load_gueses():
    return_dict = {}
    with open("guess_db.csv", 'r') as f:
        for line in f:
            result, guess = line.strip().split(",")
            return_dict[result] = guess
    return return_dict


guesses_dict = load_gueses()


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

    if not text:
        return jsonify({"ok": True})

    text = text.strip()
    
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
            "If I solve it, send <b>found</b> 🎉\n\n"
            "Enter /wordle to begin!"
        )

        send_message(chat_id, welcome_msg)
        return jsonify({"ok": True})

    if text == "/wordle":
        # Start the Wordle game
        game_msg = (
            "Let's start the Wordle game! 🕹️\n\n"
            "Guess the word <b>SLATE</b> first and send me the result! 🧩"
        )
        send_message(chat_id, game_msg)
        game = {
            "chat_id": chat_id,
            "space": ["abcdefghijklmnopqrstuvwxyz"] * 5,
            "found": "",
            "guess": FIRST_GUESS,
            "tries": 1
        }

        if get_record({"chat_id": chat_id}, pending):
            update_record({"chat_id": chat_id}, game, pending)
        else:
            insert_record(game, pending)

        return jsonify({"ok": True})
    
    game = get_record({"chat_id": chat_id}, pending)
    if game:
        result = text.upper()

        if not_valid_result(result):
            send_message(chat_id, "Please send a 5-letter result using only X, Y, and G. Example: <b>XXYXG</b>")
            return jsonify({"ok": True})

        if result == "FOUND":
            send_message(chat_id, f"The word was <b>{game['guess'].upper()}</b>! Found in {game['tries']} guesses!")
            delete_record({"chat_id": chat_id}, pending)
            return jsonify({"ok": True})

        if game["tries"] >= MAX_GUESSES:
            send_message(chat_id, "Word was not found :(")
            delete_record({"chat_id": chat_id}, pending)
            return jsonify({"ok": True})
        
        if game["tries"] == 1 and result in guesses_dict:
            guess = guesses_dict[result].lower()
            space, found = update_game_state(
                result=result,
                guess=game["guess"],
                space=game["space"],
                found=game["found"]
            )
            send_message(chat_id, f"Guess this word - <b>{guess.upper()}</b>")
            update_game(
                chat_id=chat_id,
                guess=guess,
                space=space,
                found=found,
                tries=game["tries"] + 1
            )
            return jsonify({"ok": True})

        guess, space, found = get_next_guess(
            result=result,
            guess=game["guess"],
            space=game["space"],
            found=game["found"],
            dictionary=dictionary
        )

        if not guess:
            send_message(chat_id, "No words left to guess.")
            delete_record({"chat_id": chat_id}, pending)
            return jsonify({"ok": True})
        
        game["guess"] = guess
        game["space"] = space
        game["found"] = found
        game["tries"] += 1
        update_game(
            chat_id=chat_id,
            guess=game["guess"],
            space=game["space"],
            found=game["found"],
            tries=game["tries"]
        )

        send_message(chat_id, f"Guess this word - <b>{guess.upper()}</b>")
        return jsonify({"ok": True})
        
    
    send_message(chat_id, "I don't understand 😅. Please use /start to begin the game.")
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
