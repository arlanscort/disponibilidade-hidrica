import xarray as xr
import pandas as pd

ds = xr.open_dataset('hourly_2023.grib', engine='cfgrib', indexpath=None)
da = ds['tp']

# Estacao Inmet - A817 - Indaial (SC)
y = -26.91
x = -49.27

# Pontos proximos da grade
grade = [[-49.50, -26.75], [-49.25, -26.75], [-49.25, -27], [-49.5, -27]]
df_final = []
for ponto in grade:
    da_xy = da.sel(longitude=ponto[0], latitude=ponto[1], method='nearest')
    
    pick_lon = da_xy.longitude.values
    pick_lat = da_xy.latitude.values 
    pick_name = f'{pick_lon:.2f},{pick_lat:.2f}'

    df = da_xy.to_dataframe()
    sr = pd.Series(index=df['valid_time'].values, data=df['tp'].values, name=pick_name)
    sr = sr*1000
    sr = sr.dropna()
    sr = sr.asfreq('H')

    print(pick_name, "\n")

    df_final.append(sr)

df_final = pd.concat(df_final, axis=1)
df_final.index.name = 'datahora'
df_final.to_csv('df_controle_era5.csv')