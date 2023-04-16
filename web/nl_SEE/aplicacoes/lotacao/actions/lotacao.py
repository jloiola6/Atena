from datetime import date, datetime
from traceback import print_tb
from wsgiref.validate import validator

from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.administracao.models import Etapa, Disciplinas, Turmas, Grade, Escola, Professor_aluno, Aluno, Aluno_turma


def adicionar_aluno(request, id, turma= None):
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
    aluno.importacao = f'LOTAÇÃO - {date.today()}'
    aluno.save()
    salvar_historico(request, aluno, edicao, 'administracao_aluno', modificacoes_aluno)

    if not turma:
        turma = Turmas.objects.get(id= request.POST.get('turma_escolar1'))
    aluno_turna = Aluno_turma()
    aluno_turna.aluno = aluno
    aluno_turna.turma = turma
    aluno_turna.status = 1
    aluno_turna.importacao = f'LOTAÇÃO - {date.today()}'
    aluno_turna.save()
    salvar_historico(request, aluno_turna, edicao, 'administracao_aluno_turma', None)

    return str(aluno.id)


def lotacao_turma(request, contador, unidade):
    #Capturando dados
    edicao = False
    etapa = request.POST.get(f'etapa{contador}')

    if etapa == "2":
        ano_serie = request.POST.get(f'infantil{contador}')
    elif etapa == "3":
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

    if etapa in ["7", "8", "9"]:
        turma_sala = request.POST.get(f'modulo{contador}')
    else:
        turma_sala = request.POST.get(f'turma{contador}')

    turno = request.POST.get(f'turno{contador}')

    if etapa in ["7", "8", "9"]:
        nome = turma_sala
    else:
        nome = ano_serie + " " + turma_sala

    etapa = Etapa.objects.get(id= etapa)

    if not Turmas.objects.filter(endereco= unidade, turno= turno, ano_serie= ano_serie, nome= nome, ano_letivo= 2023, etapa = etapa).exists():
        modificacoes_turma = None
        turma = Turmas()
        turma.endereco = unidade
        turma.total_alunos = 0
        turma.nome = nome
        turma.turno = turno
        turma.etapa = etapa
        turma.ano_serie = ano_serie
        turma.ano_letivo = 2023
        turma.save()

        salvar_historico(request, turma, edicao, 'administracao_turmas', modificacoes_turma)
    else:
        turma = Turmas.objects.get(endereco= unidade, turno= turno, ano_serie= ano_serie, nome= nome, ano_letivo= 2023, etapa = etapa)

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
    turma.ano_letivo = 2023
    turma.importacao = f'LOTAÇÃO - {date.today()}'
    turma.save()



    salvar_historico(request, turma, edicao, 'administracao_turmas')


def assinatura_lotacao(request, lotacao):
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
        if Servidor_lotacao.objects.filter(unidade_adm= unidade, funcao__icontains= 'Coordenador do Núcleo', status= 1).exists():
            chefe = Servidor_lotacao.objects.filter(unidade_adm= unidade, funcao__contains= 'Coordenador do Núcleo', status= 1).last()
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


def professorAluno_lotacao(request, lotacao, edicao, unidade):
    nova_turma = False
    mediador_aluno = []
    
    for post in request.POST:
        if 'mediador-aluno' in post:
            mediador_aluno.append(post)
            turma = None
        if 'nova_turma_aee' in request.POST.get(post):
            turma = lotacao_turma(request, '1', unidade)

    for item in mediador_aluno:
        if 'novo_aluno' in request.POST.get(item):
            id = str(int(request.POST.get(item).replace('novo_aluno','')) - 1)
            item = adicionar_aluno(request, id, turma)
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


def capturar_dados_professor(request, contrato, data_termino):
    if data_termino != '' and data_termino != None:
        comparador = 11
    else:
        comparador = 10

    valores_rotas = ['rota_auxilia', 'chsa', 'cnt', 'lgg', 'mat']
    rota_atual = 'error'
    rotas = []

    dados = []
    valores = []
    turmas = []
    c = 0
    names_validos = ['fieldset-tipo-disciplina', 'disciplina', 'carga_turma']
    posts = list(request.POST)
    for post in posts:
        if c > comparador:
            valor = request.POST.get(post)
            if 'rota_auxilia' in post:
                valor = request.POST.get(posts[c-1])
                rota_atual = valor.lower()
                valores.append(valor)

            if 'fieldset-tipo-disciplina' in post and int(str(post).split('fieldset-tipo-disciplina')[1]) > 1:
                valores.append(rotas)
                valores.append(turmas)
                dados.append(valores)
                valores = []
                turmas = []
                rotas = []
                valores.append(valor)
            elif 'turma_escola' in post or 'nova_turma' in post:
                turmas.append(valor)
            elif rota_atual in post.strip():
                rotas.append(valor)
            elif post[:-1] in names_validos:
                valores.append(valor)
        c += 1

    valores.append(rotas)
    valores.append(turmas)
    dados.append(valores)

    return dados


def definindo_disciplina(dado, item):
    if dado[item] == 'disciplina':
        rotas = ['']
        disciplina = Disciplinas.objects.get(id = dado[item+1])
    else:
        disciplina = None
        rotas = []
        rota = dado[item+2]
        for rota in dado[item+4]:
            rotas.append(f'{dado[item+2]} - {rota}')

    return rotas, disciplina


def cadastrar_enturmacao(request, edicao, turma, disciplina, rotas, id_lotacao, funcao_escolar, carga_horaria, unidade):
    if 'nova_turma' in turma:
        contador = int(turma.replace('nova_turma', ''))
        turma = lotacao_turma(request, contador, unidade)
    else:
        turma = Turmas.objects.get(id= turma)

    for rota in rotas:
        if not Grade.objects.filter(disciplina= disciplina, rota= rota, turma= turma, professor= id_lotacao, ano= '2023').exists():
            grade = Grade()
            if funcao_escolar != 'Professor(a) AEE' and funcao_escolar != 'Coordenador(a) Pedagógico(a) de Anos':
                grade.carga_horaria = carga_horaria.replace(',', '.')
                grade.disciplina = disciplina
                grade.rota = rota
            grade.turma = turma
            grade.ano = '2023'
            grade.professor = id_lotacao
            grade.status = 1
            grade.save()
            salvar_historico(request, grade, edicao, 'administracao_grade')


def professor_aee_lotacao(request, contrato, edicao, lotacao, funcao_escolar, unidade, data_termino):
    dados_reais= capturar_dados_professor(request, contrato, data_termino)[-1][-1]

    for turma in dados_reais:
        cadastrar_enturmacao(request, edicao, turma, None, [''], lotacao.id, funcao_escolar, '0', unidade)


def professor_lotacao(request, contrato, edicao, lotacao, funcao_escolar, unidade, data_termino):
    dados_reais = capturar_dados_professor(request, contrato, data_termino)

    for dado in dados_reais:
        for item in range(0, len(dado), 6):
            carga_horaria = dado[item+3]
            rotas, disciplina = definindo_disciplina(dado, item)

            for turma in dado[item+5]:
                cadastrar_enturmacao(request, edicao, turma, disciplina, rotas, lotacao.id, funcao_escolar, carga_horaria, unidade)


def desativar_lotacao(contrato):
    cargo_permitidos = ['CHEFE', 'CEC']
    if Servidor_lotacao.objects.filter(contrato= contrato).exists() and contrato.cargo.nome in cargo_permitidos:
        lotacao = Servidor_lotacao.objects.filter(contrato= contrato).last()
        lotacao.status = 0
        lotacao.save()

        saldo = int(contrato.saldo )
        contrato.saldo = str(saldo + int(lotacao.carga_horaria))
        contrato.save()


def adicionar_turno(request, lotacao):
    for item in ['turno-manha', 'turno-tarde', 'turno-noite']:
        if request.POST.get(item) != None:
            if 'manha' in item:
                lotacao.turno_manha = 1
            elif 'tarde' in item:
                lotacao.turno_tarde = 1
            elif 'noite' in item:
                lotacao.turno_noite = 1
    lotacao.save()


def formulario_lotacao(request, edicao, contrato, tipo_lotacao, tipo, unidade, funcao):
    if funcao in ['Diretor(a) Escolar', 'Coordenador(a) Administrativo de Escolas', 'Coordenador(a) de Ensino Escolar', 'Secretário(a) Escolar']:
        portaria = request.POST.get('portaria')
        doe_portaria = request.POST.get('doe-portaria')
    tipo_lotacao = request.POST.get('tipo_lotacao')
    subconta = int(request.POST.get('subconta'))
    orgao_origem = request.POST.get('orgao_origem')
    data_inicio = request.POST.get('inicio')
    data_termino = request.POST.get('data_finalizacao')
    carga_horaria = request.POST.get('carga_horaria')
    observacoes = request.POST.get('observacao')
    aluno_id = request.POST.get('mediador-aluno')
    numero_sei = request.POST.get('numero_sei')
    orgao_cedido = request.POST.get('orgaos')
    manha = request.POST.get('turno-manha')
    tarde = request.POST.get('turno-tarde')
    noite = request.POST.get('turno-noite')
    subconta = Servidor_subconta.objects.get(id= subconta)

    if manha == 'manha':
        manha = 1
    else:
       manha = None

    if tarde == 'tarde':
        tarde = 1
    else:
        tarde = None

    if noite == 'noite':
        noite = 1
    else:
        noite = None


    desativar_lotacao(contrato)

    lotacao = Servidor_lotacao()
    lotacao.contrato = contrato

    if tipo_lotacao not in ('Sem lotação', 'Cedido', 'Permuta'):
        if tipo == 'escolar':
            lotacao.unidade_escolar = unidade
        else:
            lotacao.unidade_adm = unidade
    elif tipo_lotacao in ('Cedido', 'Permuta'):
        lotacao.orgao_cedido = orgao_cedido

    if tipo_lotacao == 'Sem Lotação':
        lotacao.funcao = None
        lotacao.unidade_adm = None
        lotacao.unidade_escolar = None
        carga_horaria = '0'

    if tipo_lotacao in ('Complementação Salarial', 'Aula Complementar', 'Dedicação Exclusiva','Permuta','Cedido'):
        lotacao.numero_sei = numero_sei

    lotacao.funcao = funcao
    if funcao in ['Diretor(a) Escolar', 'Coordenador(a) Administrativo de Escolas', 'Coordenador(a) de Ensino Escolar', 'Secretário(a) Escolar']:
        lotacao.doe_portaria = doe_portaria
        lotacao.portaria = portaria
    lotacao.numero_memorando = memorando()
    lotacao.data_memorando = datetime.now()
    lotacao.subconta = subconta
    lotacao.tipo_lotacao = tipo_lotacao
    lotacao.orgao_origem = orgao_origem
    lotacao.data_inicio = data_inicio
    if data_termino != '' and data_termino != None:
        lotacao.data_termino = data_termino
    lotacao.carga_horaria = carga_horaria
    lotacao.status = 2
    lotacao.observacoes = observacoes
    lotacao.ano_referencia = str(date.today().year)

    if not Servidor_lotacao.objects.filter(data_inicio = data_inicio, data_termino = data_termino, carga_horaria = carga_horaria, contrato_id = contrato, funcao = funcao, tipo_lotacao = tipo_lotacao, orgao_origem = orgao_origem, orgao_cedido = orgao_cedido, status = 2, turno_manha = manha, turno_tarde = tarde, turno_noite = noite, subconta_id = subconta, observacoes = observacoes).exists():
        lotacao.save()
        salvar_historico(request, lotacao, edicao, 'lotacao_servidor_lotacao')

        saldo = int(contrato.saldo)
        contrato.saldo = str(saldo - int(carga_horaria))
        contrato.save()

        if funcao == 'Professor(a) AEE' or funcao == 'Coordenador(a) Pedagógico(a) de Anos' and tipo == 'escolar':
            professor_aee_lotacao(request, contrato, edicao, lotacao, funcao, unidade, data_termino)

        elif funcao == 'Professor(a)' and tipo_lotacao in ('Contrato', 'Aula Complementar', 'Dedicação Exclusiva') and tipo == 'escolar':
            professor_lotacao(request, contrato, edicao, lotacao, funcao, unidade, data_termino)

        elif lotacao.funcao in ('Mediador', 'Atendente Pessoal', 'Atendimento Domiciliar', 'Professor(a) Brailista', 'Interprete') and tipo == 'escolar':
            professorAluno_lotacao(request, lotacao, edicao, unidade)

        elif funcao == 'Professor(a)' and tipo == 'adm':
            id_disciplina = request.POST.get('disciplina')

            disciplina = Grade_professor_adm()
            disciplina.professor = lotacao.id
            disciplina.disciplina = Disciplinas.objects.get(id=id_disciplina)
            disciplina.status = 2
            disciplina.save()
            adicionar_turno(request, lotacao)

        else:
            adicionar_turno(request, lotacao)

        assinatura_lotacao(request, lotacao)
        return True
    else:
        return False

def lotacao_autorizar(request, id_lotacao, user, data):
    edicao=False
    status= request.POST.get('status')
    motivo= request.POST.get('motivo')

    autorizador= Usuarios.objects.get(login= user)
    lotacao= Servidor_lotacao.objects.get(id=id_lotacao)
    lotacao.status= status

    lotacao.save()
    salvar_historico(request, lotacao, edicao, 'lotacao_servidor_lotacao')

    autorizacao= Autorizacao_lotacao()
    autorizacao.autorizador= Servidor.objects.get(id=autorizador.servidor)
    autorizacao.lotacao= Servidor_lotacao.objects.get(id=id_lotacao)
    autorizacao.status= status
    autorizacao.data= data
    autorizacao.motivo= motivo

    autorizacao.save()
    salvar_historico(request, autorizacao, edicao, 'lotacao_autorizacao_lotacao')