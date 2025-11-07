from flask import Flask, request, jsonify
import os
import re
import requests
import time
from collections import defaultdict

app = Flask(__name__)

# Configuration
API_URL = 'https://kuchbhi-alpha.vercel.app/api/get-key'
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # Your Vercel deployment URL

# Rate limiting
user_last_request = defaultdict(float)
RATE_LIMIT_SECONDS = 30

def send_message(chat_id, text, parse_mode=None):
    """Send message via Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    if parse_mode:
        data['parse_mode'] = parse_mode
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def handle_start(chat_id, user_name):
    """Handle /start command"""
    welcome_message = (
        f"🎉 Welcome to Key Generator Bot! 🎉\n\n"
        f"Use /generate or /key to get your key!\n\n"
        f"⚠️ Remember: Keys expire in 10 minutes!"
    )
    send_message(chat_id, welcome_message)

def handle_help(chat_id):
    """Handle /help command"""
    help_text = (
        "📖 **Bot Commands:**\n\n"
        "/start - Start the bot\n"
        "/generate - Generate a new key\n"
        "/key - Get a key (alias for /generate)\n"
        "/help - Show this help message\n\n"
        "⚠️ **Important:**\n"
        "Keys expire in 10 minutes after generation!"
    )
    send_message(chat_id, help_text, parse_mode='Markdown')

def handle_key_generation(chat_id, user_id):
    """Handle /key and /generate commands with rate limiting"""
    current_time = time.time()
    
    # Check rate limiting
    last_request_time = user_last_request[user_id]
    time_diff = current_time - last_request_time
    
    if time_diff < RATE_LIMIT_SECONDS:
        wait_time = int(RATE_LIMIT_SECONDS - time_diff)
        message = (
            f"⏱️ Please wait {wait_time} seconds before requesting another key.\n\n"
            f"⚠️ Rate limit: 1 request per {RATE_LIMIT_SECONDS} seconds for security."
        )
        send_message(chat_id, message)
        return
    
    # Update last request time
    user_last_request[user_id] = current_time
    
    # Send processing message
    send_message(chat_id, "🔄 Generating your key...")
    
    try:
        # Make API request
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        
        # Extract key
        key = None
        if 'key' in data:
            key = data['key']
        elif 'failed_url' in data:
            match = re.search(r'key=([^&\s]+)', data['failed_url'])
            key = match.group(1) if match else None
        elif 'error' in data and 'key=' in data['error']:
            match = re.search(r'key=([A-Za-z0-9]+)', data['error'])
            key = match.group(1) if match else None
        
        # Validate and send key
        if key and re.match(r'^[A-Za-z0-9]{8,20}$', key):
            success_message = (
                f"✅ Your Key is Ready! 🎉\n\n"
                f"🔑 Key: `{key}`\n\n"
                f"⚠️ **Important:**\n"
                f"• Use this key within 10 minutes\n"
                f"• After that, it will expire\n\n"
                f"Tap to copy the key!"
            )
            send_message(chat_id, success_message, parse_mode='Markdown')
        else:
            send_message(chat_id, 
                "❌ Error: Could not extract valid key from API.\n\n"
                "Please try again with /key or /generate"
            )
    
    except requests.exceptions.Timeout:
        send_message(chat_id,
            "❌ Request timeout. API took too long to respond.\n\n"
            "Please try again with /key"
        )
    except requests.exceptions.RequestException:
        send_message(chat_id,
            "❌ Network error occurred.\n\n"
            "Please check your connection and try again with /key"
        )
    except Exception as e:
        send_message(chat_id,
            "❌ An unexpected error occurred.\n\n"
            "Please try again with /key"
        )

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'Bot is running',
        'message': 'Telegram bot webhook is active'
    })

@app.route('/', methods=['POST'])
def webhook():
    """Handle incoming Telegram webhooks"""
    if not BOT_TOKEN:
        return jsonify({'error': 'Bot token not configured'}), 500
    
    try:
        update = request.get_json()
        
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            user_name = message['from'].get('first_name', 'User')
            
            if 'text' in message:
                text = message['text']
                
                # Handle commands
                if text == '/start':
                    handle_start(chat_id, user_name)
                elif text == '/help':
                    handle_help(chat_id)
                elif text in ['/generate', '/key']:
                    handle_key_generation(chat_id, user_id)
                else:
                    send_message(chat_id, 
                        "Sorry, I don't understand that command. Use /help to see available commands."
                    )
        
        return jsonify({'ok': True}), 200
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
handler = app
