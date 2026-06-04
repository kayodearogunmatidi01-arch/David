import os
import sys
import telebot

# Force flush print statements so they show up instantly in Render logs
print("Initializing bot script...", flush=True)

# Fetch the token from Render's environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("FATAL ERROR: The environment variable 'BOT_TOKEN' is missing!", flush=True)
    print("Please add 'BOT_TOKEN' in the Render Dashboard under Environment tab.", flush=True)
    sys.exit(1)

try:
    bot = telebot.TeleBot(BOT_TOKEN)
    # Test connection by fetching bot details
    bot_info = bot.get_me()
    print(f"Successfully connected to Telegram! Bot username: @{bot_info.username}", flush=True)
except Exception as e:
    print(f"FATAL ERROR: Failed to connect to Telegram. Is your token correct?\nError details: {e}", flush=True)
    sys.exit(1)

WELCOME_MESSAGE = """Hi! I'm your Multi-Utility Bot.

I can perform the following tasks:

 Images to PDF
   Send me images one by one, then use /done

 Text to Image
   Use /text2image <your text>

 Link to QR Code
   Use /qr <your link>

 Image to QR Code
   Use /img2qr (send an image with a QR code)

Use /cancel to abort any operation."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        print(f"Received /start command from user {message.from_user.id}", flush=True)
        bot.reply_to(message, WELCOME_MESSAGE)
        print("Welcome message sent successfully.", flush=True)
    except Exception as e:
        print(f"Error trying to send welcome message: {e}", flush=True)

if __name__ == "__main__":
    print("Bot is now listening for messages (Polling)...", flush=True)
    # non_stop=True and timeout=60 ensures it won't crash on network hiccups
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
