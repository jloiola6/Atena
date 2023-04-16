import pandas as pd
import mysql.connector


def salvarBanco(tipo_contato, contato, endereco_id, descricao):
    con = mysql.connector.connect(host='localhost',database='secretaria',user='see',password='dtmisee@', auth_plugin='mysql_native_password') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(endereco_id)):
            cursor.execute(f"INSERT INTO administracao_contato (tipo_contato, contato, endereco_id, descricao) values ('{tipo_contato[i]}', '{contato[i]}', '{endereco_id[i]}', '{descricao[i]}');")
            print("Adicionando no id: ", endereco_id[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def contatos():
    tipo_contato = []
    contato = []
    endereco_id = []
    descricao = []

    dados = pd.read_excel('contatos.xlsx')
    x = dados['tipo_contato'].tolist()
    foritem(x, tipo_contato)
    x = dados['contato'].tolist()
    foritem(x, contato)
    x = dados['endereco_id'].tolist()
    foritem(x, endereco_id)
    x = dados['descricao'].tolist()
    foritem(x, descricao)

    print('FINALIZADO!!')
    salvarBanco(tipo_contato, contato, endereco_id, descricao)

contatos()