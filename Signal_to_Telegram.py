# Import required libraries
import time  # For time-related functions and sleep
from binance.client import Client  # Binance API client
import pandas as pd  # Data manipulation library
import talib as ta  # Technical analysis library
import Bot_telegram as Tb  # Custom Telegram bot module

# Configuration constants
API_KEY = 'your_api_key_here'  # Binance API public key
SECRET_KEY = 'your_secret_key_here'  # Binance API secret key
TICKER = "ETHUSDT"  # Ethereum trading pair
RSI_PERIOD = 14  # Number of periods for RSI calculation
INTERVAL = "3m"  # Candle interval (3 minutes)
CHECK_INTERVAL = 0.5  # Time between checks (in seconds)

# Initialize Binance API client
client = Client(api_key=API_KEY, api_secret=SECRET_KEY)

def get_current_price():
    """
    Get current ETH price from Binance
    Returns: float (price) or None if error occurs
    """
    try:
        # Get latest price ticker from Binance
        ticker = client.get_symbol_ticker(symbol=TICKER)
        return float(ticker['price'])  # Convert string to float
    except Exception as e:
        print(f"Error getting ETH price: {str(e)}")
        return None

def calculate_rsi():
    """
    Calculate RSI indicator for ETH
    Returns: tuple (RSI value, status message) or (None, error message)
    """
    try:
        # Get historical candle data from Binance
        klines = client.get_historical_klines(
            symbol=TICKER,
            interval=INTERVAL,
            start_str="2 hours ago UTC"  # Last 2 hours of data
        )
        
        # Check if data was received
        if not klines:
            return None, "No data available"
            
        # Create DataFrame with proper column names
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_volume',
            'taker_buy_quote_volume', 'ignore'
        ])
        
        # Convert data types
        df['close'] = pd.to_numeric(df['close'])  # Convert price to numeric
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp
        df.set_index('timestamp', inplace=True)  # Set timestamp as index
        
        # Calculate RSI using TA-Lib
        rsi = ta.RSI(df['close'], timeperiod=RSI_PERIOD)
        last_rsi = round(rsi.iloc[-2], 2)  # Get second-to-last RSI value
        
        # Determine RSI status
        if last_rsi < 30:
            status = "OVERSOLD"
        elif last_rsi > 70:
            status = "OVERBOUGHT"
        else:
            status = "NEUTRAL"
            
        return last_rsi, status
        
    except Exception as e:
        return None, f"RSI calculation error: {str(e)}"

def get_server_status():
    """
    Check Binance server status
    Returns: string (connection status)
    """
    try:
        status = client.get_system_status()
        return "CONNECTED" if status["status"] == 0 else "DISCONNECTED"
    except Exception as e:
        return f"ERROR: {str(e)}"

def prepare_message():
    """
    Prepare formatted message for Telegram
    Returns: string (formatted message) or None if error occurs
    """
    try:
        # Get current server time
        server_time = client.get_server_time()
        time_obj = pd.to_datetime(server_time["serverTime"], unit='ms')
        time_str = time_obj.strftime("%H:%M:%S")  # Format time string
        
        # Get market data
        eth_price = get_current_price()
        eth_rsi, eth_status = calculate_rsi()
        status = get_server_status()
        
        # Format price and RSI strings
        price_str = f"ETH Price: ${eth_price:,.2f}" if eth_price else "Price: Unavailable"
        rsi_str = f"RSI: {eth_rsi} ({eth_status})" if eth_rsi else "RSI: Unavailable"
        
        # Build complete message with emojis
        message = (
            f"⏰ Time: {time_str}\n"
            f"🔌 Status: {status}\n"
            f"📊 {rsi_str}\n"
            f"💎 {price_str}\n"
            f"\n#Ethereum #Trading"
        )
        
        return message
        
    except Exception as e:
        print(f"Message preparation error: {str(e)}")
        return None

def send_notifications():
    """
    Main notification loop
    Sends messages every 3 minutes at minute marks (00, 03, 06...)
    """
    last_minute = -1  # Track last notification minute
    
    while True:
        try:
            # Get current server time
            server_time = client.get_server_time()
            current_time = pd.to_datetime(server_time["serverTime"], unit='ms')
            current_minute = current_time.minute
            
            # Send notification at every 3-minute mark (00, 03, 06...)
            if current_minute != last_minute and current_minute % 3 == 0:
                message = prepare_message()
                if message:
                    Tb.telegram_send_message(message)
                last_minute = current_minute
                
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nProgram stopped by user")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(10)  # Wait longer after errors

if __name__ == "__main__":
    print("Starting Ethereum monitoring bot...")
    send_notifications()