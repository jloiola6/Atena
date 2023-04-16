import pandas as pd

def foritem(x, lista):
    for i in x:
        lista.append(i)

def localizacao():
    inep = []
    longitude = []
    latitude = []
    

    dados = pd.read_excel('escolas-urbanas-see.xlsx')
    print(dados)
    # filtro = dados['CENSO'] == 12011517
    # dados = dados[filtro]

    x = dados['Latitude'].tolist()
    foritem(x, latitude)
    x = dados['Longitude'].tolist()
    foritem(x, longitude)
    x = dados['inep '].tolist()
    foritem(x, inep)
    

    print('FINALIZADO!!')
    print(len(inep))
    print(len(latitude))
    print(len(longitude))
    
localizacao()
