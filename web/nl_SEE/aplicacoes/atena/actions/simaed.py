from aplicacoes.core.uploads import handle_uploaded_file
from aplicacoes.atena.models import *
from aplicacoes.administracao.models import *
from django.conf import settings

from datetime import datetime

import pandas as pd
import time

# CONSTANTES
DIA_ATUAL = date.today()
ANO_LETIVO = DIA_ATUAL.year

# FUNÇÃO QUE COMPARA DOIS DATAFRAMES E RETORNA SOMENTE A DIFERENÇA ENTRE ELES
def compara_dfs(df1, df2):
    novo_df = df1.merge(df2, how='outer', indicator=True)
    novo_df = novo_df[novo_df['_merge'] != 'both']

    return novo_df


# FUNÇÃO QUE LÊ UM IMPORTA DADOS PARA A TABELA AUXILIAR COM BASE EM UM ARQUIVO CSV
def nova_importacao(request):

    arquivo = request.FILES.get('arquivo')

    # CRIANDO O OBJETO DA IMPORTAÇÃO
    importacao = Importacao_simaed()
    importacao.data_hora = str(datetime.now())
    importacao.status = 0
    importacao.save()

    # SALVANDO O ARQUIVO RELACIONADO À IMPORTAÇÃO
    importacao.arquivo = handle_uploaded_file(arquivo, str(arquivo), 'SIMAED/', f'IMPORTACAO {importacao.id}')
    # importacao.arquivo_tratado = handle_uploaded_file(arquivo, f'TRATADO - {str(arquivo)}', 'SIMAED/', f'IMPORTAÇÃO #{importacao.id}')
    importacao.save()

    # INICIALIZANDO O DATA FRAME
    caminho = str(settings.BASE_DIR) + '/' + importacao.path_arquivo()
    data_frame = pd.read_csv(caminho, dtype= object).fillna('')

    importacao.enturmacoes = data_frame.shape[0]

    ultima_importacao = Importacao_simaed.objects.filter().exclude(id= importacao.id).last()
                               
    if ultima_importacao:
        ultima_importacao_caminho = ultima_importacao.path_arquivo()
        ultima_importacao_data_frame = pd.read_csv(ultima_importacao_caminho, dtype= object).fillna('')

        print(f'DF ANTES DO TRATAMENTO: {data_frame.shape}')


        data_frame = compara_dfs(ultima_importacao_data_frame, data_frame)

    importacao.novas_enturmacoes = data_frame.shape[0]

    print(f'DF DEPOIS DO TRATAMENTO: {data_frame.shape}')

    importacao.save()

    # CONSTANTES PARA TRATAMENTO
    ANOS_INICIAS = ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano']
    ANOS_FINAIS = ['6º Ano', '7º Ano', '8º Ano', '9º Ano']

    for index, linha in data_frame.iterrows():
        
        # ENCAPSULANDO OS DADOS DA PLANILHA
        municipio = linha['MUNICIPIO']
        escola = linha['ESCOLA']
        inep_escola = linha['CD_CENSO']
        nome_aluno = linha['NM_ALUNO']
        inep_aluno = linha['CD_INEP']
        nascimento = linha['DT_NASCIMENTO']
        nome_pai = linha['NM_PAI']
        nome_mae = linha['NM_MAE']
        sexo = linha['TP_SEXO']
        cor = linha['TP_COR']
        endereco = linha['ENDERECO']
        transporte = linha['TRANSPORTE_ESCOLAR']
        nome_social = linha['NM_ALUNO_SOCIAL']
        possui_deficiencia = linha['POSSUI_DEFICIENCIA']
        deficiencia = linha['DC_DEFICIENCIA']
        telefone = linha['NU_TELEFONE']
        celular = linha['NU_TELEFONE_CELULAR']
        email_aluno = linha['ED_EMAIL_ALUNO']
        nome_responsavel = linha['NM_RESPONSAVEL']
        numero_responsavel = linha['NU_RESPONSAVEL_TELEFONE']
        cpf_responsavel = linha['NU_RESPONSAVEL_CPF']
        cpf_aluno = linha['NU_CPF']
        bolsa_familia = linha['BOLSA_FAMILIA']
        cns = linha['NU_CNS']
        ra = linha['RA']
        nivel = linha['DC_NIVEL']
        etapa = linha['DC_ETAPA']
        turno = linha['DC_TURNO']
        turma = linha['DC_TURMA']
        periodo_letivo = linha['DC_PERIODO']
        data_matricula = linha['DATA_MATRICULA']
        situacao_matricula = linha['SITUACAO_MATRICULA']
        ano_referencia = linha['ANO_REFERENCIA']
        exclusivo_aee = linha['EXCLUSIVO_AEE']

        # TRATANDO DATA DE NASCIMENTO
        nascimento = nascimento.split('/')
        nascimento.reverse()
        nascimento = '-'.join(nascimento)

        # TRATANDO DATA DE MATRÍCULA
        data_matricula = data_matricula.split('/')
        data_matricula.reverse()
        data_matricula = '-'.join(data_matricula)

        # TRATANDO AS ETAPAS DE ENSINO COM BASE NA COLUNA DE NÍVEL DO SIMAED
        if 'FUNDAMENTAL - 9 ANOS' in nivel:
            if etapa in ANOS_INICIAS:
                nivel = '3'
            elif etapa in ANOS_FINAIS:
                nivel = '4'

        elif nivel == 'ENSINO MÉDIO':
            if turno == 'INTEGRAL':
                nivel = '6'
            else:
                nivel = '5'

        elif 'AEE' in nivel:
            nivel = '10'

        elif 'PRESENCIAL - ENSINO FUNDAMENTAL' in nivel:
            nivel = '7'

        elif 'PRESENCIAL - ENSINO MÉDIO' in nivel:
            nivel = '8'

        # TRATANDO OS TURNOS
        if turno == 'MANHÃ':
            turno = 'Matutino'
        elif turno == 'TARDE':
            turno = 'Vespertino'
        elif turno == 'NOITE':
            turno = 'Noturno'
        elif turno == 'INTEGRAL':
            turno = 'Integral'

        print(index, nome_aluno)

        # print(index, municipio, escola, inep_escola, nome_aluno, inep_aluno, nascimento, nome_pai, nome_mae, sexo, cor, endereco, transporte, nome_social, possui_deficiencia, deficiencia, telefone, celular, email_aluno, nome_responsavel, numero_responsavel, cpf_responsavel, cpf_aluno, bolsa_familia, cns, ra, nivel, etapa, turno, turma, periodo_letivo, data_matricula, situacao_matricula, ano_referencia, exclusivo_aee, sep=' | ', end='\n\n')
    
        simaed = Aux_simaed()
        simaed.importacao_simaed = importacao
        simaed.municipio = municipio
        simaed.escola = escola
        simaed.inep_escola = inep_escola
        simaed.nome_aluno = nome_aluno
        simaed.inep_aluno = inep_aluno
        simaed.nascimento = nascimento
        simaed.nome_pai = nome_pai
        simaed.nome_mae = nome_mae
        simaed.sexo = sexo
        simaed.cor = cor
        simaed.endereco = endereco
        simaed.transporte = transporte
        simaed.nome_social = nome_social
        simaed.possui_deficiencia = possui_deficiencia
        simaed.deficiencia = deficiencia
        simaed.telefone = telefone
        simaed.celular = celular
        simaed.email_aluno = email_aluno
        simaed.nome_responsavel = nome_responsavel
        simaed.numero_responsavel = numero_responsavel
        simaed.cpf_responsavel = cpf_responsavel
        simaed.cpf_aluno = cpf_aluno
        simaed.bolsa_familia = bolsa_familia
        simaed.cns = cns
        simaed.ra = ra
        simaed.nivel = nivel
        simaed.etapa = etapa
        simaed.turno = turno
        simaed.turma = turma
        simaed.periodo_letivo = periodo_letivo
        simaed.data_matricula = data_matricula
        simaed.situacao_matricula = situacao_matricula
        simaed.ano_referencia = ano_referencia
        simaed.exclusivo_aee = exclusivo_aee

        simaed.save()
    
    print(data_frame.head())


# FUNÇÃO QUE IDENTIFICA E RETORNA UMA TURMA JÁ EXISTENTE E CASO NÃO EXISTA RETORNA NONE
def busca_turma(nome, etapa, ano_serie, turno, inep):
    try:
        endereco = Endereco.objects.get(escola__cod_inep= inep, tipo= 'S')
        turma = Turmas.objects.get(nome= nome, etapa= etapa, ano_serie=ano_serie, turno= turno, endereco= endereco, ano_letivo= ANO_LETIVO)

        return turma
    except:
        return None


# FUNÇÃO QUE CRIA UMA NOVA TURMA E RETORNA O OBJETO CRIADO
def cria_turma(nome, etapa, ano_serie, turno, inep):
    endereco = Endereco.objects.get(escola__cod_inep= inep, tipo= 'S')

    try:
        nova_turma = Turmas()
        nova_turma.nome = nome

        nova_turma.etapa = etapa
        nova_turma.turno = turno
        nova_turma.ano_serie = ano_serie

        nova_turma.endereco = endereco
        nova_turma.ano_letivo = ANO_LETIVO

        nova_turma.importacao = f'SIMAED - {DIA_ATUAL}'

        print(f'TURMA CRIADA: {nova_turma}')
        nova_turma.save()

        return nova_turma
    except:
        print('TURMA NÃO CRIADA, INEP INVÁLIDO')


# FUNÇÃO QUE IDENTIFICA E RETORNA UM ALUNO JÁ EXISTENTE E CASO NÃO EXISTA RETORNA NONE
def busca_aluno(nome, cpf, inep_aluno, nascimento, nome_pai, nome_mae, nome_responsavel):
    print('-'*50)
    print(f'BUSCANDO: {nome}')
    print()

    if cpf.strip() != '':
        print(f'BUSCANDO POR CPF: {cpf}')

        aluno = Aluno.objects.filter(cpf= cpf)

        if aluno:
            aluno = aluno.last()
            print(f'CPF CADASTRADO NO ALUNO {aluno.nome}')

            return aluno
        else:
            print('CPF NÃO ENCONTRADO')
            print()

    elif inep_aluno.strip() != '':
        print(f'BUSCANDO POR INEP: {inep_aluno}')

        aluno = Aluno.objects.filter(cod_inep= inep_aluno)

        if aluno:
            aluno = aluno.last()
            print(f'INEP CADASTRADO NO ALUNO {aluno.nome}')

            return aluno
        else:
            print('INEP NÃO ENCONTRADO')
            print()

    elif nascimento.strip() != '':
        print(f'BUSCANDO POR NOME E DATA DE NASCIMENTO: {nascimento}')

        aluno = Aluno.objects.filter(nome= nome, nascimento= nascimento)

        if aluno:
            aluno = aluno.last()
            print(f'NASCIMENTO CADASTRADO NO ALUNO {aluno.nome}')

            return aluno
        else:
            print('NASCIMENTO NÃO ENCONTRADO')
            print()

    elif nome_responsavel.strip() != '':
        print(f'BUSCANDO POR RESPONSAVEL: {nome_responsavel}')

        aluno = Aluno.objects.filter(nome= nome, nome_responsavel= nome_responsavel)

        if aluno:
            aluno = aluno.last()
            print(f'RESPONSÁVEL CADASTRADO NO ALUNO {aluno.nome}')
            # time.sleep(3)
            return aluno
        else:
            print('RESPONSÁVEL NÃO ENCONTRADO')
            print()


    elif nome_mae.strip() != '':
        print(f'BUSCANDO POR MÃE: {nome_mae}')

        aluno = Aluno.objects.filter(nome= nome, nome_mae= nome_mae)

        if aluno:
            aluno = aluno.last()
            print(f'MÃE CADASTRADO NO ALUNO {aluno.nome}')
            # time.sleep(3)
            return aluno
        else:
            print('MÃE NÃO ENCONTRADO')
            print()

    elif nome_pai.strip() != '':
        print(f'BUSCANDO POR PAI: {nome_pai}')

        aluno = Aluno.objects.filter(nome= nome, nome_mae= nome_pai)

        if aluno:
            aluno = aluno.last()
            print(f'PAI CADASTRADO NO ALUNO {aluno.nome}')
            # time.sleep(3)
            return aluno
        else:
            print('PAI NÃO ENCONTRADO')
            print()

    return None


# FUNÇÃO QUE CRIA UM NOVO ALUNO E RETORNA O OBJETO CRIADO
def cria_aluno(nome, nome_social, nascimento, cpf, sexo, cod_inep, nome_pai, nome_mae, uf, cor, endereco, transporte, bolsa_familia, deficiencia, telefone, celular, email, nome_responsavel, telefone_responsavel, ra, data_matricula):
    novo_aluno = Aluno()
    novo_aluno.nome = nome
    novo_aluno.nome_social = nome_social
    novo_aluno.nascimento = nascimento
    novo_aluno.cpf = cpf
    novo_aluno.sexo = sexo
    novo_aluno.cod_inep = cod_inep
    novo_aluno.nome_pai = nome_pai
    novo_aluno.nome_mae = nome_mae
    novo_aluno.uf = uf
    novo_aluno.cor = cor
    novo_aluno.endereco = endereco
    novo_aluno.transporte = transporte
    novo_aluno.bolsa_familia = bolsa_familia
    novo_aluno.deficiencia = deficiencia
    novo_aluno.telefone = telefone
    novo_aluno.celular = celular
    novo_aluno.email = email
    novo_aluno.nome_responsavel = nome_responsavel
    novo_aluno.responsavel_telefone = telefone_responsavel
    novo_aluno.ra = ra
    novo_aluno.data_matricula = data_matricula
    novo_aluno.data_encerramento = ''
    novo_aluno.situacao = ''

    novo_aluno.importacao = f'SIMAED - {DIA_ATUAL}'

    print(f'ALUNO CADASTRADO: {novo_aluno}')
    novo_aluno.save()

    return novo_aluno



def busca_enturmacao(aluno, turma):
    enturmacao = Aluno_turma.objects.filter(aluno= aluno, turma= turma)

    if enturmacao:
        return enturmacao.last()

    return None


def cria_enturmacao(aluno, turma):
    # ZERANDO AS ENTURMAÇÕES ANTERIORES DO ALUNO
    Aluno_turma.objects.filter(aluno= aluno).update(status= 0)

    # CRIANDO NOVA ENTURMAÇÃO
    nova_enturmacao = Aluno_turma()
    nova_enturmacao.aluno = aluno
    nova_enturmacao.turma = turma
    nova_enturmacao.status = 1

    nova_enturmacao.importacao = f'SIMAED - {DIA_ATUAL}'

    print(f'ENTURMAÇÃO CRIADA: {nova_enturmacao}')
    nova_enturmacao.save()

    return nova_enturmacao


def migrar_enturmacoes(inep_escola, importacao):
    # INICIALIZANDO ESCOLA
    try:
        escola = Escola.objects.get(cod_inep= inep_escola)
    except:
        print('ESCOLA INVÁLIDA')
        return

    print(f'ESCOLA: {escola}')
    # EXTRAINDO AS TURMAS DA TABELA AUXILIAR
    turmas = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO, inep_escola= inep_escola, importacao_simaed= importacao).values('inep_escola', 'turma', 'nivel', 'etapa', 'turno').distinct().order_by('nivel', 'turma')
    print()

    print(f'TURMAS ({turmas.count()})')
    for turma in turmas:
        # ENCAPSULANDO OS VALORES DA TABELA AUXILIAR
        nome = turma['turma']
        nivel = turma['nivel']
        etapa = Etapa.objects.get(id= nivel)
        ano_serie = turma['etapa']
        turno = turma['turno']

        print(f'{nome} {turno}')

        # VERIFICANDO SE A TURMA EXISTE NA BASE DE DADOS
        turma_atena = busca_turma(nome, etapa, ano_serie, turno, inep_escola)

        if turma_atena:
            print(f'TURMA JÁ CADASTRADA: {turma_atena}')
        else:
            print('TURMA NÃO CADASTRADA')

            # CRIANDO A TURMA CASO NÃO EXISTA NA BASE DE DADOS
            print('CRIANDO NOVA TURMA')
            turma_atena = cria_turma(nome, etapa, ano_serie, turno, inep_escola)
        print()

        # LISTANDO OS ALUNOS DA TABELA AUXILIAR COM BASE NA TURMA
        alunos = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO, inep_escola= inep_escola, turma= nome, nivel= nivel, etapa= ano_serie, turno= turno, importacao_simaed= importacao).order_by('nome_aluno')

        print(f'ALUNOS ({alunos.count()})')
        for aluno in alunos:
            # ENCAPSULANDO OS VALORES DA TABELA AUXILIAR
            nome = aluno.nome_aluno
            nome_social = aluno.nome_social
            nascimento = aluno.nascimento
            cpf = aluno.cpf_aluno
            sexo = aluno.sexo
            cod_inep = aluno.inep_aluno
            nome_pai = aluno.nome_pai
            nome_mae = aluno.nome_mae
            uf = 'AC'
            cor = aluno.cor
            endereco = aluno.endereco
            transporte = 1 if aluno.transporte == 'UTILIZA' else 0
            bolsa_familia = 1 if aluno.bolsa_familia == 'SIM' else 0
            deficiencia = aluno.deficiencia
            telefone = aluno.telefone
            celular = aluno.celular
            email = aluno.email_aluno
            nome_responsavel = aluno.nome_responsavel
            telefone_responsavel = aluno.numero_responsavel
            ra = aluno.ra
            data_matricula = aluno.data_matricula
            data_encerramento = ''
            situacao = ''

            print(nome, cpf, cod_inep, nascimento, nome_pai, nome_mae, sep=' | ')
            aluno_atena = busca_aluno(nome, cpf, cod_inep, nascimento, nome_pai, nome_mae, nome_responsavel)
            # time.sleep(2)
            # print('-'*50)

            if aluno_atena:
                print(f'ALUNO JÁ CADASTRADO: {aluno_atena.nome}')
            else:
                print('CRIANDO NOVO ALUNO')
                aluno_atena = cria_aluno(nome, nome_social, nascimento, cpf, sexo, cod_inep, nome_pai, nome_mae, uf, cor, endereco, transporte, bolsa_familia, deficiencia, telefone, celular, email, nome_responsavel, telefone_responsavel, ra, data_matricula)
            print()

            enturmacao_atena = busca_enturmacao(aluno_atena, turma_atena)

            if enturmacao_atena:
                print(f'ALUNO JÁ ENTURMADO: {enturmacao_atena.aluno} | {enturmacao_atena.turma}')
                enturmacao_atena.status = 1
                enturmacao_atena.save()
            else:
                print('ENTURMANDO ALUNO')
                enturmacao_atena = cria_enturmacao(aluno_atena, turma_atena)
            print()
            print()


        print('*'*100)
        print()

