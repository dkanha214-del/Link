import os
import telebot
import requests
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send any video link")

# Detect video type
def detect_video(url):

    if ".mp4" in url:
        return "mp4"

    if ".m3u8" in url:
        return "m3u8"

    return "unknown"

# Handle messages
@bot.message_handler(func=lambda m: True)
def handle_link(message):

    url = message.text

    video_type = detect_video(url)

    if video_type == "mp4":

        bot.reply_to(message,"Direct video detected")

        r = requests.get(url, stream=True)

        with open("video.mp4","wb") as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)

        bot.send_video(message.chat.id, open("video.mp4","rb"))

    elif video_type == "m3u8":

        bot.reply_to(message,"Streaming link detected")

        bot.send_message(
            message.chat.id,
            f"Streaming Link:\n{url}"
        )

    else:

        bot.reply_to(message,"Video not detected")

import threading

def run():
    bot.infinity_polling()

threading.Thread(target=run).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
