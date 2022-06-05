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

# Bot 