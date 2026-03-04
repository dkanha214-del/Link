import os
import telebot
import requests
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send video download or streaming link")

@bot.message_handler(func=lambda m: True)
def download_video(message):

    url = message.text

    try:
        bot.reply_to(message, "Downloading video...")

        r = requests.get(url, stream=True)

        filename = "video.mp4"

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)

        bot.send_video(message.chat.id, open(filename, "rb"))

    except:
        bot.reply_to(message, "Invalid link")

import threading

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
