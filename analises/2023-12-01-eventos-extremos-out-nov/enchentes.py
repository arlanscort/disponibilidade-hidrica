import pandas as pd
import plotly.express as px

df = pd.read_csv('enchentes_registradas_alertablu.txt', delimiter='\t', decimal=',')
df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '/' + df['Data'], format='%Y/%d/%m')
df = df[['Data', 'Cota']]

ocorrencias = df['Cota'].groupby(df['Data'].dt.year).count().rename('Ocorrências')
maximos = df['Cota'].groupby(df['Data'].dt.year).max().rename('Máximos')
df = pd.concat([ocorrencias,  maximos], axis=1)
df.index.name = 'Ano'
anos_completos = pd.DataFrame({'Ano': range(df.index.min(), df.index.max() + 1)})
df = pd.merge(anos_completos, df, on='Ano', how='left').fillna(0)

fig = px.bar(df, x='Ano', y='Ocorrências', title='Ocorrências de Enchentes por Ano (1852 - 2023)', labels={'Ocorrencias': 'N.º de Ocorrências', 'Ano': 'Ano'})
fig.update_layout(title_x=0.5, title_y=0.9, title_xanchor='center', title_yanchor='top')
fig.show()

fig = px.bar(df, x='Ano', y='Máximos', title='Nível Máximo Atingido nas Enchentes por Ano (1852 - 2023)', labels={'Máximos': 'Nível máximo anual', 'Ano': 'Ano'})
fig.update_layout(title_x=0.5, title_y=0.9, title_xanchor='center', title_yanchor='top')
fig.show()