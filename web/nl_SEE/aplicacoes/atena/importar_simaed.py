from aplicacoes.administracao.models import *
from datetime import date

DIA_ATUAL = date.today()
ANO_LETIVO = DIA_ATUAL.year

def importar_turmas():
    # LISTANDO OS INEPS DA TABELA AUXILIAR
    ineps_escolas = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO).values('inep_escola').distinct()

    # LISTANDO AS TURMAS DA TABELA
    novas_turmas = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO).values('inep_escola', 'turma', 'nivel', 'etapa', 'turno').distinct()

    # CONTADORES
    cont_escolas = 0
    cont_enderecos = 0
    cont_turmas_adicionadas = 0

    for inep in ineps_escolas:
        try:
            escola = Escola.objects.get(cod_inep= inep['inep_escola'])
            print(f'{escola.cod_inep} - {escola}')

            cont_escolas += 1

            try:
                endereco = Endereco.objects.get(escola= escola, tipo= 'S')
                cont_enderecos += 1

                cont_turmas = 0

                for turma in novas_turmas:
                    # PERCORRENDO AS TURMAS AGRUPANDO POR ESCOLA
                    if turma['inep_escola'] == escola.cod_inep:

                        # ENCAPSULANDO OS VALORES DA TABELA AUXILIAR
                        nome = turma['turma']
                        etapa = Etapa.objects.get(id= turma['nivel'])
                        ano_serie = turma['etapa']
                        turno = turma['turno']

                        print(nome, etapa, ano_serie, turno, sep=' -- ')

                        # VERIFICANDO SE A TURMA JÁ ESTÁ CADASTRADA NA TABELA DE TURMAS
                        existe = Turmas.objects.filter(nome= nome, etapa= etapa, ano_serie=ano_serie, turno= turno, endereco= endereco, ano_letivo= ANO_LETIVO).exists()

                        if not existe:

                            # CRIANO O OBJETO DA NOVA TURMA
                            nova_turma = Turmas()
                            nova_turma.nome = nome
                            nova_turma.etapa = etapa
                            nova_turma.turno = turno
                            nova_turma.ano_serie = ano_serie

                            nova_turma.endereco = endereco
                            nova_turma.ano_letivo = ANO_LETIVO

                            nova_turma.importacao = f'SIMAED - {DIA_ATUAL}'
                            nova_turma.save()

                            cont_turmas += 1

                            print(nova_turma.nome, nova_turma.etapa, nova_turma.ano_serie, nova_turma.turno, nova_turma.endereco, nova_turma.ano_letivo, nova_turma.importacao, sep=' -- ')
                            print('TURMA ADICIONADA')


                        else:
                            print('A TURMA JÁ EXISTE')


                            # turmas_simaed = Aux_simaed.objects.filter(turma= nome, etapa= ano_serie, nivel= etapa.id, turno= turno, ano_referencia= ANO_LETIVO, inep_escola= inep['inep_escola'])
                            # print(turmas_simaed.count())

                            # for turma_simaed in turmas_simaed:
                            #     turma = Turmas.objects.get(nome= nome, etapa= etapa, ano_serie=ano_serie, turno= turno, endereco= endereco, ano_letivo= ANO_LETIVO)
                            #     print(turma.id)
                            #     turma_simaed.id_turma = turma.id
                            #     turma_simaed.save()
                            # #     print(turma)


                        print()


                print(f'{cont_turmas} TURMAS ADICIONADAS')
                cont_turmas_adicionadas += cont_turmas
            except:
                print(f'ERRO NO ENDEREÇO DA ESCOLA {escola}')
        except:
            print(f'{inep["inep_escola"]} NÃO ENCONTRADO')

        print('-'*100)

    print(f'{cont_escolas} ESCOLAS - {cont_enderecos} ENDEREÇOS')
    print(f'{cont_turmas_adicionadas} TURMAS ADICIONADAS')


def busca_turma(nome, etapa, ano_serie, turno, inep, ano_letivo):
    try:
        endereco = Endereco.objects.get(escola__cod_inep= inep, tipo= 'S')
        turma = Turmas.objects.get(nome= nome, etapa= etapa, ano_serie=ano_serie, turno= turno, endereco= endereco, ano_letivo= ANO_LETIVO)

        return turma
    except:
        return None


def importar_alunos():
    # alunos_simaed = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO).values('nome_aluno', 'nascimento', 'sexo', 'inep_aluno', 'nome_pai', 'nome_mae', 'cor', 'transporte', 'endereco', 'nome_social', 'deficiencia', 'telefone', 'celular', 'email_aluno', 'nome_responsavel', 'numero_responsavel', 'cpf_aluno', 'bolsa_familia', 'ra', 'data_matricula', 'situacao_matricula')[:50]
    alunos_simaed = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO)

    cont_cpf = 0
    cont_inep = 0
    cont_ra = 0
    cont_nome = 0
    cont_novos = 0
    cont_novas_enturmacoes = 0

    cont_aux = 0

    for aluno_simaed in alunos_simaed:
        print(f'ALUNO: {aluno_simaed.nome_aluno}')
        print()

        print(f'BUSCANDO POR CPF: {aluno_simaed.cpf_aluno}')

        aluno = Aluno.objects.filter(cpf= aluno_simaed.cpf_aluno).last()

        if aluno and aluno_simaed.cpf_aluno != 'nan':
            print(f'CPF JÁ CADASTRADO NO ALUNO {aluno.nome}')
            cont_cpf += 1

        else:
            print('CPF NÃO ENCONTRADO')
            print()

            print(f'BUSCANDO POR INEP: {aluno_simaed.inep_aluno}')

            aluno = Aluno.objects.filter(cod_inep= aluno_simaed.inep_aluno).last()

            if aluno and aluno_simaed.inep_aluno != 'nan':
                print(f'INEP JÁ CADASTRADO NO ALUNO {aluno.nome}')
                cont_inep += 1

            else:
                print('INEP NÃO ENCONTRADO')
                print()

                print(f'BUSCANDO POR RA: {aluno_simaed.ra}')

                aluno = Aluno.objects.filter(ra= aluno_simaed.ra).last()

                if aluno:
                    print(f'REGISTRO ACADEMICO JÁ CADASTRADO NO ALUNO {aluno.nome}')
                    cont_ra += 1

                else:
                    print('REGISTRO ACADEMICO NÃO ENCONTRADO')
                    print()

                    print(f'BUSCANDO POR NOME E DATA DE NASCIMENTO: {aluno_simaed.nome_aluno} - {aluno_simaed.nascimento}')

                    aluno = Aluno.objects.filter(nome= aluno_simaed.nome_aluno, nascimento= aluno_simaed.nascimento).last()

                    if aluno:
                        print(f'ALUNO JÁ CADASTRADO')
                        cont_nome += 1

                    else:
                        print('ALUNO NÃO ENCONTRADO')
                        print()

                        print('CADASTRANDO NOVO ALUNO')

                        novo_aluno = Aluno()
                        novo_aluno.nome = aluno_simaed.nome_aluno
                        novo_aluno.nome_social = aluno_simaed.nome_social
                        novo_aluno.nascimento = aluno_simaed.nascimento
                        novo_aluno.cpf = aluno_simaed.cpf_aluno
                        novo_aluno.sexo = aluno_simaed.sexo
                        novo_aluno.cod_inep = aluno_simaed.inep_aluno
                        novo_aluno.nome_pai = aluno_simaed.nome_pai
                        novo_aluno.nome_mae = aluno_simaed.nome_mae
                        novo_aluno.uf = 'AC'
                        novo_aluno.cor = aluno_simaed.cor
                        novo_aluno.endereco = aluno_simaed.endereco

                        if aluno_simaed.transporte == 'UTILIZA':
                            novo_aluno.transporte = 1
                        else:
                            novo_aluno.transporte = 0

                        if aluno_simaed.bolsa_familia == 'SIM':
                            novo_aluno.bolsa_familia = 1
                        else:
                            novo_aluno.bolsa_familia = 0

                        novo_aluno.deficiencia = aluno_simaed.deficiencia
                        novo_aluno.telefone = aluno_simaed.telefone
                        novo_aluno.celular = aluno_simaed.celular
                        novo_aluno.email = aluno_simaed.email_aluno
                        novo_aluno.nome_responsavel = aluno_simaed.nome_responsavel
                        novo_aluno.responsavel_telefone = aluno_simaed.numero_responsavel
                        novo_aluno.ra = aluno_simaed.ra
                        novo_aluno.data_matricula = aluno_simaed.data_matricula
                        novo_aluno.data_encerramento = ''
                        novo_aluno.situacao = ''

                        novo_aluno.importacao = f'SIMAED - {DIA_ATUAL}'
                        novo_aluno.save()

                        aluno = novo_aluno

                        print(f'ALUNO CADASTRADO')
                        cont_novos += 1

        print('-'*100)
        # print(f'ENTURMANDO ALUNO {aluno} NO INEP {aluno_simaed.inep_escola}')

        # turma = busca_turma(aluno_simaed.turma, aluno_simaed.nivel, aluno_simaed.etapa, aluno_simaed.turno, aluno_simaed.inep_escola, ANO_LETIVO)

        # print(f'TURMA: {turma} - {turma.endereco.escola.cod_inep} {turma.endereco}')

        # if not Aluno_turma.objects.filter(turma= turma, aluno= aluno, status=1).exists():
        #     enturmacao = Aluno_turma()
        #     enturmacao.aluno = aluno
        #     enturmacao.turma = turma
        #     enturmacao.status = 1
        #     enturmacao.importacao = f'SIMAED - {DIA_ATUAL}'

        #     enturmacao.save()
        #     cont_novas_enturmacoes += 1
        #     print('ALUNO ENTURMADO')

        cont_aux += 1
        print(cont_aux)
        print('*'*100)
        print()

    print()


    print(f'{alunos_simaed.count()} ALUNOS NA TABELA AUXILIAR')

    print(f'{cont_cpf} CPFS CADASTRADOS')
    print(f'{cont_inep} INEPS CADASTRADOS')
    print(f'{cont_ra} RA CADASTRADOS')
    print(f'{cont_nome} NOMES CADASTRADOS')
    print(f'{cont_novos} NOVOS ALUNOS')
    # print(f'{cont_novas_enturmacoes} NOVAS ENTURMAÇÕES')
    print(f'TOTAL: {cont_nome+cont_cpf+cont_inep+cont_ra}')


def enturmar_alunos():
    alunos_simaed = Aux_simaed.objects.filter(ano_referencia= ANO_LETIVO)

    cont_aux = 1
    cont_enturmacaoes = 0
    cont_enturmacaoes_novas = 0

    for aluno_simaed in alunos_simaed:
        print(f'{cont_aux}. ALUNO: {aluno_simaed.nome_aluno}')
        cont_aux += 1
        print()

        aluno = None

        if aluno_simaed.cpf_aluno != 'nan':
            aluno = Aluno.objects.filter(cpf= aluno_simaed.cpf_aluno).last()

        if not aluno and aluno_simaed.inep_aluno != 'nan':
            aluno = Aluno.objects.filter(cod_inep= aluno_simaed.inep_aluno).last()
        else:
            aluno = Aluno.objects.filter(ra= aluno_simaed.ra).last()

        if not aluno:
            aluno = Aluno.objects.filter(nome= aluno_simaed.nome_aluno, nascimento= aluno_simaed.nascimento).last()

        if aluno:
            print(f'ALUNO INICIALIZADO')

            turma = busca_turma(aluno_simaed.turma, aluno_simaed.nivel, aluno_simaed.etapa, aluno_simaed.turno, aluno_simaed.inep_escola, ANO_LETIVO)

            if turma:
                print(f'TURMA: {turma} - {turma.endereco.escola.cod_inep} {turma.endereco}')
                print()

                print('INICIANDO ENTURMAÇÃO')
                print('-'*100)

                enturmacao = Aluno_turma.objects.filter(turma= turma, aluno= aluno, status=1).last()

                if enturmacao:
                    cont_enturmacaoes += 1
                    print(f'{cont_enturmacaoes}. ENTURMAÇÃO JÁ CADASTRADA - {enturmacao.id}')
                    print(f'ALUNO: {enturmacao.aluno}')
                    print(f'TURMA: {enturmacao.turma}')
                    print(f'STATUS: {enturmacao.status}')
                    print(f'IMPORTAÇÃO: {enturmacao.importacao}')
                else:
                    cont_enturmacaoes_novas += 1
                    print(f'NOVA ENTURMAÇÃO {cont_enturmacaoes_novas}')

                    nova_enturmacao = Aluno_turma()
                    nova_enturmacao.aluno = aluno
                    nova_enturmacao.turma = turma
                    nova_enturmacao.status = 1
                    nova_enturmacao.importacao = f'SIMAED - {DIA_ATUAL}'

                    nova_enturmacao.save()

                    print('ALUNO ENTURMADO')


            else:
                print('TURMA NÃO ENCONTRADA')
        else:
            print(f'ALUNO NÃO ENCONTRADO')

        print('*'*100)
        print()

    print(f'{cont_enturmacaoes} ENTURMAÇÕES')
    print(f'{cont_enturmacaoes_novas} NOVAS ENTURMAÇÕES')