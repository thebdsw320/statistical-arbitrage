import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from config_strategy import z_score_window

# Calculate Z-Score
def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window=1).mean()
    
    df['ZSCORE'] = (x - mean) / std
    
    return df['ZSCORE'].astype(float).values

# Calculate spread
def calculate_spread(series1, series2, hedge_ratio):
    spread = pd.Series(series1) - (pd.Series(series2) * hedge_ratio)
    
    return spread

# Calculate co-integration
def calculate_cointegration(series1, series2):
    coint_flag = 0
    coint_res = coint(series1, series2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series1, series2, hedge_ratio)
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    
    if (p_value < 0.05) and (coint_t < critical_value):
        coint_flag = 1
    return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2), zero_crossings)

# Put close prices into a list
def extract_close_prices(price_data):
    close_prices = []
    
    for price_values in price_data:
        if math.isnan(price_values['close']):
            return []
        
        close_prices.append(price_values['close'])
    
    return close_prices

# Calculate cointgrated pairs
def get_cointegrated_pairs(price_data, file_name):
    
    # Loop trough coins and check for co-integration
    coint_pair_list = []
    included_list = []
    
    for symbol in price_data.keys():
        # Check each coin against the first
        for sec_symbol in price_data.keys():
            if sec_symbol != symbol:
                # Get unique combination
                sorted_chars = sorted(symbol + sec_symbol)
                unique = ''.join(sorted_chars)
                
                if unique in included_list:
                    continue
                
                # Get close prices
                series1 = extract_close_prices(price_data[symbol])
                series2 = extract_close_prices(price_data[sec_symbol])
                
                # Check for cointegration and add cointegrated pair
                coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(series1, series2)
                
                if coint_flag == 1:
                    included_list.append(unique)
                    coint_pair_list.append({
                        'symbol': symbol,
                        'sec_symbol': sec_symbol,
                        'p_value': p_value,
                        't_value': t_value,
                        'c_value': c_value,
                        'hedge_ratio': hedge_ratio,
                        'zero_crossings': zero_crossings
                    })
    
    # Output results
    df_coint = pd.DataFrame(coint_pair_list)
    df_coint = df_coint.sort_values('zero_crossings', ascending=False)
    df_coint.to_csv(file_name)
    
    return df_coint