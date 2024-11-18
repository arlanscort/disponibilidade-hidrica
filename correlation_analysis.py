import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

def cross_correlation(df, var1, var2, max_lag):
    correlations = []
    lags = range(-max_lag, max_lag+1, 1)
    for lag in lags:
        shifted_series2 = df[var2].shift(lag)
        correlation = df[var1].corr(shifted_series2)
        correlations.append(correlation)

    return lags, correlations

if __name__ == '__main__':
    df = df = pd.read_csv('BasinObs_jaguari_buenopolis.csv', parse_dates=['datetime'], index_col=0)
    var1 = 'q_down'
    var2 = 'q_up'
    maxlag = 10
    lags, correlations = cross_correlation(df, var1, var2, maxlag)

# Plotar as correlações cruzadas
plt.figure(figsize=(10, 5))
plt.plot(lags, correlations, marker='o')
plt.axvline(0, color='r', linestyle='--')
plt.axhline(0.2, color='r', linestyle='--')
plt.xlabel('Lag')
plt.xticks(np.arange(min(lags), max(lags)+1, 1))
plt.ylabel('Correlation')
plt.title(f'Cross-correlation between {var1} and {var2}')
plt.legend()
plt.show()