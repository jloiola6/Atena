import pandas as pd
import mysql.connector


def pesquisar_banco(lista):
    con = mysql.connector.connect(host='localhost', database='secretaria', user='see',password='dtmisee@') 

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()

        tipo_localizacao = []
        escolas = []
        for inep in lista:
            cursor.execute(f'SELECT end.tipo_localizacao, esc.nome_escola FROM see_lotus.administracao_endereco as end join see_lotus.administracao_escola as esc on end.escola_id = esc.id where esc.cod_inep= {inep};')
            print(cursor.fetchall())
            try:
                tipo = cursor.fetchall()[0][0]
                escola = cursor.fetchall()[0][1]
            except:
                tipo = 'Não Informado'
                escola = cursor.fetchall()[0][1]
            print("inep: ", inep, tipo), escola
            tipo_localizacao.append(tipo)
            escolas.append(escola)

    #         con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")
    
    return (tipo_localizacao, escolas)


def foritem(x, lista, campo= None):
    for i in x:
        if campo:
            lista.append(i)
        else:
            if i not in lista:
                lista.append(i)

def alunos():
    municipio = []
    escola = []
    inep = []

    dados = pd.read_excel('dados.xlsx', sheet_name= 'dados')
    x = dados['MUNICÍPIO'].tolist()
    foritem(x, municipio, True)
    x = dados['ESCOLA'].tolist()
    foritem(x, escola)
    x = dados['CENSO'].tolist()
    foritem(x, inep)

    print('FINALIZADO!!')


    dados = pesquisar_banco(inep)

    print(len(inep))
    print(len(dados[1]))
    print(len(dados[0]))
    print(len(municipio))

    dicionario = {'CENSO': inep, 'ESCOLA': escola, 'TIPO LOCALIZAÇÃO': tipo_localizacao, 'MUNICÍPIO': municipio}

    df = pd.DataFrame(data=dicionario)
    df.to_excel('Escolas.xls')
alunos()