import pandas as pd
import mysql.connector


def salvarBanco(nome, tipo):
    con = mysql.connector.connect(host='localhost',database='secretaria',user='see',password='dtmisee@', auth_plugin='mysql_native_password') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        for i in range(len(nome)):
            cursor.execute(f'INSERT INTO administracao_aluno (nome, nascimento, cpf, nome_turma, sexo, inep) values ("{nome[i]}", "{nascimento[i]}", "{cpf[i]}", "{nome_turma[i]}", "{sexo[i]}", "{inep[i]}");')
            print("Adicionando nom: ", nome[i])
            con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


def foritem(x, lista):
    for i in x:
        lista.append(i)

def funcoes():
    nome = []
    tipo = []
    
    dados = pd.read_excel('funcoes.xlsx')
    x = dados['nome'].tolist()
    foritem(x, nome)
    x = dados[' tipo'].tolist()
    foritem(x, tipo)

    print('FINALIZADO!!')


    salvarBanco(nome, tipo)
funcoes()