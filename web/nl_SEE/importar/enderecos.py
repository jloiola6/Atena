import pandas as pd
import mysql.connector


def salvarBanco(municipio, regiao, zoneamento, rua, numero, bairro, complemento, tipo_localizacao, escola_id, latitude, longitude, tipo, cep, localizacao_diferenciada, uf):
    con = mysql.connector.connect(host='localhost',database='secretaria',user='see',password='dtmisee@', auth_plugin='mysql_native_password') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(escola_id)):
            cursor.execute(f"INSERT INTO administracao_endereco (municipio, regiao, zoneamento, rua, numero, bairro, complemento, tipo_localizacao, escola_id, latitude, longitude, tipo, cep, localizacao_diferenciada, uf) values ('{municipio[i]}', '{regiao[i]}', '{zoneamento[i]}', '{rua[i]}', '{numero[i]}', '{bairro[i]}', '{complemento[i]}', '{tipo_localizacao[i]}', '{escola_id[i]}', '{latitude[i]}', '{longitude[i]}', '{tipo[i]}', '{cep[i]}', '{localizacao_diferenciada[i]}', '{uf[i]}');")
            print("Adicionando no id: ", escola_id[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def enderecos():
    escola_id = []
    municipio = []
    regiao = []
    zoneamento = []
    rua = []
    numero = []
    bairro = []
    complemento = []
    tipo_localizacao = []
    latitude = []
    longitude = []
    tipo = []
    cep = []
    localizacao_diferenciada = []
    uf = []

    dados = pd.read_excel('enderecos.xlsx')
    x = dados['escola_id'].tolist()
    foritem(x, escola_id)
    x = dados['municipio'].tolist()
    foritem(x, municipio)
    x = dados['regiao'].tolist()
    foritem(x, regiao)
    x = dados['zoneamento'].tolist()
    foritem(x, zoneamento)
    x = dados['rua'].tolist()
    foritem(x, rua)
    x = dados['numero'].tolist()
    foritem(x, numero)
    x = dados['bairro'].tolist()
    foritem(x, bairro)
    x = dados['complemento'].tolist()
    foritem(x, complemento)
    x = dados['tipo_localizacao'].tolist()
    foritem(x, tipo_localizacao)
    x = dados['latitude'].tolist()
    foritem(x, latitude)
    x = dados['longitude'].tolist()
    foritem(x, longitude)
    x = dados['tipo'].tolist()
    foritem(x, tipo)
    x = dados['cep'].tolist()
    foritem(x, cep)
    x = dados['localizacao_diferenciada'].tolist()
    foritem(x, localizacao_diferenciada)
    x = dados['uf'].tolist()
    foritem(x, uf)

    print('FINALIZADO!!')
    salvarBanco(municipio, regiao, zoneamento, rua, numero, bairro, complemento, tipo_localizacao, escola_id, latitude, longitude, tipo, cep, localizacao_diferenciada, uf)

enderecos()