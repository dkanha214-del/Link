import os
import telebot
import yt_dlp
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send video download or streaming link")

# Extract real video URL using yt-dlp
def get_video_url(page_url):
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "format": "best",
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(page_url, download=False)

        # if formats exist choose best
        if "url" in info:
            return info["url"]

        if "formats" in info:
            return info["formats"][-1]["url"]

    return None


@bot.message_handler(func=lambda m: True)
def handle_link(message):

    url = message.text.strip()

    bot.reply_to(message, "Processing link...")

    try:
        video_url = get_video_url(url)

        if video_url:
            bot.send_video(message.chat.id, video_url)
        else:
            bot.reply_to(message, "Video not found")

    except Exception as e:
        bot.reply_to(message, "Error extracting video")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
