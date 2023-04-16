import pandas as pd
import mysql.connector


def salvarBanco(nome, nascimento, cpf, sexo, nome_turma, inep):
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

def alunos():
    nome = []
    nascimento = []
    sexo = []
    cpf = []
    nome_turma = []
    inep = []

    dados = pd.read_excel('Alunos.xlsx')
    # filtro = dados['CENSO'] == 12011517
    # dados = dados[filtro]

    x = dados['NOME'].tolist()
    foritem(x, nome)
    x = dados[' NASCIMENTO'].tolist()
    foritem(x, nascimento)
    x = dados['SEXO'].tolist()
    foritem(x, sexo)
    x = dados['NU CPF'].tolist()
    foritem(x, cpf)
    x = dados['TURMA'].tolist()
    foritem(x, nome_turma)
    x = dados['CENSO'].tolist()
    foritem(x, inep)

    print('FINALIZADO!!')


    salvarBanco(nome, nascimento, cpf, sexo, nome_turma, inep)
alunos()