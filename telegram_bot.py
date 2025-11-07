import os
import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# API Configuration
API_URL = 'https://kuchbhi-alpha.vercel.app/api/get-key'

# Telegram Bot Token (You need to set this as environment variable)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "🎉 Welcome to Key Generator Bot! 🎉\n\n"
        "Use /generate to get your key!\n\n"
        "⚠️ Remember: Keys expire in 10 minutes!"
    )
    await update.message.reply_text(welcome_message)

async def generate_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a key when the command /generate is issued."""
    # Send initial message
    message = await update.message.reply_text("🔄 Generating your key...")
    
    try:
        # Make API request
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        
        # Extract key from different possible response formats
        key = None
        
        if 'key' in data:
            key = data['key']
        elif 'failed_url' in data:
            # Extract key from failed_url
            match = re.search(r'key=([^&\s]+)', data['failed_url'])
            key = match.group(1) if match else None
        elif 'error' in data and 'key=' in data['error']:
            # Extract key from error message
            match = re.search(r'key=([A-Za-z0-9]+)', data['error'])
            key = match.group(1) if match else None
        
        if key:
            # Success! Send the key
            success_message = (
                f"✅ Your Key is Ready! 🎉\n\n"
                f"🔑 Key: `{key}`\n\n"
                f"⚠️ **Important:**\n"
                f"• Use this key within 10 minutes\n"
                f"• After that, it will expire and won't work\n\n"
                f"Tap to copy the key!"
            )
            await message.edit_text(success_message, parse_mode='Markdown')
        else:
            # Could not extract key
            await message.edit_text(
                "❌ Error generating key. Could not extract key from response.\n\n"
                "Please try again with /generate"
            )
    
    except requests.exceptions.RequestException as e:
        # Network or request error
        await message.edit_text(
            f"❌ Error generating key: Network error\n\n"
            f"Please try again with /generate"
        )
    except Exception as e:
        # Any other error
        await message.edit_text(
            f"❌ Error generating key: {str(e)}\n\n"
            f"Please try again with /generate"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "📖 **Bot Commands:**\n\n"
        "/start - Start the bot\n"
        "/generate - Generate a new key\n"
        "/help - Show this help message\n\n"
        "⚠️ **Important:**\n"
        "Keys expire in 10 minutes after generation!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_key))
    application.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
