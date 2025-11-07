#!/bin/bash

# Telegram Bot Webhook Setup Script
# This script sets up the webhook for your Telegram bot on Vercel

echo "========================================"
echo "Telegram Bot Webhook Setup"
echo "========================================"
echo ""

# Check if BOT_TOKEN is provided
if [ -z "$1" ]; then
    echo "❌ Error: Bot token not provided"
    echo ""
    echo "Usage: ./setup_webhook.sh YOUR_BOT_TOKEN"
    echo ""
    echo "Example: ./setup_webhook.sh 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    echo ""
    exit 1
fi

BOT_TOKEN="$1"
WEBHOOK_URL="https://kuchbhi-alpha.vercel.app/api/telegram"

echo "🔧 Setting webhook..."
echo "Bot Token: ${BOT_TOKEN:0:10}..."
echo "Webhook URL: $WEBHOOK_URL"
echo ""

# Set the webhook
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "'"$WEBHOOK_URL"'"}')

echo "Response: $RESPONSE"
echo ""

# Check if successful
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Webhook set successfully!"
    echo ""
    echo "🔍 Verifying webhook info..."
    echo ""
    
    # Get webhook info
    curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool
    
    echo ""
    echo "========================================"
    echo "✅ Setup Complete!"
    echo "========================================"
    echo ""
    echo "Your bot is now ready! Try these commands:"
    echo "  /start - Welcome message"
    echo "  /key - Generate a key"
    echo "  /generate - Generate a key"
    echo "  /help - Show help"
    echo ""
else
    echo "❌ Failed to set webhook"
    echo "Please check:"
    echo "  1. Bot token is correct"
    echo "  2. Vercel deployment is successful"
    echo "  3. The webhook URL is accessible"
    echo ""
fi
