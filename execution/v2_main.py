import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import json, datetime
from v2_position_info import get_closed_pnl_info, place_market_close_order, get_position_info
from v2_execution_calls import set_leverage, initialise_order_execution
from v2_get_zscore import get_latest_zscore
from pybit import HTTP

with open('settings_v2.json', 'r') as f:
    data = json.load(f)
    
signal_positive_ticker = data['signalPositiveTicker']
signal_negative_ticker = data['signalNegativeTicker']
max_loss_usdt_total = int(data['maxLossUSDTTotal'])
signal_trigger_thresh = float(data['signalTriggerThresh'])
tradeable_capital_usdt = int(data['tradeableCapitalUSDT'])
max_trades_per_signal = int(data['maxTradesPerSignal'])
api_url = data['apiURL']
api_key = data['apiKey']
api_secret = data['apiSecret']

session_private = HTTP(api_url, api_key=api_key, api_secret=api_secret)

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def exec_v2():
    # Set variables
    halt_trading = False
    close_check_2 = False

    # Set leverage in case forgotten to do so on platform
    set_leverage(signal_positive_ticker)
    set_leverage(signal_negative_ticker)

    # Get zscore and check if hot
    zscore, signal_sign_positive = get_latest_zscore()
    hot = True if abs(zscore) > signal_trigger_thresh else False

    # Get and print datetime
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    
    print(style.BLUE)
    print(f"Datetime: {current_time},", f"Z-Score: {round(zscore,2)}")
    print(style.WHITE)

    # Get P&L information
    closed_pnl_1 = get_closed_pnl_info(signal_positive_ticker)
    closed_pnl_2 = get_closed_pnl_info(signal_negative_ticker)

    # Get position information
    side_1, size_1, pnl_un_1, pos_value_1 = get_position_info(signal_positive_ticker)
    side_2, size_2, pnl_un_2, pos_value_2 = get_position_info(signal_negative_ticker)

    # Check combined P&L position
    close_check_1 = (closed_pnl_1 + closed_pnl_2 + pnl_un_1 + pnl_un_2) <= max_loss_usdt_total
    if not hot:
        if size_1 > 0 or size_2 > 0:
            close_check_2 = True

    # Close open positions
    if close_check_1 or close_check_2:

        # Handle messaging
        print(style.YELLOW)
        print("Closing trades...", zscore)
        print(style.WHITE)

        # Halt trading
        halt_trading = True

        # Cancel all active orders
        session_private.cancel_all_active_orders(symbol=signal_positive_ticker)
        session_private.cancel_all_active_orders(symbol=signal_negative_ticker)

        # Close all positions
        if size_1 > 0:
            place_market_close_order(signal_positive_ticker, side_2, size_1) # use side 2

        if size_2 > 0:
            place_market_close_order(signal_negative_ticker, side_1, size_2) # use side 1

    # Open new positions
    position_capital_allowance_total = tradeable_capital_usdt / 2
    trade_check_1 = pos_value_1 < position_capital_allowance_total and pos_value_2 < position_capital_allowance_total
    trade_check_2 = hot
    if trade_check_1 and trade_check_2:

        # Handle messaging
        print(style.GREEN)
        print("Placing trades...", zscore)
        print(style.WHITE)

        # Determine Long ticker and short ticker
        if signal_sign_positive:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker

        # Place market orders
        initialise_order_execution(long_ticker, "Long", position_capital_allowance_total / max_trades_per_signal)
        initialise_order_execution(short_ticker, "Short", position_capital_allowance_total / max_trades_per_signal)
 