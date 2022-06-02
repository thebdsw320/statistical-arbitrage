from price_klines import get_price_klines
import json

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

# Store price history for all available pairs
def store_price_history(symbols_list, file_name):
    
    # Get prices and store in DataFrame
    count_stored = 0
    count_not_stored = 0
    price_history_data = dict()
    
    for symbol in symbols_list:
        symbol_name = symbol['name']
        price_history = get_price_klines(symbol_name)

        if len(price_history) > 0:
            price_history_data[symbol_name] = price_history
            count_stored += 1
            print(f'{count_stored} items stored')
        else:
            count_not_stored += 1
            print(style.RED)
            print(f'{symbol_name} not stored, {count_not_stored} items not stored')
            print(style.WHITE)
            
    if len(price_history_data) > 0:        
        with open(file_name, 'w') as f:
            json.dump(price_history_data, f, indent=4)
        
        print(style.GREEN)
        print(f'Prices saved succesfully on {file_name}')
        print(style.WHITE)