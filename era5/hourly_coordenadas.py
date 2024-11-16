# Para visualizar a grade

import xarray as xr
import pandas as pd
from itertools import product

ds = xr.open_dataset('hourly_2023.grib', engine='cfgrib')
xy = list(product(ds.longitude.values, ds.latitude.values))
df = pd.DataFrame(xy, columns=['x', 'y'])
df.to_csv('hourly_xy.csv', index=False)
