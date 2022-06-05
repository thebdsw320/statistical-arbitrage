import json, time, datetime
from calculations import extract_close_prices
from pybit import HTTP

with open('./settings.json', 'r') as f:
    data = json.load(f)
    
ticker1 = data['ticker1']
ticker2 = data['ticker2']
api_url = data['apiURL']  
timeframe = int(data['timeframe'])
kline_limit = int(data['klineLimit'])

session_public = HTTP(api_url)

# Get trade liquidity for ticker
def get_ticker_trade_liquidity(ticker):
    # Get trades history
    trades = session_public.public_trading_records(
        symbol=ticker,
        limit=50
    )
    
    # Get the average liquidity
    quantity_list = []
    
    if 'result' in trades.keys():
        for trade in trades['result']:
            quantity_list.append(trade['qty'])
    
    # Return output
    if len(quantity_list) > 0:
        avg_liquidity = sum(quantity_list) / len(quantity_list)
        result_trades_price = float(trades['result'][0]['price'])

        return avg_liquidity, result_trades_price
    
    return 0, 0

# Get start times
def get_timestamps():
    time_start_date = 0
    time_next_date = 0
    now = datetime.datetime.now()
    
    if timeframe == 60:
        time_start_date = now - datetime.timedelta(hours=kline_limit)
        time_next_date = now + datetime.timedelta(seconds=30)
    if timeframe == 'D':
        time_start_date = now - datetime.timedelta(days=kline_limit)
        time_next_date = now + datetime.timedelta(minutes=1)
        
    time_start_seconds = int(time_start_date.timestamp())
    time_next_seconds = int(time_next_date.timestamp())
    time_now_seconds = int(now.timestamp())
    return time_start_seconds, time_now_seconds, time_next_seconds

# Get historical prices (klines)
def get_price_klines(ticker):
    # Get prices
    time_start_seconds, _, _ = get_timestamps()
    prices = session_public.query_mark_price_kline(
        symbol=ticker, 
        interval=timeframe, 
        limit=kline_limit,
        from_time=time_start_seconds   
    )
    
    # Manage API Calls
    time.sleep(0.1)
    
    # Return prices output
    if len(prices['result']) != kline_limit:
        return []
    return prices['result']

# Get latest klines
def get_latest_klines():
    series1 = []
    series2 = []
    prices1 = get_price_klines(ticker1)
    prices2 = get_price_klines(ticker2)
    
    if len(prices1) > 0:
        series1 = extract_close_prices(prices1)
    if len(prices2) > 0:
        series2 = extract_close_prices(prices2)
        
    return series1, series2