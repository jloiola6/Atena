import re

from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.lotacao.models import *
from aplicacoes.core.uploads import handle_uploaded_file
from aplicacoes.usuario.models import Usuarios, Logs
from unidecode import unidecode
from datetime import datetime


def remove_non_ascii(text):
    text = text.lower()
    return text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('õ', 'o').replace('ê', 'e').replace('â', 'a').replace('ô', 'o')


def formulario_servidor(request):
    edicao = False

    matricula = request.POST.get('matricula')
    nome = request.POST.get('nome')
    nome_social = request.POST.get('nome_social')
    sexo = request.POST.get('sexo')
    data_nascimento = request.POST.get('data_nascimento')
    nacionalidade = request.POST.get('nacionalidade')

    valor = request.POST.get('naturalidade')
    if valor == 'Ji-Paraná - RO':
        valor = valor.split('-')
        naturalidade = f'{valor[0]}-{valor[1]}'
        uf = valor[-1]
    else:
        valor = valor.split('-')
        naturalidade = valor[0]
        uf = valor[-1]

    cpf = request.POST.get('cpf')
    cpf = re.sub('\D', '', cpf)
    rg = request.POST.get('rg')
    pis = request.POST.get('pis')
    titulo = request.POST.get('titulo')
    situacao = request.POST.get('situacao')

    if not Servidor.objects.filter(cpf = cpf).exists():
        servidor = Servidor()
        servidor.matricula = matricula
        servidor.nome = remove_non_ascii(nome).upper()
        servidor.nome_social = nome_social
        servidor.sexo = sexo
        servidor.data_nascimento = data_nascimento
        servidor.nacionalidade = nacionalidade
        servidor.uf = uf
        servidor.naturalidade = naturalidade
        servidor.cpf = cpf
        servidor.rg = rg
        servidor.pis = pis
        servidor.titulo_eleitor = titulo
        servidor.situacao = situacao
        servidor.save()
        salvar_historico(request, servidor, edicao, 'lotacao_servidor')

        estado = request.POST.get('estado')
        municipio = request.POST.get('municipio')
        regiao = request.POST.get('regiao')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        complemento = request.POST.get('complemento')

        endereco = Servidor_endereco()
        endereco.servidor = servidor
        endereco.uf = 'AC'
        endereco.municipio = municipio
        endereco.regiao = regiao
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.save()
        salvar_historico(request, endereco, edicao, 'lotacao_servidor_endereco')

        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')
        email = request.POST.get('email')

        if telefone:
            servidor_contato = Servidor_contato()
            servidor_contato.servidor = servidor
            servidor_contato.tipo_contato = 'T'
            servidor_contato.contato = telefone
            servidor_contato.save()
            salvar_historico(request, servidor_contato, edicao, 'lotacao_servidor_contato')

        if celular:
            servidor_contato = Servidor_contato()
            servidor_contato.servidor = servidor
            servidor_contato.tipo_contato = 'C'
            servidor_contato.contato = celular
            servidor_contato.save()
            salvar_historico(request, servidor_contato, edicao, 'lotacao_servidor_contato')

        if email:
            servidor_contato = Servidor_contato()
            servidor_contato.servidor = servidor
            servidor_contato.tipo_contato = 'E'
            servidor_contato.contato = email
            servidor_contato.save()
            salvar_historico(request, servidor_contato, edicao, 'lotacao_servidor_contato')

        instituicao = request.POST.get('instituicao')
        tipo_conta = request.POST.get('tipo-conta')
        agencia = request.POST.get('agencia')
        conta = request.POST.get('conta')

        if not Servidor_banco.objects.filter(instituicao= instituicao, tipo_conta= tipo_conta, agencia= agencia, conta= conta).exists():
            banco = Servidor_banco()
            banco.servidor = servidor
            banco.instituicao = instituicao
            banco.tipo_conta = tipo_conta
            banco.agencia = agencia
            banco.conta = conta
            banco.save()
            salvar_historico(request, banco, edicao, 'lotacao_servidor_banco')

        atualizacao = Atualizacao_cadastral()
        atualizacao.servidor = servidor
        atualizacao.ultima_atualizacao = datetime.today()
        atualizacao.log = request.session['log']
        atualizacao.save()

        return servidor


def formulario_servidor_banco(request, edicao, servidor):
    instituicao = request.POST.get('instituicao')
    tipo_conta = request.POST.get('tipo-conta')
    agencia = request.POST.get('agencia')
    conta = request.POST.get('conta')

    if edicao:
        banco = Servidor_banco.objects.filter(id= int(request.GET.get('id_servidor_banco')))

        inputs_banco = {'instituicao': instituicao, 'tipo_conta': tipo_conta, 'agencia': agencia, 'conta': conta}

        modificacoes_banco = dict_compare(banco.values()[0], inputs_banco)
        banco = banco[0]

    else:
        banco = Servidor_banco()
        banco.servidor = servidor
        modificacoes_banco = {}

    if not Servidor_banco.objects.filter(instituicao= instituicao, tipo_conta= tipo_conta, agencia= agencia, conta= conta).exists():
        banco.instituicao = instituicao
        banco.tipo_conta = tipo_conta
        banco.agencia = agencia
        banco.conta = conta
        banco.save()
        salvar_historico(request, banco, edicao, 'lotacao_servidor_banco', modificacoes_banco)

    atualizacao = Atualizacao_cadastral()
    atualizacao.servidor = servidor
    atualizacao.ultima_atualizacao = datetime.today()
    atualizacao.log = request.session['log']
    atualizacao.save()


def editar_contatos(request, edicao):

    def atualizar_contato(request, query, lista, endereco, edicao, tipo):
        for item in query:
            if item.contato not in (lista):
                excluir = True
                modificacoes_contato = {'tipo_contato': item.tipo_contato, 'contato': item.contato}
                salvar_historico(request, item, edicao, 'terceirizacao_servidor_contato', modificacoes_contato, excluir)
                item.delete()

        for item in lista:
            if not Servidor_contato.objects.filter(tipo_contato= tipo, contato= item, servidor= servidor).exists():
                modificacoes_contato = None
                contato = Servidor_contato()
                contato.tipo_contato = tipo
                contato.contato = item
                contato.servidor = servidor
                contato.save()

                salvar_historico(request, contato, edicao, 'terceirizacao_servidor_contato', modificacoes_contato)

    celulares = []
    emails = []
    telefones = []

    posts = request.POST
    id = request.GET.get('id')
    servidor = Servidor.objects.get(id= id)

    for post in posts:
        if 'celular' in post:
            celulares.append(request.POST.get(post))
        elif 'email' in post:
            emails.append(request.POST.get(post))
        elif 'telefone' in post:
            telefones.append(request.POST.get(post))

    qr_celulares = Servidor_contato.objects.filter(tipo_contato= 'C', servidor= servidor)
    qr_telefones = Servidor_contato.objects.filter(tipo_contato= 'T', servidor= servidor)
    qr_emails = Servidor_contato.objects.filter(tipo_contato= 'E', servidor= servidor)

    atualizar_contato(request, qr_celulares, celulares, servidor, edicao, 'C')
    atualizar_contato(request, qr_telefones, telefones, servidor, edicao, 'T')
    atualizar_contato(request, qr_emails, emails, servidor, edicao, 'E')

    atualizacao = Atualizacao_cadastral()
    atualizacao.servidor = servidor
    atualizacao.ultima_atualizacao = datetime.today()
    atualizacao.log = request.session['log']
    atualizacao.save()


def formulario_servidor_endereco(request, edicao, servidor, aplicacao= None):
    estado = request.POST.get('estado')
    municipio = request.POST.get('municipio')
    regiao = request.POST.get('regiao')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    bairro = request.POST.get('bairro')
    complemento = request.POST.get('complemento')

    if edicao:
        if aplicacao == "perfil":
            user = request.session['username']
            id_usuario = Usuarios.objects.get(login = user).servidor
            endereco = Servidor_endereco.objects.filter(id= int(id_usuario))

        endereco = Servidor_endereco.objects.filter(id= int(request.GET.get('id_servidor_endereco')))
        inputs_endereco = {'uf': estado, 'municipio': municipio, 'regiao': regiao, 'cep': cep, 'rua': rua, 'numero': numero, 'bairro': bairro, 'complemento': complemento}

        modificacoes_endereco = dict_compare(endereco.values()[0], inputs_endereco)
        endereco= endereco [0]

    else:
        endereco = Servidor_endereco()
        endereco.servidor = servidor
        modificacoes_endereco = {}

    endereco.uf = 'AC'
    endereco.municipio = municipio
    endereco.regiao = regiao
    endereco.cep = cep
    endereco.rua = rua
    endereco.numero = numero
    endereco.bairro = bairro
    endereco.complemento = complemento
    endereco.save()
    salvar_historico(request, endereco, edicao, 'lotacao_servidor_endereco', modificacoes_endereco)

    atualizacao = Atualizacao_cadastral()
    atualizacao.servidor = servidor
    atualizacao.ultima_atualizacao = datetime.today()
    atualizacao.log = request.session['log']
    atualizacao.save()


def formulario_servidor_base(request, edicao, servidor, lotacao):
    matricula = request.POST.get('matricula')
    nome = request.POST.get('nome')
    nome_social = request.POST.get('nome_social')
    sexo = request.POST.get('sexo')
    data_nascimento = request.POST.get('data_nascimento')
    nacionalidade = request.POST.get('nacionalidade')

    valor = request.POST.get('naturalidade')
    if valor == 'Ji-Paraná - RO':
        valor = valor.split('- ')
        naturalidade = f'{valor[0]}-{valor[1]}'
        uf = valor[-1]
    else:
        valor = valor.split('- ')
        naturalidade = valor[0]
        uf = valor[-1]

    cpf = request.POST.get('cpf')
    cpf = re.sub('\D', '', cpf)
    rg = request.POST.get('rg')
    pis = request.POST.get('pis')
    titulo = request.POST.get('titulo')
    situacao = request.POST.get('situacao')

    if edicao:
        servidor = Servidor.objects.filter(id= int(request.GET.get('id')))

        inputs_base = {'nome': nome, 'nome_social': nome_social, 'sexo': sexo, 'data_nascimento': data_nascimento, 'nacionalidade': nacionalidade, 'naturalidade': naturalidade, 'uf': uf, 'cpf': cpf, 'rg': rg, 'pis': pis, 'titulo_eleitor': titulo, 'situacao': situacao, 'matricula': matricula}
        modificacoes_base = dict_compare(servidor.values()[0], inputs_base)
        servidor= servidor[0]

    else:
        servidor = Servidor()
        servidor.servidor = servidor
        modificacoes_base = {}

    if lotacao:
        servidor.matricula = matricula
    servidor.nome = remove_non_ascii(nome).upper()
    servidor.nome_social = nome_social
    servidor.sexo = sexo
    servidor.data_nascimento = data_nascimento
    servidor.nacionalidade = nacionalidade
    servidor.uf = uf
    servidor.naturalidade = naturalidade
    servidor.cpf = cpf
    servidor.rg = rg
    servidor.pis = pis
    servidor.titulo_eleitor = titulo
    servidor.situacao = situacao
    servidor.save()
    salvar_historico(request, servidor, edicao, 'lotacao_servidor', modificacoes_base)

    atualizacao = Atualizacao_cadastral()
    atualizacao.servidor = servidor
    atualizacao.ultima_atualizacao = datetime.today()
    atualizacao.log = request.session['log']
    atualizacao.save()


def formulario_documento(request, servidor):
    edicao = False

    print(request.FILES)
    documento = request.FILES.get('documento')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')

    versao = Servidor_documento.objects.filter(servidor= servidor).count() + 1
    if versao > 1:
        nome = f'Documento({versao}).' + str(documento).split('.')[-1]
    else:
        nome = 'Documento.' + str(documento).split('.')[-1]

    salvar_documento = Servidor_documento()
    salvar_documento.servidor = servidor
    salvar_documento.documento = handle_uploaded_file(documento, nome, 'Lotacao/', servidor.nome)
    salvar_documento.categoria = categoria
    salvar_documento.descricao = descricao
    salvar_documento.save()
    salvar_historico(request, salvar_documento, edicao, 'lotacao_servidor_documento')


def formulario_escolaridade(request, servidor):
    edicao = False

    formacao = request.POST.get('formacao')
    if formacao == "Ensino Médio":
        escola = request.POST.get('select_escola')
        data_conclusao = request.POST.get('conclusao')
    elif formacao == "Ensino Médio - Magistério":
        escola_magisterio = request.POST.get('select_escola_magisterio')
        curso_magisterio = request.POST.get('curso_magisterio')
        data_conclusao = request.POST.get('conclusao')
    else:
        curso = request.POST.get('curso')
        instituicao = request.POST.get('instituicao')
        situacao = request.POST.get('fieldset-situacao')

        if situacao == "Concluído":
            data_conclusao = request.POST.get('conclusao')

    escolaridade = Servidor_escolaridade()
    if formacao == "Ensino Médio":
        escolaridade.servidor = servidor
        escolaridade.formacao = formacao
        escolaridade.escola = escola
        escolaridade.data_conclusao = data_conclusao
        escolaridade.situacao = "Concluído"
    elif formacao == 'Ensino Médio - Magistério':
        escolaridade.servidor = servidor
        escolaridade.formacao = formacao
        escolaridade.escola = escola_magisterio
        escolaridade.curso = curso_magisterio
        escolaridade.data_conclusao = data_conclusao
        escolaridade.situacao = "Concluído"
    else:
        escolaridade.servidor = servidor
        escolaridade.formacao = formacao
        escolaridade.curso = curso
        escolaridade.instituicao = instituicao
        escolaridade.situacao = situacao
        if situacao == "Concluído":
            escolaridade.data_conclusao = data_conclusao
    escolaridade.save()


def excluir_servidor(request, servidor):
    banco = Servidor_banco.objects.filter(servidor= servidor)
    if banco != None:
        banco.delete()
    contato = Servidor_contato.objects.filter(servidor= servidor)
    if contato != None:
        contato.delete()
    endereco = Servidor_endereco.objects.filter(servidor= servidor)
    if endereco != None:
        endereco.delete()
    atualizacao = Atualizacao_cadastral.objects.filter(servidor= servidor)
    if atualizacao != None:
        atualizacao.delete()
    documento = Servidor_documento.objects.filter(servidor= servidor)
    if documento != None:
        documento.delete()
    escolaridade = Servidor_escolaridade.objects.filter(servidor= servidor)
    if escolaridade != None:
        escolaridade.delete()
    base = Servidor.objects.get(id= servidor.id)
    if base != None:
        base.delete()
