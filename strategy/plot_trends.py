from cointegration import calculate_cointegration, calculate_spread, calculate_zscore, extract_close_prices
import pandas as pd
import matplotlib.pyplot as plt

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
     
# Plot price and trends
def plot(symbol1, symbol2, price_data, filename):
    # Extract close prices
    prices1 = extract_close_prices(price_data[symbol1])
    prices2 = extract_close_prices(price_data[symbol2])
    
    # Get spread and z-score
    coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossing = calculate_cointegration(prices1, prices2)
    spread = calculate_spread(prices1, prices2, hedge_ratio)
    zscore = calculate_zscore(spread)
    
    # Calculate percentage changes 
    df = pd.DataFrame(columns=[symbol1, symbol2])
    df[symbol1] = prices1
    df[symbol2] = prices2
    df[f'{symbol1}_pct'] = df[symbol1] / prices1[0]
    df[f'{symbol2}_pct'] = df[symbol2] / prices2[0]
    
    series1 = df[f'{symbol1}_pct'].astype(float).values
    series2 = df[f'{symbol2}_pct'].astype(float).values
    
    # Save results for backtesting
    df2 = pd.DataFrame()
    df2[symbol1] = prices1
    df2[symbol2] = prices2
    df2['spread'] = spread
    df2['zscore'] = zscore
    
    df2 = df2.dropna()
    
    df2.to_csv(filename)
    
    # Plot chart
    plt.subplot(3, 1, 1)
    plt.plot(series1)
    plt.plot(series2)
    plt.legend([symbol1, symbol2], loc='lower right')
    plt.title(f'Price - {symbol1} vs {symbol2}')

    plt.subplot(3, 1, 2)
    plt.plot(spread)
    plt.title('Spread')
    
    plt.subplot(3, 1, 3)
    plt.plot(zscore)
    plt.title('Z-Score')
    
    print(style.GREEN)
    print('Plotting...')
    print(style.WHITE)

    plt.subplots_adjust(left=0.124,
                        bottom=0.057, 
                        right=0.9, 
                        top=0.945, 
                        wspace=0.614, 
                        hspace=0.302)
    plt.show(block=False)
    # plt.close()
    
    # print(style.GREEN)
    # print('Closing plot...')
    # print(style.WHITE)

    #plt.savefig(f'{symbol1}-{symbol2}.png', dpi=1200)

def save_data_backtest(symbol1, symbol2, price_data, filename):
    # Extract close prices
    prices1 = extract_close_prices(price_data[symbol1])
    prices2 = extract_close_prices(price_data[symbol2])
    
    # Get spread and z-score
    coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossing = calculate_cointegration(prices1, prices2)
    spread = calculate_spread(prices1, prices2, hedge_ratio)
    zscore = calculate_zscore(spread)
    
    # Calculate percentage changes 
    df = pd.DataFrame(columns=[symbol1, symbol2])
    df[symbol1] = prices1
    df[symbol2] = prices2
    df[f'{symbol1}_pct'] = df[symbol1] / prices1[0]
    df[f'{symbol2}_pct'] = df[symbol2] / prices2[0]
    
    series1 = df[f'{symbol1}_pct'].astype(float).values
    series2 = df[f'{symbol2}_pct'].astype(float).values
    
    # Save results for backtesting
    df2 = pd.DataFrame()
    df2[symbol1] = prices1
    df2[symbol2] = prices2
    df2['spread'] = spread
    df2['zscore'] = zscore
    
    df2 = df2.dropna()
    
    df2.to_csv(filename)