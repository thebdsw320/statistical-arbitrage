import PySimpleGUI as sg
import json

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
    
def make_window():
    right_click_menu_def = [[], ['Exit']]
    
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
        [sg.Input(k='tradeable_capital_usdt')],
        [sg.Text('Stop Loss (Stop loss at market order in case of drastic event)')],
        [sg.Input(k='stop_loss_fail_safe')],
        [sg.Text('Signal Trigger Threshold (Z-Score threshold which determines trade [must be above zero])')],
        [sg.Input(k='signal_trigger_thresh')],
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
        [sg.Button('Save Settings')]        
    ]
    
    layout = [[sg.Text('Statistical Arbitrage -  Execution Settings', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    
    layout += [[sg.TabGroup([[  sg.Tab('Settings', configuration_layout)    ]], 
                            key='-TAB GROUP-', expand_x=True, expand_y=True), ]]
    
    layout[-1].append(sg.Sizegrip())
    
    window = sg.Window('Statistical Arbitrage - Settings', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True)    
    
    window.set_min_size(window.size)
    return window

def main():
    window = make_window()
    
    while True:
        event, values = window.read()
        
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            pass
        if event in (None, 'Exit'):
            break     
        elif event == 'Save Settings':
            mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret = values['mode_option'], values['ticker1'], values['ticker2'], values['signal_positive_ticker'], values['signal_negative_ticker'], values['rounding_ticker1'], values['rounding_ticker2'], values['quantity_rounding_ticker1'], values['quantity_rounding_ticker2'], values['limit_order_basis'], values['tradeable_capital_usdt'], values['stop_loss_fail_safe'], values['signal_trigger_thresh'], values['timeframe'], values['kline_limit'], values['zscore_window'], values['public_key'], values['private_key']
            update_settings(mode, ticker1, ticker2, signal_positive_ticker, signal_negative_ticker, rounding_ticker_1, rounding_ticker_2, quantity_rounding_ticker_1, quantity_rounding_ticker_2, limit_order_basis, tradeable_capital_usdt, stop_loss_fail_safe, signal_trigger_thresh, timeframe, kline_limit, zscore_window, api_key, api_secret)
            print(style.GREEN)
            print('Settings updated')
            print(style.WHITE)
            break
    
    window.close()
    exit(0) 
    
if __name__ == '__main__':
    main()