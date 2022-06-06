import json
from pybit import HTTP

with open('settings.json', 'r') as f:
    data = json.load(f)

signal_positive_ticker = data['signalPositiveTicker']
signal_negative_ticker = data['signalNegativeTicker']
ticker1 = data['ticker1']
api_key = data['apiKey']
api_secret = data['apiSecret']
api_url = data['apiURL']

session_private = HTTP(api_url, api_key=api_key, api_secret=api_secret)

# Get position information
def get_position_info(ticker):
    # Declare output variables
    side = 0
    size = ""
    
    # Extract position info
    position = session_private.my_position(symbol=ticker)
    if 'ret_msg' in position.keys():
        if position['ret_msg'] == 'OK':
            if len(position['result']) == 2:
                if position['result'][0]['size'] > 0:
                    size = position['result'][0]['size']
                    side = 'Buy'
                else:
                    size = position['result'][0]['size']
                    side = 'Sell'
    
    # Return Output
    return side, size

# Place market close order
def place_market_close_order(ticker, side, size):
    # Close position
    session_private.place_active_order(
        symbol=ticker,
        side=side,
        order_type='Market',
        qty=size,
        time_in_force='GoodTillCancel',
        reduce_only=True,
        close_on_trigger=False
    )
    
    # Return
    return

# Close all positions for ticker
def close_all_positions(kill_switch):
    # Cancel all active orders
    session_private.cancel_all_active_orders(symbol=signal_positive_ticker)
    session_private.cancel_all_active_orders(symbol=signal_negative_ticker)
    
    # Get position information
    side1, size1 = get_position_info(signal_positive_ticker)
    side2, size2 = get_position_info(signal_negative_ticker)
    
    if size1 > 0:
        place_market_close_order(signal_positive_ticker, side2, size1) # Use side 2
    
    if size2 > 0:
        place_market_close_order(signal_negative_ticker, side1, size2) # Use side 1
    
    # Output results
    kill_switch = 0
    
    # Return
    return kill_switch