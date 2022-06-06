import json
from pybit import HTTP
from ws_connect import ws_public, subs_public
from calculations import get_trade_details
from price_calls import get_latest_klines
from stats import calculate_metrics

with open('settings.json', 'r') as f:
    data = json.load(f)

# Get latest z-score 
def get_latest_zscore():
    # Get latest asset orderbook prices and add dummy price for latest
    orderbook1 = ws_public.fetch(subs_public[0])
    mid_price1, _, _ = get_trade_details(orderbook1)
    orderbook2 = ws_public.fetch(subs_public[1])
    mid_price2, _, _ = get_trade_details(orderbook2)
    
    # Get latest price history
    series1, series2 = get_latest_klines()
    
    # Get z-score and confirm if hot
    if len(series1) > 0 and len(series2) > 0:
        # Replace last kline price with latest orderbook mid price
        series1 = series1[:-1]
        series2 = series2[:-1]
        
        series1.append(mid_price1)
        series2.append(mid_price2)
        
        # Get latest z-score
        _, zscore_list = calculate_metrics(series1, series2)
        zscore = zscore_list[-1]
        
        if zscore > 0:
            signal_sign_positive = True
        else:
            signal_sign_positive = False
        
        # Return output
        return zscore, signal_sign_positive
    
    # Return output if not true
    return 

get_latest_zscore()