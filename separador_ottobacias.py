'''
Arlan Scortegagna, junho de 2023
'''

import geopandas as gpd
import re
import time

def separador_ottobacias(cobacia, inclui_exutoria=True):
    cobacia = str(cobacia)
    codigo_esq = re.search(r'^.*?(\d*[02468])', cobacia).group(0)
    gdf_temp = gdf.loc[gdf['cobacia'].str.startswith(codigo_esq)]
    cobacias_reg = gdf_temp['cobacia'].str.ljust(len(cobacia), '9')
    if inclui_exutoria is True:
        cobacias_montante = cobacias_reg >= cobacia
    else:
        cobacias_montante = cobacias_reg > cobacia
    gdf_montante = gdf_temp.loc[cobacias_montante]
    
    gdf_dissolved = gdf_montante.dissolve(aggfunc=dict(nuareacont='sum'))
    gdf_dissolved['cobacia'] = cobacia
    return gdf_dissolved[['cobacia', 'nuareacont', 'geometry']]


if __name__ == '__main__':

    # Carregar base
    print('Carregando base ottocodificada...')
    t1 = time.time()
    bbox = (-50.5, -28.0, -48.5, -26.0)
    cols = ['cotrecho', 'cocursodag', 'cobacia', 'nuareacont', 'geometry']
    gdf =  gpd.read_file('bases-ottocodificadas/geoft_bho_2017_area_drenagem.gpkg', bbox=bbox, columns=cols)
    # gdf = gdf[['cotrecho', 'cocursodag', 'cobacia', 'nuareacont', 'geometry']]
    dt1 = time.time() - t1
    print(f'dt = {dt1/60:.2f}')

    # Separar as bacias
    nomes = ['foz_itajai', 'foz_itapocu', 'capt_eta1', 'capt_eta2', 'capt_eta3', 'capt_eta4']
    cobacias = [779611, 7795815, 7796353, 77963591, 779634371, 7795849715]
    dts = []
    for nome, cobacia in zip(nomes, cobacias):
        print(f'\nSeparando {nome}...')
        t = time.time()
        
        gdf_bacia = separador_ottobacias(cobacia, True)
        gdf_bacia.to_file(f'bacias-separadas/{nome}.gpkg', driver='GPKG')
        
        dt = time.time() - t
        dts.append(dt)
        print(f'dt = {dt/60:.2f}')

        break