import re

from aplicacoes.administracao.models import *
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.core.models import Historico
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import Logs, Permissao, Usuarios


def formulario_unidade(request, edicao):
    #Dados Escola
    inep =  request.POST.get('inep')
    turmalina =  request.POST.get('turmalina')
    nome =  request.POST.get('nome')
    dependencia =  request.POST.get('dependencia')

    #Dados Etapas
    etapas = []
    for etapa in Etapa.objects.all():
        if request.POST.get(etapa.nome) == 'on':
            etapas.append(etapa)

    #Dados Endereço
    tipo_localizacao =  request.POST.get('tipo_localizacao')
    municipio =  request.POST.get('municipio')
    regiao =  request.POST.get('regiao')
    zoneamento =  request.POST.get('zoneamento')
    cep = request.POST.get('cep')
    cep = re.sub('\D', '', cep)
    rua =  request.POST.get('rua')
    numero =  request.POST.get('numero')
    bairro =  request.POST.get('bairro')
    complemento =  request.POST.get('complemento')
    latitude =  request.POST.get('latitude')
    longitude =  request.POST.get('longitude')
    tipo =  'S'
    localizacao_diferenciada =  request.POST.get('localizacao_diferenciada')

    #Dados Contato
    telefone =  request.POST.get('telefone')
    telefone = re.sub('\D', '', telefone)
    celular =  request.POST.get('celular')
    celular = re.sub('\D', '', celular)
    email =  request.POST.get('email')

    modificacoes_escola = None
    modificacoes_endereco = None
    modificacoes_contato = None
    modificacoes_etapa = None

    escola = Escola()
    endereco = Endereco()


    #Salvando no banco dados da unidade
    escola.cod_inep = inep
    escola.cod_turmalina = turmalina
    escola.nome_escola = nome
    escola.dependencia_adm = dependencia
    escola.save()
    salvar_historico(request, escola, edicao, 'administracao_escola', modificacoes_escola)

    if tipo_localizacao == 'Indígena':
        if request.POST.get('fieldset-etnia') == 'existente':
            indigena_etnia = request.POST.get('etnia_select')
        else:
            indigena_etnia = request.POST.get('etnia_input')

        if request.POST.get('fieldset-localizacao') == 'existente':
            indigena_localizacao = request.POST.get('localizacao_select')
        else:
            indigena_localizacao = request.POST.get('localizacao_input')

        if request.POST.get('fieldset-aldeia') == 'existente':
            indigena_aldeia = request.POST.get('aldeia_select')
        else:
            indigena_aldeia = request.POST.get('aldeia_input')

        modificacoes_indigena_detalhes = None
        detalhes_indigenas = Detalhes_Indigena()

        detalhes_indigenas.etnia = indigena_etnia
        detalhes_indigenas.localizacao = indigena_localizacao
        detalhes_indigenas.aldeia = indigena_aldeia
        detalhes_indigenas.escola = escola
        detalhes_indigenas.save()
        salvar_historico(request, detalhes_indigenas, edicao, 'administracao_detalhes_indigena', modificacoes_indigena_detalhes)


    #Salvando no banco dados da unidade
    for etapa in etapas:
        etapa_escola = Etapa_escola()
        etapa_escola.escola = escola
        etapa_escola.etapa = etapa
        etapa_escola.save()
    salvar_historico(request, etapa_escola, edicao, 'administracao_etapa_escola', modificacoes_etapa)

    #Salvando no banco dados de endereço
    endereco.escola = escola
    endereco.tipo_localizacao = tipo_localizacao
    endereco.municipio = municipio
    endereco.regiao = regiao
    endereco.zoneamento = zoneamento
    endereco.cep = cep
    endereco.rua = rua
    endereco.numero = numero
    endereco.bairro = bairro
    endereco.complemento = complemento
    endereco.latitude = latitude
    endereco.longitude = longitude
    endereco.localizacao_diferenciada = localizacao_diferenciada
    endereco.tipo = 'S'
    endereco.save()
    salvar_historico(request, endereco, edicao, 'administracao_endereco', modificacoes_endereco)

    #Salvando no banco dados de contato
    names_contato = ['celular', 'telefone', 'email']
    for name in names_contato:
        if request.POST.get(name) != None:
            if len(request.POST.get(name)) > 0:
                contato = Contato()
                contato.endereco = endereco
                tipo_contato = name[0].upper()
                contato.tipo_contato = tipo_contato
                contato.contato = request.POST.get(name)
                contato.save()

                salvar_historico(request, contato, edicao, 'administracao_contato', modificacoes_contato)

def formulario_turma(request, edicao):
    #Capturando dados
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

    # if etapa in ["7", "8", "9", "12"]:
    #     nome = turma_sala
    # else:
    #     nome = ano_serie + " " + turma_sala

    if edicao:
        turma = Turmas.objects.filter(id= int(request.GET.get('turma')))
        etapa = Etapa.objects.get(id= etapa)

        inputs_turma = {'id': turma[0].id, 'nome': nome, 'turno': turno, 'etapa': etapa.id, 'ano_serie': ano_serie }
        modificacoes_turma = dict_compare(turma.values()[0], inputs_turma)

        turma = turma[0]
        etapa= etapa
    else:
        modificacoes_turma = None
        etapa = Etapa.objects.get(id= etapa)
        turma = Turmas()
        turma.endereco = Endereco.objects.get(id= request.GET.get('id'))
        turma.total_alunos = 0

    if etapa in ["7", "8", "9", "12"]:
        turma.nome = turma_sala
    else:
        turma.nome = ano_serie + " " + turma_sala

    turma.turno = turno
    turma.etapa = etapa
    turma.ano_serie = ano_serie
    turma.ano_letivo = 2022
    turma.save()

    salvar_historico(request, turma, edicao, 'administracao_turmas', modificacoes_turma)

def formulario_grade_disciplina(request, edicao):
    #Capturando dados
    disciplina = Disciplinas.objects.get(id= request.POST.get('disciplina'))
    professor = request.POST.get('professor')
    print('id:',professor)
    carga_horaria = request.POST.get('carga_horaria')

    if edicao:
        grade = Grade.objects.filter(id= request.GET.get('grade'))

        inputs_grade= {'id': grade[0].id, 'turma': grade[0].turma, 'disciplina': disciplina, 'professor': professor, 'carga_horaria': carga_horaria,}
        modificacoes_grade = dict_compare(grade.values()[0], inputs_grade)

        grade = grade[0]
    else:
        grade = Grade()
        modificacoes_grade = None
        grade.turma = Turmas.objects.get(id= request.GET.get('id'))

    if professor != None and professor != '':
        professor = int(professor)

        grade.professor = int(professor)

    #Salvando no banco dados da grade
    grade.disciplina = disciplina
    grade.carga_horaria = carga_horaria
    grade.save()
    salvar_historico(request, grade, edicao, 'administracao_grade', modificacoes_grade)

def formulario_organizacao_escolar(request, edicao):
    #Capturando dados
    escola = Escola.objects.get(id= request.GET.get('id'))
    site = request.POST.get('site')
    compartilha_espaco = request.POST.get('fieldset-organizacao-espacos')
    utiliza_espaco = request.POST.get('fieldset-organizacao-utiliza-espacos')
    projeto = request.POST.get('fieldset-organizacao-projeto')
    educacao_indigena = request.POST.get('fieldset-organizacao-indigena')
    processo = request.POST.get('fieldset-organizacao-processo')

    if edicao:
        organizacao = Organizacao_escolar.objects.filter(escola= escola)
        inputs_organizacao = {'site': site, 'espacos_entorno': utiliza_espaco, 'espacos_escola_comunidade': compartilha_espaco, 'pedagogia_atualizada': projeto, 'educacao_indigena': educacao_indigena, 'processo_seletivo': processo}
        modificacoes_organizacao = dict_compare(organizacao.values()[0], inputs_organizacao)

        organizacao = organizacao[0]
    else:
        organizacao = Organizacao_escolar()
        modificacoes_organizacao = None

    # Salvando no banco dados de organização escolar
    organizacao.escola = escola
    organizacao.site = site
    # organizacao.lingua_ministrada = lingua
    organizacao.espacos_entorno = utiliza_espaco
    organizacao.espacos_escola_comunidade = compartilha_espaco
    organizacao.pedagogia_atualizada = projeto
    organizacao.educacao_indigena = educacao_indigena
    organizacao.processo_seletivo = processo
    organizacao.save()
    salvar_historico(request, organizacao, edicao, 'administracao_organizacao_escolar', modificacoes_organizacao)

    if edicao:
        edicao = False
        Organizacao_formas_organizacao.objects.filter(organizacao_escolar= organizacao).delete()
        Organizacao_instrumento_educativo.objects.filter(organizacao_escolar= organizacao).delete()
        Organizacao_reserva_cota.objects.filter(organizacao_escolar= organizacao).delete()
        Organizacao_colegiados_escola.objects.filter(organizacao_escolar= organizacao).delete()

    for i in range(1, 7, 1):
        if request.POST.get(f'checkbox-{i}') != None:
            formas_organizacao = Organizacao_formas_organizacao()
            formas_organizacao.organizacao_escolar = organizacao
            formas_organizacao.tipo_organizacao = request.POST.get(f'checkbox-{i}')
            formas_organizacao.save()
            salvar_historico(request, formas_organizacao, edicao, 'administracao_formas_organizacao')

    for i in range(7, 19, 1):
        if request.POST.get(f'checkbox-{i}') != None:
            instrumento_educativo = Organizacao_instrumento_educativo()
            instrumento_educativo.organizacao_escolar = organizacao
            instrumento_educativo.instrumento = request.POST.get(f'checkbox-{i}')
            instrumento_educativo.save()
            salvar_historico(request, instrumento_educativo, edicao, 'administracao_instrumento_educativo')

    for i in range(19, 25, 1):
        if request.POST.get(f'checkbox-{i}') != None:
            reserva_cota = Organizacao_reserva_cota()
            reserva_cota.organizacao_escolar = organizacao
            reserva_cota.tipo_cota = request.POST.get(f'checkbox-{i}')
            reserva_cota.save()
            salvar_historico(request, reserva_cota, edicao, 'administracao_reserva_cota')

    for i in range(25, 31, 1):
        if request.POST.get(f'checkbox-{i}') != None:
            colegiados_escola = Organizacao_colegiados_escola()
            colegiados_escola.organizacao_escolar = organizacao
            colegiados_escola.orgao_colegiado = request.POST.get(f'checkbox-{i}')
            colegiados_escola.save()
            salvar_historico(request, colegiados_escola, edicao, 'administracao_colegiados_escola')

def excluir_disciplina(request, grade, edicao):
    edicao=False
    grades=  grade

    grades.status = 0
    grades.save()

def adicionar_mapa(request, endereco):
    google_map = request.POST.get('google_map')

    edicao = endereco.google_map != None

    endereco.google_map = google_map
    endereco.save()

    salvar_historico(request, endereco, edicao, 'administracao_endereco')

def editar_contatos(request, edicao):

    def atualizar_contato(request, query, lista, endereco, edicao, tipo):
        for item in query:
            if item.contato not in (lista):
                excluir = True
                modificacoes_contato = {'tipo_contato': item.tipo_contato, 'contato': item.contato, 'endereco_id': item.endereco.id}
                salvar_historico(request, item, edicao, 'administracao_contato', modificacoes_contato, excluir)
                item.delete()

        for item in lista:
            if not Contato.objects.filter(tipo_contato= tipo, contato= item, endereco= endereco).exists():
                modificacoes_contato = None
                contato = Contato()
                contato.tipo_contato = tipo
                contato.contato = item
                contato.endereco = endereco
                contato.save()

                salvar_historico(request, contato, edicao, 'administracao_contato', modificacoes_contato)

    celulares = []
    emails = []
    telefones = []

    posts = request.POST
    id = request.GET.get('id')
    endereco = Endereco.objects.get(id= id)

    for post in posts:
        if 'celular' in post:
            celulares.append(request.POST.get(post))
        elif 'email' in post:
            emails.append(request.POST.get(post))
        elif 'telefone' in post:
            telefones.append(request.POST.get(post))

    qr_celulares = Contato.objects.filter(tipo_contato= 'C', endereco= endereco)
    qr_telefones = Contato.objects.filter(tipo_contato= 'T', endereco= endereco)
    qr_emails = Contato.objects.filter(tipo_contato= 'E', endereco= endereco)

    atualizar_contato(request, qr_celulares, celulares, endereco, edicao, 'C')
    atualizar_contato(request, qr_telefones, telefones, endereco, edicao, 'T')
    atualizar_contato(request, qr_emails, emails, endereco, edicao, 'E')


def formulario_dados(request, etapas_existentes):
    edicao = True
    situacao = edicao

    #Dados Escola
    inep =  request.POST.get('inep')
    turmalina =  request.POST.get('turmalina')
    nome =  request.POST.get('nome')
    dependencia =  request.POST.get('dependencia')

    #Dados Modalidades
    etapas = []
    for etapa in Etapa.objects.all():
        if request.POST.get(etapa.nome) == 'on':
            etapas.append(etapa)

    escola = Escola.objects.filter(id= request.GET.get('id'))
    inputs_escola = {'id': escola[0].id, 'cod_inep': inep, 'cod_turmalina': turmalina, 'nome_escola': nome, 'dependencia_adm': dependencia}
    modificacoes_escola = dict_compare(escola.values()[0], inputs_escola)
    escola = escola[0]

    if modificacoes_escola != {}:
        #Salvando no banco dados da unidade
        escola.cod_inep = inep
        escola.cod_turmalina = turmalina
        escola.nome_escola = nome
        escola.dependencia_adm = dependencia
        escola.save()
        salvar_historico(request, escola, edicao, 'administracao_escola', modificacoes_escola)

    if etapas != etapas_existentes:
        for etapa in etapas_existentes:
            if etapa not in etapas:
                if Etapa_escola.objects.filter(escola= escola, etapa= etapa).exists():
                    excluir = True
                    etapa_escola = Etapa_escola.objects.filter(escola= escola, etapa= etapa)
                    etapa_escola.delete()

        modificacoes_etapa = None
        for etapa in etapas:
            if not Etapa_escola.objects.filter(escola= escola, etapa= etapa).exists():
                etapa_escola = Etapa_escola()
                etapa_escola.escola = escola
                etapa_escola.etapa = etapa
                etapa_escola.save()
                salvar_historico(request, etapa_escola, situacao, 'administracao_etapa_escola', modificacoes_etapa)

    return escola.cod_inep


def formulario_endereco(request):
    edicao = True

    tipo_localizacao =  request.POST.get('tipo_localizacao')
    municipio =  request.POST.get('municipio')
    regiao =  request.POST.get('regiao')
    zoneamento =  request.POST.get('zoneamento')
    cep = request.POST.get('cep')
    cep = re.sub('\D', '', cep)
    rua =  request.POST.get('rua')
    numero =  request.POST.get('numero')
    bairro =  request.POST.get('bairro')
    complemento =  request.POST.get('complemento')
    latitude =  request.POST.get('latitude')
    longitude =  request.POST.get('longitude')
    localizacao_diferenciada =  request.POST.get('localizacao_diferenciada')

    endereco = Endereco.objects.filter(id= int(request.GET.get('id')))
    inputs_endereco = {'id':int(request.GET.get('id')), 'tipo_localizacao': tipo_localizacao, 'municipio': municipio, 'regiao': regiao, 'zoneamento': zoneamento, 'cep': cep, 'rua': rua, 'numero': numero, 'bairro': bairro, 'complemento': complemento, 'escola_id': endereco[0].escola.id, 'latitude': latitude, 'longitude': longitude, 'localizacao_diferenciada': localizacao_diferenciada}
    modificacoes_endereco = dict_compare(endereco.values()[0], inputs_endereco)

    endereco = endereco[0]
    escola = endereco.escola

    if tipo_localizacao == 'Indígena':
        if request.POST.get('fieldset-etnia') == 'existente':
            indigena_etnia = request.POST.get('etnia_select')
        else:
            indigena_etnia = request.POST.get('etnia_input')

        if request.POST.get('fieldset-localizacao') == 'existente':
            indigena_localizacao = request.POST.get('localizacao_select')
        else:
            indigena_localizacao = request.POST.get('localizacao_input')

        if request.POST.get('fieldset-aldeia') == 'existente':
            indigena_aldeia = request.POST.get('aldeia_select')
        else:
            indigena_aldeia = request.POST.get('aldeia_input')

        if Detalhes_Indigena.objects.filter(escola= escola).exists():
            edicao_indigenas = True
            detalhes_indigenas = Detalhes_Indigena.objects.filter(escola= escola)

            endereco = Endereco.objects.filter(id= endereco.id)
            inputs_indigena_detalhes = {'id':int(request.GET.get('id')), 'etnia': indigena_etnia, 'localizacao': indigena_localizacao, 'aldeia': indigena_aldeia}
            modificacoes_indigena_detalhes = dict_compare(detalhes_indigenas.values()[0], inputs_indigena_detalhes)

            detalhes_indigenas = detalhes_indigenas[0]

            detalhes_indigenas.etnia = indigena_etnia
            detalhes_indigenas.localizacao = indigena_localizacao
            detalhes_indigenas.aldeia = indigena_aldeia
            detalhes_indigenas.escola = escola
            detalhes_indigenas.save()
            salvar_historico(request, detalhes_indigenas, edicao_indigenas, 'administracao_detalhes_indigena', modificacoes_indigena_detalhes)

        else:
            edicao_indigenas = False
            modificacoes_indigena_detalhes = None
            detalhes_indigenas = Detalhes_Indigena()

            detalhes_indigenas.etnia = indigena_etnia
            detalhes_indigenas.localizacao = indigena_localizacao
            detalhes_indigenas.aldeia = indigena_aldeia
            detalhes_indigenas.escola = escola
            detalhes_indigenas.save()
            salvar_historico(request, detalhes_indigenas, edicao_indigenas, 'administracao_detalhes_indigena', modificacoes_indigena_detalhes)

    #Salvando no banco dados de endereço
    endereco = Endereco.objects.get(id= int(request.GET.get('id')))
    if modificacoes_endereco != {}:
        endereco.escola = escola
        endereco.tipo_localizacao = tipo_localizacao
        endereco.municipio = municipio
        endereco.regiao = regiao
        endereco.zoneamento = zoneamento
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.latitude = latitude
        endereco.longitude = longitude
        endereco.localizacao_diferenciada = localizacao_diferenciada
        endereco.save()
        salvar_historico(request, endereco, edicao, 'administracao_endereco', modificacoes_endereco)


def formulario_anexo(request, escola):
    def ultimo_anexo(escola):
        endereco = Endereco.objects.filter(escola= escola, tipo= 'A').last()
        if endereco == None:
            return 1
        else:
            return endereco.numero_anexo + 1

    edicao = False

    tipo_localizacao =  request.POST.get('tipo_localizacao')
    municipio =  request.POST.get('municipio')
    regiao =  request.POST.get('regiao')
    zoneamento =  request.POST.get('zoneamento')
    cep = request.POST.get('cep')
    cep = re.sub('\D', '', cep)
    rua =  request.POST.get('rua')
    numero =  request.POST.get('numero')
    bairro =  request.POST.get('bairro')
    complemento =  request.POST.get('complemento')
    latitude =  request.POST.get('latitude')
    longitude =  request.POST.get('longitude')
    localizacao_diferenciada =  request.POST.get('localizacao_diferenciada')

    endereco = Endereco()
    endereco.escola = escola
    endereco.tipo_localizacao = tipo_localizacao
    endereco.municipio = municipio
    endereco.regiao = regiao
    endereco.zoneamento = zoneamento
    endereco.cep = cep
    endereco.rua = rua
    endereco.numero = numero
    endereco.bairro = bairro
    endereco.complemento = complemento
    endereco.latitude = latitude
    endereco.longitude = longitude
    endereco.localizacao_diferenciada = localizacao_diferenciada
    endereco.tipo = 'A'
    endereco.numero_anexo = ultimo_anexo(escola)
    endereco.save()
    salvar_historico(request, endereco, edicao, 'administracao_endereco')

    if tipo_localizacao == 'Indígena':
        if request.POST.get('fieldset-etnia') == 'existente':
            etnia = request.POST.get('etnia_select')
        else:
            etnia = request.POST.get('etnia_input')

        if request.POST.get('fieldset-localizacao') == 'existente':
            localizacao = request.POST.get('localizacao_select')
        else:
            localizacao = request.POST.get('localizacao_input')

        if request.POST.get('fieldset-aldeia') == 'existente':
            aldeia = request.POST.get('aldeia_select')
        else:
            aldeia = request.POST.get('aldeia_input')

        detalhes_indigenas = Detalhes_Indigena()
        detalhes_indigenas.escola = escola
        detalhes_indigenas.etnia = etnia
        detalhes_indigenas.localizacao = localizacao
        detalhes_indigenas.aldeia = aldeia
        detalhes_indigenas.save()
        salvar_historico(request, detalhes_indigenas, edicao, 'administracao_detalhes_indigena')

    #Salvando no banco dados de contato
    names_contato = ['celular', 'telefone', 'email']
    for name in names_contato:
        if request.POST.get(name) != None:
            if len(request.POST.get(name)) > 0:
                contato = Contato()
                contato.endereco = endereco
                tipo_contato = name[0].upper()
                contato.tipo_contato = tipo_contato
                contato.contato = request.POST.get(name)
                contato.save()

                salvar_historico(request, contato, edicao, 'administracao_contato')


def formulario_aluno(request, edicao):
    #Capturando dados
    nome = request.POST.get('nome')
    cpf = request.POST.get('CPF')
    cpf = re.sub('\D', '', cpf)
    sexo = request.POST.get('sexo')
    data = request.POST.get('data')
    nome_mae = request.POST.get('nome_mae')
    nome_pai = request.POST.get('nome_pai')
    nacionalidade = request.POST.get('nacionalidade')
    uf = request.POST.get('estado')
    naturalidade = request.POST.get('naturalidade')

    turma = Turmas.objects.get(id= request.GET.get('id'))
    aluno = Aluno()
    modificacoes_aluno = None

    aluno.nome = nome
    aluno.cpf = cpf
    aluno.sexo = sexo
    aluno.nascimento = data
    aluno.nome_pai = nome_pai
    aluno.nome_mae = nome_mae
    aluno.nacionalidade = nacionalidade
    aluno.uf = uf
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
    aluno.save()

    turma.total_alunos = str(int(turma.total_alunos) + 1)
    turma.save()
    salvar_historico(request, aluno, edicao, 'administracao_aluno', modificacoes_aluno)

    aluno_turma = Aluno_turma()
    aluno_turma.aluno = aluno
    aluno_turma.turma = turma
    aluno_turma.status = 1
    aluno_turma.save()
    salvar_historico(request, aluno_turma, edicao, 'administracao_aluno_turma')



def formulario_vincular_professor(request, aluno):
    edicao= False

    professor = request.POST.get('professor')

    if professor != '' and professor != None:
        vinculo = Professor_aluno()
        vinculo.aluno = aluno
        vinculo.professor = professor
        vinculo.status = 1
        vinculo.save()

        salvar_historico(request, vinculo, edicao, 'administracao_professor_aluno')
