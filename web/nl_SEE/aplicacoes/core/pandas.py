import pandas as pd
from aplicacoes.usuario.models import Usuarios

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

    dados = pd.read_excel('nl_SEE/aplicacoes/core/usuarios.xlsx')
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

    for item in range(len(id)):
        banco = Usuarios()
        banco.id = id_usuario[item]
        banco.nome = nome[item]
        banco.login = login[item]
        banco.cpf = cpf[item]
        banco.senha = senha[item]
        banco.email = email[item]
        banco.status = status[item]
        banco.save()

    print('FINALIZADO!!')