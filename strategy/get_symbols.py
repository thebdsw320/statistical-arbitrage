import json
from pybit import HTTP

# Import API URL from settings.json
with open('./settings.json', 'r') as f:
    data = json.load(f)

session = HTTP(data['apiURL'])

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
    
# Get all tradeable symbols with own filters
def get_tradeable_symbols():
    symbols_list = list()
    symbols = session.query_symbol()
    
    if symbols['ret_msg'] == 'OK':
        symbols = symbols['result']
        for symbol in symbols:
            if (symbol['quote_currency'] == 'USDT') and (symbol['status'] == 'Trading'): #and (float(symbol['maker_fee']) < 0) :
                symbols_list.append(symbol)
    
    print(style.BLUE)
    print(f'Found {len(symbols_list)} items that match filters')
    print(style.WHITE)
    
    return symbols_list