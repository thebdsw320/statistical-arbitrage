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

def update_settings(mode, timeframe, kline_limit, zscore_window, api_public, api_private):
    api_url = "https://api-testnet.bybit.com" if mode == "Testnet" else "https://api.bybit.com"
    
    f = open('./settings.json', 'r')
    data = json.load(f)
        
    data['mode'] = mode
    data['timeframe'] = timeframe
    data['klineLimit'] = kline_limit
    data['zscoreWindow'] = zscore_window
    data['apiPublicKey'] = api_public
    data['apiPrivateKey'] = api_private
    data['apiURL'] = api_url
    
    f = open('settings.json', 'w')
    json.dump(data, f, indent=4)
    f.close()
    
def make_window():
    right_click_menu_def = [[], ['Exit']]
    
    configuration_layout = [
        [sg.Text('Select Mode')], 
        [sg.Combo(values=('Testnet', 'Mainnet'), default_value='Testnet', readonly=True, k='mode_option')],
        [sg.Text('Enter timeframe')], 
        [sg.Input(key='timeframe')],
        [sg.Text('Enter K-Line limit')], 
        [sg.Input(key='kline_limit')],
        [sg.Text('Enter Z-Score Window')], 
        [sg.Input(key='zscore_window')],
        [sg.Text('Enter public key:')],
        [sg.Input(key='public_key')],
        [sg.Text('Enter private key:')],
        [sg.Input(key='private_key')],
        [sg.Button('Save Settings')]        
    ]
    
    layout = [[sg.Text('Statistical Arbitrage -  Strategy Settings', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    
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
            mode, timeframe, kline_limit, zscore_window, api_public, api_private = values['mode_option'], values['timeframe'], values['kline_limit'], values['zscore_window'], values['public_key'], values['private_key']
            update_settings(mode, timeframe, kline_limit, zscore_window, api_public, api_private)
            print(style.GREEN)
            print('Settings updated')
            print(style.WHITE)
            break
    
    window.close()
    exit(0) 
    
if __name__ == '__main__':
    main()