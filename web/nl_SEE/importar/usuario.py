import pandas as pd
import mysql.connector


def salvarBanco(id_usuario, nome, login, cpf, senha, email, status):
    con = mysql.connector.connect(host='localhost',database='secretaria',user='see',password='dtmisee@', auth_plugin='mysql_native_password') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(id_usuario)):
            cursor.execute(f"INSERT INTO usuario_usuarios (id, nome, login, cpf, senha, email, status) values ({id_usuario[i]}, '{nome[i]}', '{login[i]}', '{cpf[i]}', '{senha[i]}', '{email[i]}', '{status[i]}');")
            print("Adicionando no id: ", id_usuario[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def usuarios():
    id_usuario = []
    nome = []
    login = []
    cpf = []
    senha = []
    email = []
    status = []

    dados = pd.read_excel('usuarios.xlsx')
    x = dados['id'].tolist()
    foritem(x, id_usuario)
    x = dados['nome'].tolist()
    foritem(x, nome)
    x = dados['login'].tolist()
    foritem(x, login)
    x = dados['cpf'].tolist()
    foritem(x, cpf)
    x = dados['senha'].tolist()
    foritem(x, senha)
    x = dados['email'].tolist()
    foritem(x, email)
    x = dados['status'].tolist()
    foritem(x, status)

    print('FINALIZADO!!')
    salvarBanco(id_usuario, nome, login, cpf, senha, email, status)

usuarios()