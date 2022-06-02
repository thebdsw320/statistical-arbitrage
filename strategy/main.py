from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import PySimpleGUI as sg
import os, json, base64
from get_symbols import get_tradeable_symbols
from store_prices import store_price_history
from cointegration import get_cointegrated_pairs
from plot_trends import plot

#sg.set_options(icon=base64.b64encode(open(r'/home/bdsw3207/Code/Statistical Arbitrage/bot/strategy/icon.png', 'rb').read()))
os.system('')

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

def make_window():
    sg.theme('BlueMono')
    right_click_menu_def = [[], ['About', 'Exit']]
    
    logging_layout = [[sg.Text("Output")],
                      [sg.Multiline(
                                    size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True, 
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True
                                    )]]   
    
    get_symbols_layout = [[sg.Text('Get tradeable symbols from ByBit Exchange')],
                     [sg.Text('Enter filename')],
                     [sg.Input(key='filename_symbols')],
                     [sg.Button('Get Symbols')]]
    
    cointegration_layout = [[sg.Text('Check for cointegrated pairs')],
                     [sg.Text('Enter JSON filename with pairs from the previous window')],
                     [sg.Button('Browse File')],
                     #[sg.Input(key='filename_from_cointegration')],
                     [sg.Text('Enter filename to save cointegrated pairs')],
                     [sg.Input(key='filename_to_cointegration')],
                     [sg.Button('Check Cointegration')]]
    
    plot_layout = [[sg.Text('Plot trends and save for backtesting')],
                   [sg.Text('Enter the first symbol:')],
                   [sg.Input(key='symbol1')],
                   [sg.Text('Enter the first symbol:')],
                   [sg.Input(key='symbol2')],
                   [sg.Text('Enter JSON filename with pairs from the previous window')],
                   [sg.Button('Browse File')],
                   [sg.Text('Enter filename to save data for backtest of previous symbols')],
                   [sg.Input(key='filename_backtest')],               
                   [sg.Button('Plot')]]
    
    layout = [[sg.Text('Statistical Arbitrage -  ByBit', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    
    layout += [[sg.TabGroup([[  sg.Tab('Output', logging_layout),
                                sg.Tab('Get Symbols', get_symbols_layout),
                                sg.Tab('Cointegration Check', cointegration_layout),
                                sg.Tab('Plot', plot_layout)]], 
                            key='-TAB GROUP-', expand_x=True, expand_y=True), ]]
    
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Statistical Arbitrage - ByBit', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True)#, keep_on_top=True)
    
    window.set_min_size(window.size)
    return window

def main():
    window = make_window()
    
    while True: 
        event, values = window.read(timeout=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ ', event, ' ==============')
        if event in (None, 'Exit'):
            break                     
        elif event == 'About':
            sg.popup('Statistical Arbitrage - ByBit',
                     '- Get tradeable symbols',
                     '- Store symbols in JSON',
                     '- Check for cointegration',
                     '- Crete a file with cointegration data for backtesting', keep_on_top=True) 
        elif event == 'Get Symbols':
            print(style.GREEN)
            print('Getting symbols...')
            print(style.WHITE)  
             
            symbols_response = get_tradeable_symbols()
            file_name = values['filename_symbols']
            
            print(style.GREEN)
            print('Constructing and saving data price to JSON...')
            print(style.WHITE) 
             
            if len(symbols_response) > 0:
                store_price_history(symbols_response, file_name)
            else:
                print(style.RED)
                print(f'Found {len(symbols_response)} tradeable items')
                print(style.WHITE)
        elif event == 'Browse File':
            file_from = sg.popup_get_file('Choose your file')#, keep_on_top=True)  
        elif event == 'Browse File1':
            file_from = sg.popup_get_file('Choose your file')#, keep_on_top=True)              
        elif event == 'Check Cointegration':
            #file_from = values['filename_from_cointegration']
            file_name = values['filename_to_cointegration']

            print(style.BLUE)
            print(f'Calculating cointegration for data in file {str(file_from)}...')
            print(style.WHITE) 
            
            file_name = values['filename_to_cointegration']
            
            with open(f'{file_from}', 'r') as file:
                price_data = json.load(file)
                
                if len(price_data) > 0:
                    cointegrated_pairs = get_cointegrated_pairs(price_data, file_name)
                    print(style.GREEN)
                    print(f'Data computed succesfully! Saved in {file_name}')
                    print(style.WHITE)
                else:
                    print(style.RED)
                    print('Something went wrong with your list of prices! Check JSON file')
                    print(style.WHITE)  
        elif event == 'Plot':
            print(style.BLUE)
            print('Plotting trends...')
            print(style.WHITE)
            
            symbol1 = values['symbol1']
            symbol2 = values['symbol2']
            file_name = values['filename_backtest']
            
            print(style.BLUE)
            print(f'Plotting trends for {symbol1}-{symbol2}')
            print(style.WHITE)
            
            with open(file_from, 'r') as file:
                price_data = json.load(file)
                if len(price_data) > 0:
                    plot(symbol1, symbol2, price_data, file_name)            
                             
    window.close()
    exit(0)              
     
# Entry point
if __name__ == '__main__':
    main()
    # # # Get tradeable symbols
    # print(style.GREEN)
    # print('Getting symbols...')
    # print(style.WHITE)
    
    # # symbols_response = get_tradeable_symbols()
    
    # # # Construct and save price history
    # # print(style.GREEN)
    # # print('Constructing and saving data price to JSON...')
    # # print(style.WHITE)
    
    # # if len(symbols_response) > 0:
    # #     store_price_history(symbols_response)
    # # else:
    # #     print(style.RED)
    # #     print(f'Found {len(symbols_response)} tradeable items')
    # #     print(style.WHITE)
    
    # # # Find cointegrated pairs
    # print(style.BLUE)
    # file_name = input('File name: ')
    # # print(f'Calculating cointegration for data in file {file_name}...')
    # print(style.WHITE)
    
    
    # with open(f'./{file_name}', 'r') as file:
    #     price_data = json.load(file)
    #     if len(price_data) > 0:
    #         cointegrated_pairs, filename = get_cointegrated_pairs(price_data)
    #         print(style.GREEN)
    #         print(f'Data computed succesfully! Saved in {filename}')
    #         print(style.WHITE)
    #     else:
    #         print(style.RED)
    #         print('Something went wrong with your list of prices! Check JSON file')
    #         print(style.WHITE)
            
    # # Plot trends and save for backtesting
    # print(style.BLUE)
    # print('Plotting trends...')
    # print(style.WHITE)
    
    # print(style.YELLOW)
    # symbol1 = input('Please enter the first symbol: ')
    # symbol2 = input('Please enter the second symbol: ')
    
    # print(style.BLUE)
    # print(f'Plotting trends for {symbol1}-{symbol2}')
    # print(style.WHITE)
    
    # with open(file_name, 'r') as file:
    #     price_data = json.load(file)
    #     if len(price_data) > 0:
    #         plot(symbol1, symbol2, price_data)    