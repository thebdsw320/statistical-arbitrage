import PySimpleGUI as sg
import json, time, multiprocessing
from main import exec
from v2_main import exec_v2

sg.theme('BlueMono')

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

def update_settings(mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret):
    api_url = "https://api-testnet.bybit.com" if mode == "Testnet" else "https://api.bybit.com"
    ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "Testnet" else "wss://stream.bybit.com/realtime_public"
    
    f = open('./settings.json', 'r')
    data = json.load(f)
        
    data['mode'] = mode
    data['timeframe'] = timeframe
    data['klineLimit'] = kline_limit
    data['zscoreWindow'] = zscore_window
    data['apiSecret'] = api_secret
    data['apiKey'] = api_key
    data['apiURL'] = api_url
    data['wsPublicURL'] = ws_public_url
    data['ticker1'] = ticker1
    data['ticker2'] = ticker2
    data['signalPositiveTicker'] = signal_positive_ticker
    data['signalNegativeTicker'] = signal_negative_ticker
    data['roundingTicker1'] = rounding_ticker_1
    data['roundingTicker2'] = rounding_ticker_2
    data['quantityRoundingTicker1'] = quantity_rounding_ticker_1
    data['quantityRoundingTicker2'] = quantity_rounding_ticker_2
    data['limitOrderBasis'] = limit_order_basis
    data['tradeableCapitalUSDT'] = tradeable_capital_usdt
    data['stopLossFailSafe'] = stop_loss_fail_safe
    data['signalTriggerThresh'] = signal_trigger_thresh
    
    f = open('./settings.json', 'w')
    json.dump(data, f, indent=4)
    f.close()

def update_settings_v2(mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret, max_trades_per_signal, max_loss_usdt_total):
    api_url = "https://api-testnet.bybit.com" if mode == "Testnet" else "https://api.bybit.com"
    ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "Testnet" else "wss://stream.bybit.com/realtime_public"
    
    f = open('./settings_v2.json', 'r')
    data = json.load(f)
        
    data['mode'] = mode
    data['timeframe'] = timeframe
    data['klineLimit'] = kline_limit
    data['zscoreWindow'] = zscore_window
    data['apiSecret'] = api_secret
    data['apiKey'] = api_key
    data['apiURL'] = api_url
    data['wsPublicURL'] = ws_public_url
    data['ticker1'] = ticker1
    data['ticker2'] = ticker2
    data['signalPositiveTicker'] = signal_positive_ticker
    data['signalNegativeTicker'] = signal_negative_ticker
    data['roundingTicker1'] = rounding_ticker_1
    data['roundingTicker2'] = rounding_ticker_2
    data['quantityRoundingTicker1'] = quantity_rounding_ticker_1
    data['quantityRoundingTicker2'] = quantity_rounding_ticker_2
    data['limitOrderBasis'] = limit_order_basis
    data['tradeableCapitalUSDT'] = tradeable_capital_usdt
    data['stopLossFailSafe'] = stop_loss_fail_safe
    data['signalTriggerThresh'] = signal_trigger_thresh
    data['maxTradesPerSignal'] = max_trades_per_signal
    data['maxLossUSDTTotal'] = max_loss_usdt_total
    
    f = open('./settings_v2.json', 'w')
    json.dump(data, f, indent=4)
    f.close()

def execution():
    while True:
        try:
            exec()
        finally:
            exec()

def execution_v2():
    while True:
        try:
            exec_v2()
        finally:
            exec_v2()    

def make_window():
    # Right click menu
    right_click_menu_def = [[], ['Exit']]
    
    # Set layouts
    configuration_layout = [
        [sg.Text('Select Mode')], 
        [sg.Combo(values=('Testnet', 'Mainnet'), default_value='Testnet', readonly=True, k='mode_option')],
        [sg.Frame('Tickers (Check backtest results)', [
            [sg.Text('Ticker 1:'), sg.Input(key='ticker1')],
            [sg.Text('Ticker 2:'), sg.Input(key='ticker2')],
            [sg.Text('Signal Positive Ticker:'), sg.Input(key='signal_positive_ticker')],
            [sg.Text('Signal Negative Ticker:'), sg.Input(key='signal_negative_ticker')],
            [sg.Text('Rounding Ticker 1:'), sg.Input(key='rounding_ticker1')],
            [sg.Text('Rounding Ticker 2:'), sg.Input(key='rounding_ticker2')],
            [sg.Text('Quantity Rounding Ticker 1:'), sg.Input(key='quantity_rounding_ticker1')],
            [sg.Text('Quantity Rounding Ticker 2:'), sg.Input(key='quantity_rounding_ticker2')]
        ])],
        [sg.Text('Limit Order Basis (Will ensure positions [except for Close] will be placed on limit basis)')],
        [sg.Combo(values=('True', 'False'), default_value='True', readonly=True, k='limit_order_basis')],
        [sg.Text('Tradeable Capital USDT (Total tradeable capital to be split between both pairs)')],
        [sg.Input(key='tradeable_capital_usdt')],
        [sg.Frame('V2 Execution', [
            [sg.Text('Max Loss USDT Total (Only for V2 execution)')],
            [sg.Input(key='max_loss_usdt_total')],
            [sg.Text('Max Trades Per Signal')],
            [sg.Input(key='max_trades_per_signal')]
        ])],
        [sg.Text('Stop Loss (Stop loss at market order in case of drastic event)')],
        [sg.Input(key='stop_loss_fail_safe')],
        [sg.Text('Signal Trigger Threshold (Z-Score threshold which determines trade [must be above zero])')],
        [sg.Input(key='signal_trigger_thresh')],
        [sg.Text('Enter timeframe')], 
        [sg.Input(key='timeframe')],
        [sg.Text('Enter K-Line limit')], 
        [sg.Input(key='kline_limit')],
        [sg.Text('Enter Z-Score Window')], 
        [sg.Input(key='zscore_window')],
        [sg.Frame('Keys', [
            [sg.Text('Enter API key:'), sg.Input(key='public_key')],
            [sg.Text('Enter API secret:'), sg.Input(key='private_key')]
        ])],
        [sg.Button('Save Settings')], 
        [sg.Button('Save Settings V2')]      
    ]
    
    execution_layout = [
        [sg.Frame('V1', [
            [sg.Text('Execute bot')],
            [sg.Button('Execute')],
            [sg.Button('Stop')]
        ])],
        [sg.Frame('V2', [
            [sg.Text('Execute bot V2')],
            [sg.Button('Execute V2')],
            [sg.Button('Stop V2')]
        ])],
    ]
    
    # Layout setting
    layout = [[sg.Text('Statistical Arbitrage -  Execution', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    
    layout += [[sg.TabGroup([[  sg.Tab('Settings', configuration_layout),
                                sg.Tab('Execution', execution_layout)]], 
                            key='-TAB GROUP-', expand_x=True, expand_y=True), ]]
    
    layout[-1].append(sg.Sizegrip())
    
    # Window setting
    window = sg.Window('Statistical Arbitrage - Execution', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True)    
    
    window.set_min_size(window.size)
    return window

def main():
    # Get window with layouts
    window = make_window()
    
    # Event loop
    while True:
        # Read values
        event, values = window.read()
        
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            pass
        if event in (None, 'Exit'):
            break     
        # Update settings with specified values
        elif event == 'Save Settings':
            mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret = values['mode_option'], values['ticker1'], values['ticker2'], values['signal_positive_ticker'], values['signal_negative_ticker'], values['rounding_ticker1'], values['rounding_ticker2'], values['quantity_rounding_ticker1'], values['quantity_rounding_ticker2'], values['limit_order_basis'], values['tradeable_capital_usdt'], values['stop_loss_fail_safe'], values['signal_trigger_thresh'], values['timeframe'], values['kline_limit'], values['zscore_window'], values['public_key'], values['private_key']
            update_settings(mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret)
            print(style.GREEN)
            print('Settings updated')
            print(style.WHITE)
        # Update settings with specified values for bot V2
        elif event == 'Save Settings V2':
            mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret, max_trades_per_signal, max_loss_usdt_total = values['mode_option'], values['ticker1'], values['ticker2'], values['signal_positive_ticker'], values['signal_negative_ticker'], values['rounding_ticker1'], values['rounding_ticker2'], values['quantity_rounding_ticker1'], values['quantity_rounding_ticker2'], values['limit_order_basis'], values['tradeable_capital_usdt'], values['stop_loss_fail_safe'], values['signal_trigger_thresh'], values['timeframe'], values['kline_limit'], values['zscore_window'], values['public_key'], values['private_key'], values['max_trades_per_signal'], values['max_loss_usdt_total']
            update_settings_v2(mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret, max_trades_per_signal, max_loss_usdt_total)
            print(style.GREEN)
            print('Settings updated')
            print(style.WHITE)
        # Execute bot
        elif event == 'Execute':
            time.sleep(1)
            try:
                execution_process = multiprocessing.Process(name='execution', target=execution, daemon=True)
                execution_process.start()
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass  
        elif event == 'Stop':
            try:
                execution_process.terminate()
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass  
        # Execute bot V2
        elif event == 'Execute V2':
            time.sleep(1)
            try:
                execution_process_v2 = multiprocessing.Process(name='execution v2', target=execution_v2, daemon=True)
                execution_process_v2.start()
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass  
        elif event == 'Stop V2':
            try:
                execution_process_v2.terminate()
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass  
            
    window.close()
    exit(0) 
    
if __name__ == '__main__':
    main()