import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import json, time
from ws_connect import ws_public, subs_public
from position_calls import open_position_confirmation, active_position_confirmation
from trade_managment import manage_new_trades
from execution_calls import set_leverage
from close_positions import close_all_positions
from get_zscore import get_latest_zscore
from save_status import save_status

with open('./settings.json', 'r') as f:
    data = json.load(f)
    
signal_positive_ticker = data['signalPositiveTicker']
signal_negative_ticker = data['signalNegativeTicker']

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

def exec():
    # Initial printout
    print(style.GREEN)
    print('StatBot initiated...')
    print(style.WHITE)
    
    # Initialise variables
    status_dict = {
        'message': 'starting...'
    }
    order_long = {}
    order_short = {}
    signal_sign_positive = False
    signal_side = ''
    kill_switch = 0
    
    # Save status
    save_status(status_dict)
    
    # Set leverage in case forgotten to do so on the platform 
    print(style.BLUE)
    print(f'Setting leverage for tickers: {signal_positive_ticker} - {signal_negative_ticker}')
    print(style.WHITE)
    set_leverage(signal_positive_ticker)
    set_leverage(signal_negative_ticker)
    
    # Commence bot
    print(style.BLUE)
    print('Seeking trades...')
    print(style.WHITE)
    
    while True:
        # Pause - Protect API
        time.sleep(2)
        
        # Check if open trades already exist
        is_p_ticker_open = open_position_confirmation(signal_positive_ticker)
        is_n_ticker_open = open_position_confirmation(signal_negative_ticker)
        is_p_ticker_active = active_position_confirmation(signal_positive_ticker)
        is_n_ticker_active = active_position_confirmation(signal_negative_ticker)
        
        checks = [is_p_ticker_open, is_n_ticker_open, is_p_ticker_active, is_n_ticker_active]
        is_manage_new_trades = not any(checks)
        
        # Save status
        status_dict['message'] = 'Initial checks made...'
        status_dict['checks'] = checks
        save_status(status_dict)
        
        # Check for signal and place new trades
        if is_manage_new_trades and kill_switch == 0:
            status_dict['message'] = 'Managing new trades...'
            save_status(status_dict)
            kill_switch, signal_side = manage_new_trades(kill_switch)

        # Managing open kill switch if positions change or should reach 2
        # Check for signal to be false
        if kill_switch == 1:
            # Get and save the latest z-score
            zscore, signal_sign_positive = get_latest_zscore()

            # Close positions
            if signal_side == 'positive' and zscore < 0:
                kill_switch = 2
            if signal_side == 'negative' and zscore >= 0:
                kill_switch = 2

            # Put back to zero if trades are closed
            if is_manage_new_trades and kill_switch != 2:
                kill_switch = 0
        
        # Close all active orders and positions
        if kill_switch == 2:
            status_dict['message'] == 'Closing existing trades...'
            save_status(status_dict)
            kill_switch = close_all_positions(kill_switch)

            # Sleep 5 seconds
            time.sleep(3)    