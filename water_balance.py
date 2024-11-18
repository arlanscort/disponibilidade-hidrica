import pandas as pd

df = pd.read_csv('BasinObs.csv', parse_dates=['DatesR'], index_col='DatesR')

df_month = df.resample('M').sum()
df_annual = df.resample('A-JAN').sum()
df_annual['%'] = df_annual['Qmm']/df_annual['P']