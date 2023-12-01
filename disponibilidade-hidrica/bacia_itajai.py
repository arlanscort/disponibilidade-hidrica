import sys
sys.path.append('C:\\Users\\arlan\\git\\hidrologia\\codigos')
import aquisicao_ana
import pandas as pd 
import geopandas as gpd


# df = aquisicao_ana.hidro_inventario()

# df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].astype(float)
# df = df.query('(Latitude > -28.0) and (Latitude < -25.8) and (Longitude > -50.8) and (Longitude < -48.7)')

# df_flu = df.query('TipoEstacao == "1"')
# df_flu.to_csv('estacoes_area_flu.csv', index=False)
# df_plu = df.query('TipoEstacao == "2"')
# df_plu.to_csv('estacoes_area_plu.csv', index=False)

# df = df.loc[df['PeriodoDescLiquidaInicio'].notnull()]
# df.to_csv('estacoes_area_flu_com_dados.csv', index=False)


df = pd.read_csv('estacoes_area_flu_com_dados.csv')

for codigo in df['Codigo']:
    print(codigo)
    sr_temp = aquisicao_ana.hidro_serie_historica(codigo)
    break
    if sr_temp is not None:
        sr_temp.to_csv(f'series-historicas/{codigo}.csv')
    