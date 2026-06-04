import os
import sys
import telebot

# Force logs to stream immediately to the Render Dashboard
print("=== STARTING THE BOT ENGINE ===", flush=True)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ CRITICAL ERROR: 'BOT_TOKEN' environment variable is not set in Render!", flush=True)
    sys.exit(1)

try:
    bot = telebot.TeleBot(BOT_TOKEN)
    
    # FIX: This clears out any conflicting webhook settings from past hostings
    print("Clearing any old active webhooks...", flush=True)
    bot.remove_webhook()
    
    bot_info = bot.get_me()
    print(f"✅ Bot Connected! Running as username: @{bot_info.username}", flush=True)
except Exception as e:
    print(f"❌ CRITICAL ERROR: Authentication failed. Is your token 100% correct?\nDetails: {e}", flush=True)
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

# Handle explicit start commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        print(f"📩 Received /start from user {message.from_user.id}", flush=True)
        bot.reply_to(message, WELCOME_MESSAGE)
        print("📤 Welcome message successfully dispatched.", flush=True)
    except Exception as e:
        print(f"❌ Messaging Error: {e}", flush=True)

# Catch-All Safety Net: If anyone sends anything else, force-reply with the menu
@bot.message_handler(func=lambda message: True)
def catch_all_messages(message):
    try:
        print(f"📩 Received message text from user {message.from_user.id}. Forcing welcome reply.", flush=True)
        bot.reply_to(message, WELCOME_MESSAGE)
    except Exception as e:
        print(f"❌ Catch-all Messaging Error: {e}", flush=True)

if __name__ == "__main__":
    print("🚀 Bot engine is long-polling... Send a message on Telegram!", flush=True)
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
