import pandas as pd
import mysql.connector


def salvarBanco(id_escola, cod_inep, cod_turmalina, nome_escola, cnpj, dependencia_adm, tipificacao):
    con = mysql.connector.connect(host='localhost',database='secretaria',user='see',password='dtmisee@', auth_plugin='mysql_native_password') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(id_escola)):
            cursor.execute(f"INSERT INTO administracao_escola (cod_inep, cod_turmalina, nome_escola, cnpj, dependencia_adm) values ('{cod_inep[i]}', '{cod_turmalina[i]}', '{nome_escola[i]}', ' ', '{dependencia_adm[i]}');")
            print("Adicionando no id: ", id_escola[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def escolas():
    id_escola = []
    cod_inep = []
    cod_turmalina = []
    nome_escola = []
    cnpj = []
    dependencia_adm = []
    tipificacao = []

    dados = pd.read_excel('escolas.xlsx')
    x = dados['id'].tolist()
    foritem(x, id_escola)
    x = dados['cod_inep'].tolist()
    foritem(x, cod_inep)
    x = dados['cod_turmalina'].tolist()
    foritem(x, cod_turmalina)
    x = dados['nome_escola'].tolist()
    foritem(x, nome_escola)
    x = dados['cnpj'].tolist()
    foritem(x, cnpj)
    x = dados['dependecia_adm'].tolist()
    foritem(x, dependencia_adm)
    x = dados['tipificacao'].tolist()
    foritem(x, tipificacao)

    print('FINALIZADO!!')
    salvarBanco(id_escola, cod_inep, cod_turmalina, nome_escola, cnpj, dependencia_adm, tipificacao)

escolas()