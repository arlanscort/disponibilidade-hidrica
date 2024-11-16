import pandas as pd
import matplotlib.pyplot as plt

# Prepara serie observada
df = pd.read_csv('dados_inmet_A817_indaial.csv', sep=';', dtype={'Data':str, 'Hora (UTC)':str}, decimal=',')
df['datahora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora (UTC)'], format='%d/%m/%Y %H%M')
idx = df['datahora'] + pd.Timedelta(1, 'H') # Os dados do C3S sao indexados a esquerda
sr = pd.Series(index=df['datahora'], data=df['Chuva (mm)'].values, name='chuva_controle_inmet')
sr = sr.dropna()
sr = sr.asfreq('H')

# Leitura dos dados de controle do ERA5
df = pd.read_csv('df_controle_era5.csv', index_col='datahora', parse_dates=True)

# Comparativo
df2 = df.join(sr, on='datahora', how='inner')
df2 = df2.loc['2023-09-01':]

