import pandas as pd

from .models import *
from aplicacoes.administracao.models import Turmas, Etapa, Etapa_escola, Escola, Endereco, Aluno, Aluno_turma
from aplicacoes.core.uploads import handle_uploaded_file


def cadastrar_aluno(turma, lista_nome_aluno, lista_cod_inep, lista_sexo, lista_nome_pai, lista_nome_mae, lista_nascimento, lista_cor, lista_endereco, lista_transporte, lista_nome_social, lista_deficiencia, lista_telefone, lista_celular, lista_email, lista_nome_responsavel, lista_responsavel_telefone, lista_cpf, lista_bolsa_familia, lista_ra, lista_data_matricula, lista_situacao, lista_data_encerramento):
    # if not Aluno.objects.filter(turma= turma, nome= lista_nome_aluno).exists():
    #     aluno = Aluno()
    # else:
    #     aluno = Aluno.objects.get(turma= turma, nome= lista_nome_aluno)

    lista_cpf = str(lista_cpf)
    lista_cod_inep = str(lista_cod_inep)
    if Aluno.objects.filter(cpf= lista_cpf).exists() and lista_cpf != 'nan':
        aluno = Aluno.objects.filter(cpf= lista_cpf).last()
    elif Aluno.objects.filter(cod_inep= lista_cod_inep).exists() and lista_cod_inep != 'nan':
        aluno = Aluno.objects.filter(cod_inep= lista_cod_inep).last()
    elif Aluno.objects.filter(nome= lista_nome_aluno, nascimento= lista_nascimento).exists():
        aluno = Aluno.objects.filter(nome= lista_nome_aluno, nascimento= lista_nascimento).last()
    else:
        novo_aluno = True
        aluno = Aluno()

        if lista_transporte == 'NÃO UTILIZA':
            lista_transporte = 0
        else:
            lista_transporte = 1

        if lista_bolsa_familia == 'NÃO':
            lista_bolsa_familia = 0
        else:
            lista_bolsa_familia = 1

        # aluno.turma = turma
        aluno.nome = lista_nome_aluno
        aluno.cod_inep = lista_cod_inep
        aluno.sexo = lista_sexo
        aluno.nome_pai = lista_nome_pai
        aluno.nome_mae = lista_nome_mae
        aluno.nascimento = lista_nascimento
        aluno.cor = lista_cor
        aluno.endereco = lista_endereco
        aluno.transporte = lista_transporte
        aluno.nome_social = lista_nome_social
        aluno.deficiencia = lista_deficiencia
        aluno.telefone = lista_telefone
        aluno.celular = lista_celular
        aluno.email = lista_email
        aluno.nome_responsavel = lista_nome_responsavel
        aluno.responsavel_telefone = lista_responsavel_telefone
        aluno.cpf = lista_cpf
        aluno.bolsa_familia = lista_bolsa_familia
        aluno.ra = lista_ra
        aluno.data_matricula = lista_data_matricula
        aluno.situacao = lista_situacao
        aluno.data_encerramento = lista_data_encerramento
        aluno.save()

    if not Aluno_turma.objects.filter(aluno= aluno, turma= turma, status= 1).exists():
        print(f'Novo aLuno: {aluno.nome}')
        for item in Aluno_turma.objects.filter(aluno= aluno, status = 1):
            item.status = 0
            turminha = item.turma
            total_alunos = int(turminha.total_alunos)
            if total_alunos > 0:
                turminha.total_alunos = str(total_alunos - 1)
            turminha.save()
            item.save()

        aluno_turma = Aluno_turma()
        aluno_turma.aluno = aluno
        aluno_turma.turma = turma
        aluno_turma.status = 1
        aluno_turma.save()

        total_alunos = turma.total_alunos
        if total_alunos == '':
            total_alunos = 0
        else:
            total_alunos = int(total_alunos)
        turma.total_alunos = str(total_alunos + 1)
        turma.save()


def atualizar_turmas(dados):
    try:
        #Dados da escola
        cod_inep = dados['CD_CENSO'].to_list()

        #Dados da Turma
        lista_etapa = dados['DC_NIVEL'].to_list()
        lista_ano_serie = dados['DC_ETAPA'].to_list()
        lista_turno = dados['DC_TURNO'].to_list()
        lista_nome = dados['DC_TURMA'].to_list()
        lista_ano_letivo = dados['DC_PERIODO'].to_list()

        #Dados do aluno
        lista_nome_aluno = dados['NM_ALUNO'].to_list()
        lista_cod_inep = dados['CD_INEP'].to_list()
        lista_sexo = dados['TP_SEXO'].to_list()
        lista_nome_pai = dados['NM_PAI'].to_list()
        lista_nome_mae = dados['NM_MAE'].to_list()
        lista_nascimento = dados['DT_NASCIMENTO'].to_list()
        lista_cor = dados['TP_COR'].to_list()
        lista_endereco = dados['ENDERECO'].to_list()
        lista_transporte = dados['TRANSPORTE_ESCOLAR'].to_list()
        lista_nome_social = dados['NM_ALUNO_SOCIAL'].to_list()
        lista_deficiencia = dados['DC_DEFICIENCIA'].to_list()
        lista_telefone = dados['NU_TELEFONE'].to_list()
        lista_celular = dados['NU_TELEFONE_CELULAR'].to_list()
        lista_email = dados['ED_EMAIL_ALUNO'].to_list()
        lista_nome_responsavel = dados['NM_RESPONSAVEL'].to_list()
        lista_responsavel_telefone = dados['NU_RESPONSAVEL_TELEFONE'].to_list()
        lista_cpf = dados['NU_CPF'].to_list()
        lista_bolsa_familia = dados['BOLSA_FAMILIA'].to_list()
        lista_ra = dados['RA'].to_list()
        lista_data_matricula = dados['DATA_MATRICULA'].to_list()
        lista_situacao = dados['SITUACAO_MATRICULA'].to_list()
        lista_data_encerramento = dados['DATA_ENCERRAMENTO'].to_list()     
    except:
        detalhe = Detalhes.objects.get(id= 1)
        detalhe.atualizar_simaed = 0
        detalhe.situacao = 'Ativo'
        detalhe.save()   
    
    detalhe = Detalhes.objects.get(id= 1)
    if detalhe.situacao != 'Ativo':
        for i in range(len(lista_nome)):
            print(f'{i+1} ---- {lista_situacao[i]}')

            try:
                turno = lista_turno[i].replace('MANHÃ', 'Matutino').replace('TARDE', 'Vespertino').replace('INTEGRAL', 'Integral').replace('NOITE', 'Noite')
            except:
                turno = 'Não Definido'
            
            try:
                ano_letivo = lista_ano_letivo[i].split()[-1]
            except:
                continue


            if 'AEE' in lista_nome[i]:
                nome_turma = lista_nome[i]
                endereco = Endereco.objects.get(escola__cod_inep= cod_inep[i], tipo= 'S')

                if 'AEE/AC' == lista_etapa[i]:
                    if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 10).exists():
                            etapa = Etapa.objects.get(id= 10)
                    else:
                        etapa = Etapa_escola()
                        etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                        etapa.etapa = Etapa.objects.get(id= 10)
                        etapa.save()
                        etapa = etapa.etapa
                
                if not Turmas.objects.filter(endereco= endereco, nome= nome_turma, etapa= etapa, ano_letivo= ano_letivo, turno= turno, ano_serie= lista_ano_serie[i]).exists():
                    turma = Turmas()
                    turma.endereco = endereco
                    turma.nome = nome_turma
                    turma.turno = turno
                    turma.etapa = etapa
                    turma.ano_serie = lista_ano_serie[i]
                    turma.ano_letivo = ano_letivo
                    turma.total_alunos = 0
                    turma.save()

            elif 'ANO' in lista_nome[i] or 'SERIE' in lista_nome[i] or 'SÉRIE' in lista_nome[i]:
                nome_turma = lista_nome[i].replace(' ', '').replace('ANO', ' ANO ').replace('SERIE', ' SERIE ').replace('SÉRIE', ' SERIE ').replace('ano', ' ANO ').replace('Ano', ' ANO ')
                endereco = Endereco.objects.get(escola__cod_inep= cod_inep[i], tipo= 'S')

                #EJA
                if 'PRESENCIAL' in lista_etapa[i]:
                    if 'ENSINO FUNDAMENTAL' in lista_etapa[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 7).exists():
                            etapa = Etapa.objects.get(id= 7)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 7)
                            etapa.save()
                            etapa = etapa.etapa

                    elif 'ENSINO MÉDIO' in lista_etapa[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 8).exists():
                            etapa = Etapa.objects.get(id= 8)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 8)
                            etapa.save()
                            etapa = etapa.etapa


                #Ensino Fundamental
                elif 'ENSINO FUNDAMENTAL' in lista_etapa[i]:

                    if '1' in lista_ano_serie[i] or '2' in lista_ano_serie[i] or '3' in lista_ano_serie[i] or '4' in lista_ano_serie[i] or '5' in lista_ano_serie[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 3).exists():
                            etapa = Etapa.objects.get(id= 3)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 3)
                            etapa.save()
                            etapa = etapa.etapa
                    else:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 4).exists():
                            etapa = Etapa.objects.get(id= 4)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 4)
                            etapa.save()
                            etapa = etapa.etapa
                

                #Ensino Médio     
                elif 'ENSINO MÉDIO' in lista_etapa[i]:          
                    if lista_turno[i] == 'INTEGRAL':
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 6).exists():
                            etapa = Etapa.objects.get(id= 6)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 6)
                            etapa.save()
                            etapa = etapa.etapa
                    else:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 5).exists():
                            etapa = Etapa.objects.get(id= 5)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 5)
                            etapa.save()
                            etapa = etapa.etapa
                
                if not Turmas.objects.filter(endereco= endereco, nome= nome_turma, etapa= etapa, ano_letivo= ano_letivo, turno= turno, ano_serie= lista_ano_serie[i]).exists():
                    turma = Turmas()
                    turma.endereco = endereco
                    turma.nome = nome_turma
                    turma.turno = turno
                    turma.etapa = etapa
                    turma.ano_serie = lista_ano_serie[i]
                    turma.ano_letivo = ano_letivo
                    turma.total_alunos = 0
                    turma.save()

            else:
                nome_turma = lista_nome[i]
                endereco = Endereco.objects.get(escola__cod_inep= cod_inep[i], tipo= 'S')

                #EJA
                if 'PRESENCIAL' in lista_etapa[i]:
                    if 'ENSINO FUNDAMENTAL' in lista_etapa[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 7).exists():
                            etapa = Etapa.objects.get(id= 7)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 7)
                            etapa.save()
                            etapa = etapa.etapa

                    elif 'ENSINO MÉDIO' in lista_etapa[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 8).exists():
                            etapa = Etapa.objects.get(id= 8)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 8)
                            etapa.save()
                            etapa = etapa.etapa


                #Ensino Fundamental
                elif 'ENSINO FUNDAMENTAL' in lista_etapa[i]:

                    if '1' in lista_ano_serie[i] or '2' in lista_ano_serie[i] or '3' in lista_ano_serie[i] or '4' in lista_ano_serie[i] or '5' in lista_ano_serie[i]:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 3).exists():
                            etapa = Etapa.objects.get(id= 3)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 3)
                            etapa.save()
                            etapa = etapa.etapa
                    else:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 4).exists():
                            etapa = Etapa.objects.get(id= 4)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 4)
                            etapa.save()
                            etapa = etapa.etapa

                #Ensino Médio     
                elif 'ENSINO MÉDIO' in lista_etapa[i]:
                    if lista_turno[i] == 'INTEGRAL':
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 6).exists():
                            etapa = Etapa.objects.get(id= 6)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 6)
                            etapa.save()
                            etapa = etapa.etapa
                    else:
                        if Etapa_escola.objects.filter(escola__cod_inep= cod_inep[i], etapa__id= 5).exists():
                            etapa = Etapa.objects.get(id= 5)
                        else:
                            etapa = Etapa_escola()
                            etapa.escola = Escola.objects.get(cod_inep= cod_inep[i])
                            etapa.etapa = Etapa.objects.get(id= 5)
                            etapa.save()
                            etapa = etapa.etapa

                
                if not Turmas.objects.filter(endereco= endereco, nome= nome_turma, etapa= etapa, ano_letivo= ano_letivo, turno= turno, ano_serie= lista_ano_serie[i]).exists():
                    turma = Turmas()
                    turma.endereco = endereco 
                    turma.nome = nome_turma
                    turma.turno = turno
                    turma.etapa = etapa
                    turma.ano_serie = lista_ano_serie[i]
                    turma.ano_letivo = ano_letivo
                    turma.total_alunos = 0
                    turma.save()

            # print()
            # print(endereco)
            # print(nome_turma)
            # print(turno)
            # print(etapa)
            # print(lista_ano_serie[i])
            # print(ano_letivo)
            # print('-'*100)
            # print()

            if Turmas.objects.filter(endereco= endereco, nome= nome_turma, etapa= etapa, ano_letivo= ano_letivo, turno= turno, ano_serie= lista_ano_serie[i]).exists():
                turma = Turmas.objects.filter(endereco= endereco, nome= nome_turma, etapa= etapa, ano_letivo= ano_letivo, turno= turno, ano_serie= lista_ano_serie[i]).first()

                #Cadastrar Alunos na turma
                cadastrar_aluno(turma, lista_nome_aluno[i], lista_cod_inep[i], lista_sexo[i], lista_nome_pai[i], lista_nome_mae[i], lista_nascimento[i], lista_cor[i], lista_endereco[i], lista_transporte[i], lista_nome_social[i], lista_deficiencia[i], lista_telefone[i], lista_celular[i], lista_email[i], lista_nome_responsavel[i], lista_responsavel_telefone[i], lista_cpf[i], lista_bolsa_familia[i], lista_ra[i], lista_data_matricula[i], lista_situacao[i], lista_data_encerramento[i])
          
            
    etapa = Etapa.objects.get(id= 11)
    for turma in Turmas.objects.filter(nome__icontains= 'APRENDER'):
        escola = turma.endereco.escola
        if not Etapa_escola.objects.filter(escola= escola, etapa= etapa).exists():
            etapa_escola = Etapa_escola()
            etapa_escola.escola= escola 
            etapa_escola.etapa = Etapa.objects.get(id= 11)
            etapa_escola.save()
        
        turma.etapa = etapa
        turma.ano_serie = 'PAC'
        turma.save()


def ler_planilha():
    # caminho = handle_uploaded_file(arquivo, 'dados_simaed.csv', 'Atena/', 'Atualizar dados do SIMAED')

    try:
        dados = pd.read_csv('C:/Users/Jloio/OneDrive/SEE-Trabalho/Atena/nl_SEE/static/media/Atena/Atualizar_dados_do_SIMAED/dados_simaed.csv')
    except:
        dados = pd.read_csv('C:/Users/Jloio/OneDrive/SEE-Trabalho/Atena/nl_SEE/static/media/Atena/Atualizar_dados_do_SIMAED/dados_simaed.csv')
    
    dados_filtrados = dados[dados['SITUACAO_MATRICULA'] == 'ATIVA']
    #Atualizar Turmas
    atualizar_turmas(dados_filtrados)
   
