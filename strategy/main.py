from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import PySimpleGUI as sg
import os, json, csv
from get_symbols import get_tradeable_symbols
from store_prices import store_price_history
from cointegration import get_cointegrated_pairs
from backtest import update_data, retrieve_data, update_values
from plot_trends import plot, save_data_backtest

sg.theme('BlueMono')

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

# Function to display csv in GUI
def table_csv():
    filename = sg.popup_get_file('CSV to preview', no_window=True, file_types=(('CSV Files','*.csv'),))
    if filename == '':
        return
    data = []
    header_list = []
    button = sg.popup_yes_no('Does this file have column names already?')
    if filename is not None:
        with open(filename, 'r') as infile:
            reader = csv.reader(infile)
            if button == 'Yes':
                header_list = next(reader)
            try:
                data = list(reader)  # read everything else into a list of rows
                if button == 'No':
                    header_list = ['column' + str(x) for x in range(len(data[0]))]
            except:
                sg.popup_error('Error reading file')
                return
            
    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Table(values=data,
                            headings=header_list,
                            max_col_width=25,
                            auto_size_columns=True,
                            justification='right',
                            num_rows=min(len(data), 20))]]


    window = sg.Window('Preview CSV', layout, grab_anywhere=False)
    event, values = window.read()

    window.close()    
    
# Function to display csv table with backtest data
def table_backtest():
    headings, data = retrieve_data()
    
    layout = [[sg.Table(values=data, headings=headings, auto_size_columns=True, justification='right')]]
    
    window = sg.Window('Backtest - Mean Reversion', layout, grab_anywhere=True)
    event, values = window.read()

    window.close()
    
# Make window 
def make_window():
    # Define right click menu
    right_click_menu_def = [[], ['About', 'Exit']]
    
    # Define layouts
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
                     [sg.Text('Enter CSV filename to save cointegrated pairs')],
                     [sg.Input(key='filename_to_cointegration')],
                     [sg.Button('Check Cointegration')]]
    
    plot_layout = [[sg.Text('Plot trends and save for backtesting')],
                   [sg.Text('Enter the first symbol:')],
                   [sg.Input(key='symbol1')],
                   [sg.Text('Enter the second symbol:')],
                   [sg.Input(key='symbol2')],
                   [sg.Text('Enter JSON filename with pairs from the previous window')],
                   [sg.Button('Browse File')],
                   [sg.Text('Enter CSV filename to save data for backtest of previous symbols')],
                   [sg.Input(key='filename_backtest')],               
                   [sg.Button('Plot')],
                   [sg.Frame('Fast Data Preparing', [
                       [sg.Text('Run data preparation for backtest with top 10 pairs of cointegration file')],
                       [sg.Text('CSV File with cointegration data')],
                       [sg.Button('Browse cointegration CSV')],
                       [sg.Text('CSV filename for save top 10 pairs')],
                       [sg.Input(key='csv_top10')],
                       [sg.Button('Fast Backtest')]
                       ])
                    ]
                   ]
    
    csv_preview_layout = [[sg.Text('Browse CSV file you want to preview')],
                          [sg.Button('Browse CSV')]]

    backtest_layout = [[sg.Text('Browse CSV file from previous step to perform backtest')],
                       [sg.Button('Browse file')],
                       [sg.Button('Update data')],
                       [sg.Text('Enter Z-Score Threshold')],
                       [sg.Input(key='z_score_threshold')],
                       [sg.Text('Enter Trading Capital')],
                       [sg.Input(key='trading_capital')],
                       [sg.Text('Enter Rebate')],
                       [sg.Input(key='rebate')],
                       [sg.Text('Enter Slippage Assumption')],
                       [sg.Input(key='slippage_assumption')],
                       [sg.Text('Long when Z-Score Negative')],
                       [sg.Combo(values=('Sym_1', 'Sym_2'), default_value='Sym_1', readonly=True, k='symbol_option')],
                       [sg.Text('Many opens')],
                       [sg.Combo(values=('No', 'Yes'), default_value='No', readonly=True, k='many_opens_option')],
                       [sg.Button('Update values')],
                       [sg.Button('Run Backtest')]]
    
    # Set layouts
    layout = [[sg.Text('Statistical Arbitrage -  Strategy', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
    
    layout += [[sg.TabGroup([[  sg.Tab('Output', logging_layout),
                                sg.Tab('Get Symbols', get_symbols_layout),
                                sg.Tab('Cointegration Check', cointegration_layout),
                                sg.Tab('Plot', plot_layout),
                                sg.Tab('Preview CSV', csv_preview_layout),
                                sg.Tab('Backtest', backtest_layout)]], 
                            key='-TAB GROUP-', expand_x=True, expand_y=True), ]]
    
    layout[-1].append(sg.Sizegrip())
    
    # Set window
    window = sg.Window('Statistical Arbitrage - ByBit', layout, right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True)#, keep_on_top=True)
    
    window.set_min_size(window.size)
    return window

def main():
    # Get window
    window = make_window()
    
    while True: 
        # Read values
        event, values = window.read()
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            pass
        if event in (None, 'Exit'):
            break                     
        elif event == 'About':
            sg.popup('Statistical Arbitrage - ByBit',
                     '- Get tradeable symbols',
                     '- Store symbols in JSON',
                     '- Check for cointegration',
                     '- Crete a file with cointegration data for backtesting', keep_on_top=True) 
        elif event == 'Get Symbols':
            try:
                print(style.GREEN)
                print('Getting symbols...')
                print(style.WHITE)  
                # Get tradeable symbols
                symbols_response = get_tradeable_symbols()
                file_name = values['filename_symbols']
                
                print(style.GREEN)
                print('Constructing and saving data price to JSON...')
                print(style.WHITE) 
                # Store prices in JSON file
                if len(symbols_response) > 0:
                    store_price_history(symbols_response, file_name)
                else:
                    print(style.RED)
                    print(f'Found {len(symbols_response)} tradeable items')
                    print(style.WHITE)
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass
        elif event == 'Browse File':
            file_from = sg.popup_get_file('Choose your file', no_window=True, file_types=(('JSON Files','*.json'),)) 
        elif event == 'Browse File1':
            file_from = sg.popup_get_file('Choose your file', no_window=True, file_types=(('JSON Files','*.json'),))
        elif event == 'Browse cointegration CSV':
            csv_coint = sg.popup_get_file('Choose your file', no_window=True, file_types=(('CSV Files','*.csv'),))
        elif event == 'Browse CSV':
            try:
                table_csv()        
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass
        elif event == 'Browse file':
            file_csv = sg.popup_get_file('Choose your file', no_window=True, file_types=(('CSV Files','*.csv'),))       
        elif event == 'Check Cointegration':
            try:
                print(style.BLUE)
                print(f'Calculating cointegration for data in file {str(file_from)}...')
                print(style.WHITE) 
                
                file_name = values['filename_to_cointegration']
                
                # Open price list for cointegration review
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
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass  
        elif event == 'Plot':
            try:
                # Plot trends for backtesting
                print(style.BLUE)
                print('Plotting trends...')
                print(style.WHITE)
                symbol1 = values['symbol1']
                symbol2 = values['symbol2']
                file_name = values['filename_backtest']
                
                print(style.BLUE)
                print(f'Plotting trends for {symbol1}-{symbol2}')
                print(style.WHITE)
                # Open JSON file with price data
                with open(file_from, 'r') as file:
                    price_data = json.load(file)
                    if len(price_data) > 0:
                        plot(symbol1, symbol2, price_data, file_name)   
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass     
        elif event == 'Fast Backtest':
            try:
                df_coint = pd.read_csv(csv_coint)
                df_coint['symbol'] = df_coint['symbol'].astype('string')
                df_coint['sec_symbol'] = df_coint['sec_symbol'].astype('string')
                
                print(style.BLUE)
                print('Preparing data for backtesting with top 10 pairs')
                print(style.WHITE)
                
                best = df_coint.head(10)
                filename_top10 = values['csv_top10']
                best.to_csv(filename_top10)
                
                for i in range(1, 10):
                    
                    symbol1_row = best.iloc[i, 1]
                    symbol2_row = best.iloc[i, 2]                    
                    
                    print(style.BLUE)
                    print('Plotting trends...')
                    print(style.WHITE)
                    
                    print(style.BLUE)
                    print(f'Plotting trends for {symbol1_row}-{symbol2_row}')
                    print(style.WHITE)
                    
                    # Open JSON file with price data
                    with open(file_from, 'r') as file:
                        price_data = json.load(file)
                        if len(price_data) > 0:
                            save_data_backtest(symbol1_row, symbol2_row, price_data, f'{symbol1_row}_{symbol2_row}.csv')                     

                print(style.BLUE)
                print('Fast backtest finished...')
                print(style.WHITE)
                    
            except Exception as e:     
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass                              
        elif event == 'Update data':
            # Update data in backtest tab
            try:
                update_data(file_csv)
                print(style.GREEN)
                print('Data updated - ' + file_csv)
                print(style.WHITE)
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass
        elif event == 'Update values':
            # Update values in backtest tab
            zscore_threshold, trading_capital, rebate, slippage_assumption, long_when_zscore_negative, many_opens = values['z_score_threshold'], values['trading_capital'], values['rebate'], values['slippage_assumption'], values['symbol_option'], values['many_opens_option']
            update_values(zscore_threshold, trading_capital, rebate, slippage_assumption, long_when_zscore_negative, many_opens)
            print(style.GREEN)
            print('Values updated')
            print(style.WHITE)
        elif event == 'Run Backtest':
            try:
                table_backtest()
            except Exception as e:
                print(style.RED)
                print(f'Something went wrong, please try again {e}')
                print(style.WHITE)
                pass
            
    window.close()
    exit(0)              
     
# Entry point
if __name__ == '__main__':
    main()