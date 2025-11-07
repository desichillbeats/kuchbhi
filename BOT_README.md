# Telegram Key Generator Bot 🎉

A Telegram bot that generates keys using the API endpoint. This bot provides the same functionality as the web key generator but through Telegram!

## Features

- 🔑 Generate keys instantly with `/generate` command
- ⚡ Fast and reliable key generation
- 🎨 Beautiful formatted messages with emojis
- ⚠️ 10-minute expiry warnings
- 🛡️ Proper error handling

## Commands

- `/start` - Start the bot and see welcome message
- `/generate` - Generate a new key
- `/help` - Show help message with all commands

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/desichillbeats/kuchbhi.git
   cd kuchbhi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your bot token**
   
   Your Bot Token: `8365271416:AAEs0CyAaGQSwg0UsVkTag9E9n8T2nEYD-4`

   **Option A: Using Environment Variable (Recommended)**
   
   Windows:
   ```bash
   set TELEGRAM_BOT_TOKEN=8365271416:AAEs0CyAaGQSwg0UsVkTag9E9n8T2nEYD-4
   ```
   
   Linux/Mac:
   ```bash
   export TELEGRAM_BOT_TOKEN=8365271416:AAEs0CyAaGQSwg0UsVkTag9E9n8T2nEYD-4
   ```
   
   **Option B: Edit the file directly**
   
   Open `telegram_bot.py` and replace line 11:
   ```python
   BOT_TOKEN = '8365271416:AAEs0CyAaGQSwg0UsVkTag9E9n8T2nEYD-4'
   ```

4. **Run the bot**
   ```bash
   python telegram_bot.py
   ```

5. **Start using your bot!**
   - Open Telegram
   - Search for your bot
   - Send `/start` to begin
   - Use `/generate` to get your key

## How It Works

1. User sends `/generate` command
2. Bot makes a request to the API: `https://kuchbhi-alpha.vercel.app/api/get-key`
3. Bot extracts the key from the API response
4. Key is sent to the user in a formatted message
5. User can tap the key to copy it

## API Response Handling

The bot intelligently handles multiple response formats:
- Direct `key` field in JSON
- Key extracted from `failed_url` parameter
- Key extracted from `error` message

## Important Notes

⚠️ **Key Expiry**: All generated keys expire in 10 minutes. Make sure to use them quickly!

🔒 **Security**: Never share your bot token publicly. If you accidentally expose it, regenerate it through [@BotFather](https://t.me/BotFather).

## Troubleshooting

### Bot not responding
- Check if the bot is running (you should see "Bot is starting..." message)
- Verify your bot token is correct
- Make sure you have internet connection

### "Error generating key" message
- API might be temporarily down
- Check your internet connection
- Try again after a few seconds

### Import errors
- Make sure you installed all dependencies: `pip install -r requirements.txt`
- Try upgrading pip: `pip install --upgrade pip`

## Support

If you encounter any issues, please:
1. Check the troubleshooting section above
2. Make sure you're using the latest version
3. Check if the API endpoint is accessible

## License

This project is open source and available for personal use.

---

Made with ❤️ for easy key generation!
