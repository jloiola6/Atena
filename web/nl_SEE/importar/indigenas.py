from threading import local
import pandas as pd
import mysql.connector


def salvarBanco(inep, localizacao, aldeia, etnia):
    con = mysql.connector.connect(host='localhost', database='secretaria', user='see',password='dtmisee@') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(inep)):
            cursor.execute(f'INSERT INTO administracao_detalhes_indigena (inep, localizacao, aldeia, etnia) values ("{inep[i]}", "{localizacao[i]}", "{aldeia[i]}", "{etnia[i]}");')
            print("Adicionando nom: ", inep[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def alunos():
    inep = []
    localizacao = []
    aldeia = []
    etnia = []
    dados = pd.read_excel('indigenas.xlsx')

    x = dados['INEP'].tolist()
    foritem(x, inep)
    x = dados['Localizacao'].tolist()
    foritem(x, localizacao)
    x = dados['Aldeia'].tolist()
    foritem(x, aldeia)
    x = dados['Etnia'].tolist()
    foritem(x, etnia)

    print('FINALIZADO!!')


    salvarBanco(inep, localizacao, aldeia, etnia)
alunos()