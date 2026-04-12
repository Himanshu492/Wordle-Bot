import os
import requests
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

# the url to set the webhook for the bot
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

# data we are sending to that url
data = {
    # the webvhook url where telegram will send the updates
    "url": WEBHOOK_URL,
    "secret_token": WEBHOOK_SECRET
}

response = requests.post(url, json=data)
result = response.json()