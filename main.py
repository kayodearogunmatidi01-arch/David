import os
import sys
import telebot

# Ensure log outputs stream instantly to Render's logging viewer
print("=== PRODUCTION BOT INITIALIZATION ===", flush=True)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("CRITICAL ERROR: 'BOT_TOKEN' environment variable is missing!", flush=True)
    sys.exit(1)

try:
    # Initialize the bot worker instance
    bot = telebot.TeleBot(BOT_TOKEN)
    bot_info = bot.get_me()
    print(f"Connection Secure! Running as: @{bot_info.username}", flush=True)
except Exception as e:
    print(f"CRITICAL ERROR: Authentication failed. Check your token value.\nDetails: {e}", flush=True)
    sys.exit(1)

# Exact text structure requested
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

# Rule 1: Handle explicit start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        print(f"User {message.from_user.id} triggered /start", flush=True)
        bot.reply_to(message, WELCOME_MESSAGE)
    except Exception as e:
        print(f"Messaging error: {e}", flush=True)

# Rule 2: Fallback safety net 
# If anyone interacts with the bot without a specific command setup yet,
# it forces the welcome menu to appear instead of ignoring them.
@bot.message_handler(func=lambda message: True)
def handle_all_other_messages(message):
    try:
        print(f"User {message.from_user.id} sent text: {message.text}. Sending welcome fallback.", flush=True)
        bot.reply_to(message, WELCOME_MESSAGE)
    except Exception as e:
        print(f"Fallback messaging error: {e}", flush=True)

if __name__ == "__main__":
    print("Bot engine is spinning up polling systems...", flush=True)
    # infinity_polling prevents infrastructure network blips from crashing the container
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
