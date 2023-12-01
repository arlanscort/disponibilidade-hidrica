'''
Arlan Scortegagna, junho de 2023
'''

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import re
import json
import time

def hidro_inventario(nmEstado=''):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'
    params = {
        'nmEstado': nmEstado,
        'codEstDE': '',
        'codEstATE': '',
        'tpEst': '',
        'nmEst': '',
        'nmRio': '',
        'codSubBacia': '',
        'codBacia': '',
        'nmMunicipio': '',
        'sgResp': '',
        'sgOper': '',
        'telemetrica': ''
    }
    response = requests.get(url, params=params)
    xml_data = response.content
    root = ET.fromstring(xml_data)
    df = []
    for dados_estacao in root.findall('.//Table'):
        tags = []
        vals = []  
        for i in dados_estacao:
            tags.append(i.tag)
            vals.append(i.text)
        df_temp = pd.DataFrame(index=tags, data=vals).T
        df.append(df_temp)
    df = pd.concat(df)
    df = df.drop_duplicates()
    return df

def hidro_serie_historica(codEstacao, tipoDados=3):
    url = 'https://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica'
    params = {
        'codEstacao': codEstacao,
        'dataInicio': '',
        'dataFim': '',
        'tipoDados': tipoDados,
        'nivelConsistencia': '',
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    dados = []
    if len(root.findall('.//SerieHistorica')) == 0:
        return None
    for dados_mes in root.iter('SerieHistorica'):
        serie_mes = {'vazao':{}, 'status':{}}
        for elemento in dados_mes.iter():
            tag = elemento.tag 
            if tag == 'NivelConsistencia':
                NivelConsistencia = elemento.text
            elif tag == 'DataHora':
                DataHora = elemento.text
            elif re.match(r'Vazao(\d{2})$', tag):
                k = re.match(r'Vazao(\d{2})$', tag).group(1)
                serie_mes['vazao'][k] = elemento.text
            elif re.match(r'Vazao(\d{2})Status$', tag):
                k = re.match(r'Vazao(\d{2})Status$', tag).group(1)
                serie_mes['status'][k] = elemento.text
        df_temp = pd.DataFrame(serie_mes).reset_index()    
        df_temp['nivel_consistencia'] = NivelConsistencia
        periodo = pd.to_datetime(DataHora).to_period('M')
        idx = pd.date_range(periodo.start_time, periodo.end_time, freq='D')
        idx_dias = [f'{i:02d}' for i in idx.day]
        df_ideal = pd.DataFrame({'data':idx, 'index':idx_dias})
        df_ideal = df_ideal.merge(df_temp, left_on='index', right_on='index')
        dados.append(df_ideal[['data', 'vazao', 'status', 'nivel_consistencia']])
    df = pd.concat(dados).set_index('data').sort_index()
    
    return df
    
    df['vazao'] = df['vazao'].astype(float)
    df['nivel_consistencia'] = df['nivel_consistencia'].astype(int)
    df['status'] = df['status'].astype(int)
    return df

if __name__ == '__main__':

    df = hidro_inventario()