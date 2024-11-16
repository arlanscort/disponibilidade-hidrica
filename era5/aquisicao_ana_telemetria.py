import requests
import xml.etree.ElementTree as ET
import pandas as pd

import requests


def inventario_telemetricas(statusEstacoes = "", origem = ""):
    # statusEstacoes: 0-Ativo ou 1-Manutenção
    # Origem: 0-Todas, 1-ANA/INPE, 2-ANA/SIVAM, 3-RES_CONJ_03, 4-CotaOnline, 5-Projetos Especiais
    params = {
        "statusEstacoes" : statusEstacoes,
        "origem" : origem,
    }
    resposta = requests.get("https://telemetriaws1.ana.gov.br/ServiceANA.asmx/ListaEstacoesTelemetricas", params=params)  
    xml_string = resposta.content.decode('utf-8')
    raiz = ET.fromstring(xml_string)
    tabelas = raiz.findall('.//Table')
    df = pd.DataFrame()
    dados = []
    for tabela in tabelas:
        linha = {}
        for elemento in tabela:
            linha[elemento.tag] = elemento.text
        dados.append(linha)

    return pd.DataFrame(dados)


def dados(codEstacao, dataInicio, dataFim):
    params = {
        "codEstacao" : codEstacao, 
        "dataInicio" : dataInicio,
        "dataFim" : dataFim,
    }
    resposta = requests.get("https://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos", params=params)
    xml_string = resposta.content.decode('utf-8')
    raiz = ET.fromstring(xml_string)
    dados = []
    for dado in raiz.findall('.//DadosHidrometereologicos'):
        DataHora = dado.find('DataHora').text
        Vazao = dado.find('Vazao').text
        Nivel = dado.find('Nivel').text
        Chuva = dado.find('Chuva').text
        dados.append([DataHora, Vazao, Nivel, Chuva])
    
    df = pd.DataFrame(dados, columns=['DataHora', 'Vazao', 'Nivel', 'Chuva'])
    df['DataHora'] = pd.to_datetime(df['DataHora'])
    df['Vazao'] = pd.to_numeric(df['Vazao'])
    df['Nivel'] = pd.to_numeric(df['Nivel'])
    df['Chuva'] = pd.to_numeric(df['Chuva'])
    df = df.set_index('DataHora').sort_index()

    return df


if __name__ == "__main__":
    
    # Exemplo Inventario 
    df = inventario_telemetricas(statusEstacoes = 0)
    df = df.set_index('CodEstacao')
    df.to_csv('inventario_telemetricas.csv')
    
    # Exemplo Fazendinha
    codEstacao = 65010000
    df = dados(codEstacao, '2010-01-01', '2023-01-01')
    df.to_csv(f'{codEstacao}.csv')