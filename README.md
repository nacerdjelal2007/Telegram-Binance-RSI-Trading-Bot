# Telegram-Binance-RSI-Trading-Bot

Binance RSI Trading Bot
A Python bot that monitors RSI (Relative Strength Index) for any cryptocurrency pair available on Binance, sending alerts to Telegram when significant changes occur.

Features
🚀 Multi-Crypto Support: Works with any trading pair available on Binance (BTCUSDT, ETHUSDT, etc.)
📈 Real-time RSI Monitoring: Customizable RSI periods and thresholds
🔔 Telegram Alerts: Instant notifications for oversold/overbought conditions
⏱ Scheduled Updates: Provides regular 3-minute updates
⚙️ Easy Configuration: Change cryptocurrency pair by modifying one variable
Prerequisites
Python 3.8+
Binance API keys
Telegram bot token and chat ID
TA-Lib library
Installation
Clone the repository:
git clone https://github.com/nacerdjelal2007/Telegram-Binance-RSI-Trading-Bot.git
cd Telegram-Binance-RSI-Trading-Bot
Install dependencies:
pip install python-binance pandas TA-Lib python-dotenv
Create a
.env
file with your credentials:
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
Configuration
To monitor a different cryptocurrency, simply change the
TICKER
variable in the code:

TICKER = "BTCUSDT"  # Change this to any valid Binance trading pair
Other customizable parameters:

RSI_PERIOD = 14      # RSI calculation period (14 is standard)
INTERVAL = "3m"      # Candle interval (1m, 5m, 15m, etc.)
CHECK_INTERVAL = 0.5 # How often to check (in seconds)
Usage
Run the bot:

python binance_rsi_bot.py
The bot will:

Check price and RSI every 3 minutes
Send alerts when RSI crosses 30 (oversold) or 70 (overbought)
Provide regular updates to your Telegram channel
Example Telegram Alert
⏰ Time: 14:03:00
🔌 Status: CONNECTED
📊 RSI: 72.15 (OVERBOUGHT)
💎 BTC Price: $42,850.20

#Bitcoin #Trading
Supported Cryptocurrencies
This bot works with any trading pair available on Binance, including:

BTCUSDT (Bitcoin)
ETHUSDT (Ethereum)

And many more...
TA-Lib Installation
For Linux:

sudo apt-get install python3-dev build-essential
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
For MacOS:

brew install ta-lib
pip install TA-Lib
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
MIT
