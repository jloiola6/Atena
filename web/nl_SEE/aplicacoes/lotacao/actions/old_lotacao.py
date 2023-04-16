from datetime import date, datetime
from telnetlib import STATUS
from wsgiref.validate import validator

from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.administracao.models import Etapa, Disciplinas, Turmas, Grade, Escola, Professor_aluno, Aluno, Aluno_turma

def adicionar_aluno(request, id):

    nome = request.POST.get(f'nome-aluno{id}')
    cpf = request.POST.get(f'cpf-aluno{id}')
    data = request.POST.get(f'nascimento-aluno{id}')
    sexo = request.POST.get(f'sexo-aluno{id}')
    pai = request.POST.get(f'pai-aluno{id}')
    mae = request.POST.get(f'mae-aluno{id}')
    nacionalidade = request.POST.get(f'nacionalidade-aluno{id}')
    estado = request.POST.get(f'estado-aluno{id}')
    municipio = request.POST.get(f'naturalidade-aluno{id}')
    
    edicao = False
    aluno = Aluno()
    modificacoes_aluno = None

    aluno.nome = nome
    aluno.cpf = cpf
    aluno.sexo = sexo
    aluno.nascimento = data
    aluno.nome_pai = pai
    aluno.nome_mae = mae
    aluno.nacionalidade = nacionalidade
    aluno.uf = estado
    aluno.naturalidade = municipio

    aluno.bolsa_familia = 0
    aluno.celular = ''
    aluno.cod_inep = ''
    aluno.cor = ''
    aluno.data_encerramento = ''
    aluno.data_matricula = ''
    aluno.deficiencia = ''
    aluno.email = ''
    aluno.endereco = ''
    aluno.nome_responsavel = ''
    aluno.nome_social = ''
    aluno.ra = ''
    aluno.responsavel_telefone = ''
    aluno.situacao = ''
    aluno.telefone = ''
    aluno.transporte = 0
    aluno.save()
    salvar_historico(request, aluno, edicao, 'administracao_aluno', modificacoes_aluno)

    turma = Turmas.objects.get(id= request.POST.get('turma_escolar1'))
    aluno_turna = Aluno_turma()
    aluno_turna.aluno = aluno
    aluno_turna.turma = turma
    aluno_turna.status = 1
    aluno_turna.save()
    salvar_historico(request, aluno_turna, edicao, 'administracao_aluno_turma', None)

    return str(aluno.id)


def lotacao_turma(request, contador):
    #Capturando dados
    edicao = False
    etapa = request.POST.get(f'etapa{contador}')
 
    if etapa == "3":
        ano_serie = request.POST.get(f'fundamental1{contador}')
    elif etapa == "4":
        ano_serie = request.POST.get(f'fundamental2{contador}')
    elif etapa == "5":
        ano_serie = request.POST.get(f'medio{contador}')
    elif etapa == "6":
        ano_serie = request.POST.get(f'medio-integral{contador}')
    elif etapa == "7":
        ano_serie = request.POST.get(f'eja-f1{contador}')
    elif etapa == "8":
        ano_serie = request.POST.get(f'eja-medio{contador}')
    elif etapa == "9":
        ano_serie = request.POST.get(f'eja-profissional{contador}')
    elif etapa == "10":
        ano_serie = request.POST.get(f'aee{contador}')
    elif etapa == "11":
        ano_serie = request.POST.get(f'pac{contador}')
    elif etapa == "12":
        ano_serie = request.POST.get(f'campo-inciais1{contador}')
    elif etapa == "13":
        ano_serie = request.POST.get(f'campo-finais2{contador}')
    elif etapa == "14":
        ano_serie = request.POST.get(f'campo-medio{contador}')
    elif etapa == "15":
        ano_serie = request.POST.get(f'socio-inciais1{contador}')
    elif etapa == "16":
        ano_serie = request.POST.get(f'socio-finais2{contador}')
    elif etapa == "17":
        ano_serie = request.POST.get(f'socio-medio{contador}')
    elif etapa == "18":
        ano_serie = request.POST.get(f'socio-eja-fundamental1{contador}')
    elif etapa == "19":
        ano_serie = request.POST.get(f'socio-eja-fundamental2{contador}')
    elif etapa == "20":
        ano_serie = request.POST.get(f'socio-eja-medio{contador}')

    if etapa in ["7", "8", "9"]:
        turma_sala = request.POST.get(f'modulo{contador}')
    elif etapa == "18":
        turma_sala = request.POST.get(f'socio-eja1{contador}')
    elif etapa == "19":
        turma_sala = request.POST.get(f'socio-eja2{contador}')
    elif etapa == "20":
        turma_sala = request.POST.get(f'socio-eja3{contador}')
    else:
        turma_sala = request.POST.get(f'turma{contador}')

    turno = request.POST.get(f'turno{contador}')

    # if etapa in ["7", "8", "9"]:
    #     nome = turma_sala
    # else:
    nome = ano_serie + " " + turma_sala

    etapa = Etapa.objects.get(id= etapa)
    endereco = Endereco.objects.get(id= request.POST.get('endereco'))

    if  not Turmas.objects.filter(endereco= endereco, turno= turno, ano_serie= ano_serie, nome= nome, ano_letivo= 2022, etapa = etapa).exists():
        modificacoes_turma = None
        turma = Turmas()
        turma.endereco = endereco
        turma.total_alunos = 0
        turma.nome = nome
        turma.turno = turno
        turma.etapa = etapa
        turma.ano_serie = ano_serie
        turma.ano_letivo = 2022
        turma.save()

        salvar_historico(request, turma, edicao, 'administracao_turmas', modificacoes_turma)
    else:
        turma = Turmas.objects.get(endereco= endereco, turno= turno, ano_serie= ano_serie, nome= nome, ano_letivo= 2022, etapa = etapa)

    return turma


def memorando():
    data_dia = str(date.today()).split("-")
    ultimo = ((Servidor_lotacao.objects.all().last()).numero_memorando).split('/')
    if ultimo[1] == data_dia[0]:
        valor = int(ultimo[0])+1
        valor = f"{valor}/{data_dia[0]}"
    else:
        valor = f"1/{data_dia[0]}"
    return valor
        
    
def formulario_subconta(request):
    edicao = False

    sub = request.POST.get('sub')
    fonte = request.POST.get('fonte')
    situacao = request.POST.get('situacao')
    descricao = request.POST.get('descricao')

    if not Servidor_subconta.objects.filter(sub= sub, fonte= fonte, situacao= situacao, descricao= descricao).exists():
        subconta = Servidor_subconta()

        subconta.sub = sub
        subconta.fonte = fonte
        subconta.situacao = situacao
        subconta.descricao = descricao
        subconta.save()
        salvar_historico(request, subconta, edicao, 'lotacao_servidor_subconta')


def formulario_lotacao(request, edicao, contrato):
    tipo = request.POST.get('fieldset-tipo-unidade')
    unidade_escolar = request.POST.get('endereco')
    unidade_adm = request.POST.get('administrativa')
    funcao_adm = request.POST.get('funcao_adm')
    tipo_lotacao = request.POST.get('tipo_lotacao')
    subconta = int(request.POST.get('subconta'))
    funcao_escolar = request.POST.get('funcao_escolar')
    orgao_origem = request.POST.get('orgao_origem')
    data_inicio = request.POST.get('inicio')
    data_termino = request.POST.get('data_finalizacao')
    carga_horaria = request.POST.get('carga_horaria')
    observacoes = request.POST.get('observacao')
    aluno_id = request.POST.get('mediador-aluno')
    orgao_cedido = request.POST.get('orgaos')
    subconta = Servidor_subconta.objects.get(id= subconta)

    unidade_escolar = Endereco.objects.get(id = unidade_escolar)
    unidade_adm = Unidade_administrativa.objects.get(id = unidade_adm)



    # if not Servidor_lotacao.objects.filter(contrato= contrato, carga_horaria= carga_horaria, unidade_escolar= unidade_escolar, unidade_adm= unidade_adm, orgao_origem= orgao_origem, status= 1, tipo_lotacao= tipo_lotacao).exists():
    # if Servidor_lotacao.objects.filter(contrato= contrato).exists() and 'PROFESSOR' not in contrato.cargo.nome and 'APOIO' not in contrato.cargo.nome:
    cargo_permitidos = ['CHEFE', 'CEC']
    if Servidor_lotacao.objects.filter(contrato= contrato).exists() and contrato.cargo.nome in cargo_permitidos:
        lotacao = Servidor_lotacao.objects.filter(contrato= contrato).last()
        lotacao.status = 0
        lotacao.save()

        saldo = int(contrato.saldo )
        contrato.saldo = str(saldo + int(lotacao.carga_horaria))
        contrato.save()

    lotacao = Servidor_lotacao()
    lotacao.contrato = contrato

    funcao = ''
    if tipo_lotacao not in ('Sem lotação', 'Cedido', 'Permuta'):
        if tipo == 'escolar':
            lotacao.unidade_escolar = unidade_escolar
            lotacao.funcao = funcao_escolar
            funcao = funcao_escolar
        else:
            lotacao.unidade_adm = unidade_adm
            lotacao.funcao = funcao_adm
            funcao = funcao_adm
    elif tipo_lotacao in ('Cedido', 'Permuta'):
        lotacao.orgao_cedido = orgao_cedido
        lotacao.funcao = funcao_adm

    lotacao.numero_memorando = memorando()
    lotacao.data_memorando = datetime.now()
    lotacao.subconta = subconta
    lotacao.tipo_lotacao = tipo_lotacao
    lotacao.orgao_origem = orgao_origem
    lotacao.data_inicio = data_inicio
    if "TEMP"  in contrato.cargo.nome:
        lotacao.data_termino = data_termino
    lotacao.carga_horaria = carga_horaria
    lotacao.status = 1
    lotacao.observacoes = observacoes
    lotacao.save()
    salvar_historico(request, lotacao, edicao, 'lotacao_servidor_lotacao')

    saldo = int(contrato.saldo )
    contrato.saldo = str(saldo - int(carga_horaria))
    contrato.save()

    if "Professor" in funcao and not 'Professor(a) Brailista' in funcao:
        if  "TEMP"  in contrato.cargo.nome:
            comparador = 15
        else:
            comparador = 14

        dados = []
        valores = []
        turmas = []
        c = 0
        for post in request.POST:
            if c > comparador:
                valor = request.POST.get(post)
                if 'fieldset-tipo-disciplina' in post and int(str(post).split('fieldset-tipo-disciplina')[1]) > 1:
                    valores.append(turmas)
                    dados.append(valores)
                    valores = []
                    turmas = []
                    valores.append(valor)
                elif 'turma_escola' in post or 'nova_turma' in post:
                    turmas.append(valor)
                else:
                    valores.append(valor)
            c += 1

        valores.append(turmas)
        dados.append(valores)

        dados_reais = []
        for dado in dados:
            if len(dado) > 9:
                dados_reais.append([dado[0], dado[1], dado[2], dado[3], dado[4], dado[5], dado[6], dado[7], dado[-1]])
            else:
                dados_reais.append(dado)
        
        for dado in dados_reais:
            for item in range(0, len(dado), 9):
                if dado[item] == 'disciplina':
                    rota = None
                    disciplina = Disciplinas.objects.get(id = dado[item+1])
                else:
                    disciplina = None
                    rota = dado[item+2]
                    if rota == 'CHSA':
                        rota += f'- {dado[item+3]}'
                    elif rota == 'CNT':
                        rota += f'- {dado[item+4]}'
                    elif rota == 'LGG':
                        rota += f'- {dado[item+5]}'
                    elif rota == 'MAT':
                        rota += f'- {dado[item+6]}'

                carga_horaria = dado[item+7]
                
                for turma in dado[item+8]:
                    if 'nova_turma' in turma:
                        contador = int(turma.replace('nova_turma', ''))
                        turma = lotacao_turma(request, contador)
                    else:
                        turma = Turmas.objects.get(id= turma)

                    if not Grade.objects.filter(disciplina= disciplina, rota= rota, turma= turma, professor= lotacao.id, ano= '2022').exists():
                        grade = Grade()
                        if funcao_escolar != 'Professor(a) AEE':
                            grade.carga_horaria = carga_horaria
                            grade.disciplina = disciplina
                            grade.rota = rota
                        grade.turma = turma
                        grade.ano = '2022'
                        grade.professor = lotacao.id
                        grade.status = 1
                        grade.save()
                        salvar_historico(request, grade, edicao, 'administracao_grade')

    elif lotacao.funcao in ('Mediador', 'Atendente Pessoal', 'Atendimento Domiciliar', 'Professor(a) Brailista'):
        mediador_aluno = []
        for post in request.POST:
            if 'mediador-aluno' in post:
                mediador_aluno.append(post)

        for item in mediador_aluno:
            if 'novo_aluno' in request.POST.get(item):
                id = request.POST.get(item).replace('novo_aluno','')
                item = adicionar_aluno(request, id)
            else:
                item = request.POST.get(item)

            aluno = Aluno.objects.get(id= item)
            if not Professor_aluno.objects.filter(aluno= aluno, professor= lotacao.id, status= 1).exists():
                vinculo = Professor_aluno()
                vinculo.professor = lotacao.id
                vinculo.aluno = aluno
                vinculo.status = 1
                vinculo.save()
                salvar_historico(request, vinculo, edicao, 'administracao_professor_aluno')
    else:
        for item in ['turno-manha', 'turno-tarde', 'turno-noite']:
            if request.POST.get(item) != None:
                if 'manha' in item:
                    lotacao.turno_manha = 1
                elif 'tarde' in item:
                    lotacao.turno_tarde = 1
                elif 'noite' in item:
                    lotacao.turno_noite = 1
        lotacao.save()
        
    user = request.session['username']
    servidor_id = Usuarios.objects.get(login= user).servidor
    servidor = Servidor.objects.get(id= servidor_id)

    try:
        servidor_sistema = Servidor_lotacao.objects.filter(contrato__servidor= servidor, unidade_adm__isnull= False).last()
        if servidor_sistema.funcao:
            funcao_tecnico = servidor_sistema.funcao
        else:
            funcao_tecnico = "Técnico(a) de Lotação"
        sigla = servidor_sistema.unidade_adm.sigla
        unidade = servidor_sistema.unidade_adm
    except:
        servidor_sistema = Contrato_lotacao.objects.filter(servidor= servidor, unidade_administrativa__isnull= False).last()
        funcao_tecnico = "Técnico(a) de Lotação"
        sigla = servidor_sistema.unidade_administrativa.sigla
        unidade = servidor_sistema.unidade_administrativa

    departamento = unidade.nome
    
    if Servidor_lotacao.objects.filter(unidade_adm= unidade, funcao__contains= 'em exercicio', status= 1).exists():
        chefe = Servidor_lotacao.objects.filter(unidade_adm= unidade, funcao__contains= 'em exercicio', status= 1).last()
    else:
        chefe = Servidor_lotacao.objects.filter(unidade_adm= unidade, funcao__contains= 'Chefe', status= 1).last()


    if not Lotacao_assinatura.objects.filter(gestor= chefe.contrato.servidor.nome, lotacao= lotacao, tecnico=servidor).exists():
        historico_gestor = Lotacao_assinatura()
        historico_gestor.lotacao = lotacao
        historico_gestor.gestor = chefe.contrato.servidor.nome
        historico_gestor.cargo_gestor = chefe.funcao
        historico_gestor.sigla = sigla
        historico_gestor.lotacao_gestor = departamento
        historico_gestor.tecnico = servidor
        historico_gestor.funcao_tecnico = funcao_tecnico
        historico_gestor.rua = unidade.endereco.rua
        historico_gestor.numero = unidade.endereco.numero
        historico_gestor.bairro = unidade.endereco.bairro
        historico_gestor.cep = unidade.endereco.cep
        historico_gestor.municipio = unidade.endereco.municipio
        historico_gestor.uf = unidade.endereco.uf
        historico_gestor.telefone = unidade.telefone
        historico_gestor.email = unidade.email
        historico_gestor.save()

def formulario_turma(request, endereco):
    edicao= False

    etapa = request.POST.get('etapa')
 
    if etapa == "3":
        ano_serie = request.POST.get('fundamental1')
    elif etapa == "4":
        ano_serie = request.POST.get('fundamental2')
    elif etapa == "5":
        ano_serie = request.POST.get('medio')
    elif etapa == "6":
        ano_serie = request.POST.get('medio-integral')
    elif etapa == "7":
        ano_serie = request.POST.get('eja-f1')
    elif etapa == "12":
        ano_serie = request.POST.get('eja-f2')
    elif etapa == "8":
        ano_serie = request.POST.get('eja-medio')
    elif etapa == "9":
        ano_serie = request.POST.get('eja-profissional')
    elif etapa == "10":
        ano_serie = request.POST.get('aee')
    elif etapa == "11":
        ano_serie = request.POST.get('pac')

    if etapa in ["7", "8", "9", "12"]:
        turma_sala = request.POST.get('modulo')
    else:
        turma_sala = request.POST.get('turma')

    turno = request.POST.get('turno')
    total_alunos = request.POST.get('total_alunos')

    turma = Turmas()
    turma.endereco = Endereco.objects.get(id= request.GET.get('id'))
    turma.total_alunos = 0

    if etapa in ["7", "8", "9", "12"]:
        turma.nome = turma_sala
    else:
        turma.nome = ano_serie + " " + turma_sala

    turma.turno = turno
    turma.etapa = Etapa.objects.get(id= etapa)
    turma.ano_serie = ano_serie
    turma.ano_letivo = 2022
    turma.save()

    salvar_historico(request, turma, edicao, 'administracao_turmas')


def formulario_aluno(request, turma):
    edicao = False

    nome = request.POST.get('nome')
    cpf = request.POST.get('CPF')
    genero = request.POST.get('sexo')
    nascimento = request.POST.get('data')
    pai = request.POST.get('nome_pai')
    mae = request.POST.get('nome_mae')
    nacionalidade = request.POST.get('nacionalidade')
    estado = request.POST.get('estado')
    naturalidade = request.POST.get('naturalidade')

    aluno = Aluno()
    aluno.nome = nome
    aluno.cpf = cpf

    aluno.sexo = genero
    aluno.nascimento = nascimento
    aluno.nome_pai = pai
    aluno.nome_mae = mae
    aluno.nacionalidade = nacionalidade
    aluno.uf = estado
    aluno.naturalidade = naturalidade

    aluno.bolsa_familia = 0
    aluno.celular = ''
    aluno.cod_inep = ''
    aluno.cor = ''
    aluno.data_encerramento = ''
    aluno.data_matricula = ''
    aluno.deficiencia = ''
    aluno.email = ''
    aluno.endereco = ''
    aluno.nome_responsavel = ''
    aluno.nome_social = ''
    aluno.ra = ''
    aluno.responsavel_telefone = ''
    aluno.situacao = ''
    aluno.telefone = ''
    aluno.transporte = 0

    aluno.nome_turma = turma.nome
    aluno.save()
    salvar_historico(request, aluno, edicao, 'administracao_aluno')

    aluno_turma = Aluno_turma()
    aluno_turma.aluno = aluno
    aluno_turma.turma = turma
    aluno_turma.status = 1
    aluno_turma.save()
    salvar_historico(request, aluno_turma, edicao, 'administracao_aluno_turma')