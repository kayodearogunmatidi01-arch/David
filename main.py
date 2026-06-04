import os
import telebot

# Fetch the token from Render's environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

bot = telebot.TeleBot(BOT_TOKEN)

# Your custom welcome message
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

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # This replies to the user who sent the command (works for anyone)
    bot.reply_to(message, WELCOME_MESSAGE)

if __name__ == "__main__":
    print("Bot is starting up...")
    # infinity_polling keeps the bot running and handles errors automatically
    bot.infinity_polling()
