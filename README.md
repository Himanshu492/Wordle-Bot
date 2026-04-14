# Wordle Bot

🎮 A Telegram bot that helps solve Wordle one clue at a time.

Give the bot your Wordle result pattern, and it will suggest the next best 5-letter guess. It starts with **SLATE**, reads feedback like `XXYGX`, keeps track of the game in MongoDB, and tries to crack the word in 6 guesses or fewer.

## 🌈 What It Does

- 🧩 Runs as a Telegram bot using a Flask webhook.
- 🟩 Understands Wordle-style feedback:
  - `G` = green: correct letter, correct spot
  - `Y` = yellow: correct letter, wrong spot
  - `X` = gray: letter is not in the word
- 🚀 Uses `guess_db.csv` for fast second guesses after the first `SLATE` result.
- 🧠 Narrows the word list using `guesses.txt`.
- 💾 Stores active games and processed Telegram updates in MongoDB.
- 🕹️ Supports multiple chats by tracking each chat's game state.

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Telegram Bot API**
- **MongoDB**
- **PyMongo**
- **python-dotenv**
- **Gunicorn** for production-friendly serving

## 📁 Project Structure

```text
.
├── main.py              # Flask app and Telegram webhook handler
├── wordle_logic.py      # Word filtering and next-guess logic
├── database_utils.py    # MongoDB helper functions
├── set_webhook.py       # Registers the Telegram webhook
├── generate.py          # Optional script to regenerate first-guess lookup data
├── guesses.txt          # Word list used by the bot
├── guess_db.csv         # Precomputed best second guesses for SLATE feedback
└── requirements.txt     # Python dependencies
```

## 🚀 Getting Started

### 1. Clone the project

```bash
git clone https://github.com/Himanshu492/Wordle-Bot.git
cd Wordle-Bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_SECRET=your_webhook_secret
WEBHOOK_URL=https://your-domain.com/webhook
MONGO_URI=your_mongodb_connection_string
```

## 🤖 Telegram Bot Setup

1. Create a Telegram bot with [BotFather](https://t.me/BotFather).
2. Copy the bot token into `BOT_TOKEN`.
3. Deploy the Flask app somewhere with a public HTTPS URL.
4. Set `WEBHOOK_URL` to:

```env
WEBHOOK_URL=https://your-domain.com/webhook
```

5. Register the webhook:

```bash
python set_webhook.py
```

If everything goes well, Telegram will start sending updates to your `/webhook` route.

## 🧪 Run Locally

```bash
python main.py
```

The app runs on:

```text
http://0.0.0.0:8080
```

For Telegram webhooks, your local app must be exposed through HTTPS. Tools like ngrok or Cloudflare Tunnel can help while developing.

## 💬 How To Play

Start the bot in Telegram:

```text
/start
```

Begin a Wordle game:

```text
/wordle
```

The bot will ask you to guess:

```text
SLATE
```

After you enter that guess in Wordle, send the bot the result pattern:

```text
XXYXG
```

The bot will reply with the next word to guess.

When the bot gets it right, send:

```text
found
```

Then celebrate responsibly. Or irresponsibly. Wordle glory is serious business.

## 🧠 How The Guessing Works

The bot keeps a possible-letter space for each of the 5 word positions.

For every result:

- `X` removes that letter from possible positions.
- `Y` marks the letter as found but removes it from that exact position.
- `G` locks the letter into that position.

Then the bot builds possible words from `guesses.txt` and scores them by letter frequency. Words with useful, high-information letters get to the top.

For the first guess, `guess_db.csv` stores precomputed best responses for all `243` possible `X/Y/G` result combinations from `SLATE`.

## 🗃️ Regenerating `guess_db.csv`

The `generate.py` script rebuilds the lookup table for the first guess.

It uses `tqdm`, which is not part of the main runtime requirements. Install it first if needed:

```bash
pip install tqdm
```

Then run:

```bash
python generate.py
```

Heads up: this can take a few minutes, and it appends to `guess_db.csv`, so clear the file first if you want a clean regeneration.

## 🌐 Deployment Notes

A typical production command with Gunicorn:

```bash
gunicorn main:app
```

Make sure your deployment environment includes:

- `BOT_TOKEN`
- `WEBHOOK_SECRET`
- `WEBHOOK_URL`
- `MONGO_URI`

The `/` route returns a simple health message:

```text
Bot is running!
```

## 🧰 Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `BOT_TOKEN` | Yes | Telegram bot token from BotFather |
| `WEBHOOK_SECRET` | Yes | Secret token checked on incoming Telegram webhook requests |
| `WEBHOOK_URL` | Yes | Public HTTPS URL ending in `/webhook` |
| `MONGO_URI` | Yes | MongoDB connection string |

## 🧭 Roadmap Ideas

- Add a `/stop` command to abandon a game.
- Allow user to upload a screenshot of current game progress, and the bot will tell you your next guess.
- Make an agent that does the worlde on your browser.

## 🤝 Contributing

Fun project energy is welcome.

1. Fork the repo.
2. Create a feature branch.
3. Make your changes.
4. Test the bot logic.
5. Open a pull request.

## 👨‍💻 Author

Made with stubbornness with too many Wordle guesses by **Himanshu**.

- GitHub: [Himanshu492](https://github.com/Himanshu492)
- LinkedIn: [Himanshu Sharma](https://linkedin.com/in/your-profile)


---

Made so you can beat your friends in Wordle, and the joy of seeing five green squares. 🟩🟩🟩🟩🟩
