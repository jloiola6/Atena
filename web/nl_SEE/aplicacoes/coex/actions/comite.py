import re
from aplicacoes.coex.models import *
from aplicacoes.core.uploads import handle_uploaded_file
from aplicacoes.core.actions import salvar_historico, dict_compare
from aplicacoes.administracao.models import Contato, Detalhes_Indigena, Endereco
from aplicacoes.lotacao.models import Servidor, Servidor_endereco, Servidor_contato, Atualizacao_cadastral
from datetime import datetime


def remove_non_ascii(text):
    text = text.lower()
    return text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('õ', 'o').replace('ê', 'e').replace('â', 'a').replace('ô', 'o')


def consultar_servidor(servidor, cpf= None):
    if servidor in ('None', ''):
        return None

    if cpf != None and Servidor.objects.filter(cpf= servidor).exists():
        servidor = Servidor.objects.filter(cpf= servidor).last()
    elif Servidor.objects.filter(id= servidor).exists():
        servidor = Servidor.objects.get(id= servidor)
    else:
        servidor = None
    return servidor


def formulario_documento(request, coex):
    edicao = False

    qr_arquivo = Arquivo.objects.filter(coex = coex)

    descricao = request.POST.get('descricao')
    documento = request.FILES.get('arquivo')

    versao = qr_arquivo.count() + 1
    if versao > 1:
        nome = f'Documento({versao}).' + str(documento).split('.')[-1]
    else:
        nome = 'Documento.' + str(documento).split('.')[-1]

    categorias = request.POST.get('categorias')

    arquivo = Arquivo()
    arquivo.coex = coex
    arquivo.descricao = descricao
    arquivo.arquivo = handle_uploaded_file(documento, nome, 'Coex/', coex.escola.nome_escola)
    arquivo.categoria = categorias
    arquivo.status = 1
    arquivo.save()
    salvar_historico(request, arquivo, edicao, 'coex_documento')


def formulario_comite(request):
    edicao = False

    id_escola = request.POST.get('unidade')
    cnpj = request.POST.get('cnpj')
    nome_empresarial = request.POST.get('nome_empresarial')
    if nome_empresarial == '':
        nome_empresarial = None
    escola = Escola.objects.get(id = id_escola)

    if not Coex.objects.filter(cnpj= cnpj).exists():
        coex = Coex()
        coex.escola = escola
        coex.cnpj = cnpj
        coex.nome_empresarial = nome_empresarial
        coex.status = 1
        coex.save()
        salvar_historico(request, coex, edicao, 'coex_coex')

        return escola.id


def formulario_equipe(request, edicao):
    id_escola = request.GET.get('id')
    nome_empresarial = request.POST.get('nome_empresarial')
    cnpj = request.POST.get('cnpj')

    presidente_id = request.POST.get('comite-presidente')
    presidente = consultar_servidor(presidente_id)
    tesoureiro_id = request.POST.get('comite-tesoureiro')
    tesoureiro = consultar_servidor(tesoureiro_id)
    # secretario2_id = request.POST.get('comite-secretario2')
    # secretario2 = consultar_servidor(secretario2_id)


    secretario1 = request.POST.get('secretario1')
    secretario2 = request.POST.get('secretario2')
    secretario3 = request.POST.get('secretario3')
    secretario4 = request.POST.get('secretario4')

    dados_equipe = ((presidente, 'Presidente'), (tesoureiro, 'Tesoureiro'), (secretario1, 'Secretário 1'), (secretario2, 'Secretário 2'), (secretario3, 'Secretário 3'), (secretario4, 'Secretário 4'))
    print(dados_equipe)

    coex = Coex.objects.get(escola__id = id_escola)

    for dado in dados_equipe:
        if dado[0] != None:
            if '1' in dado[1] or '2' in dado[1] or '3' in dado[1] or '4' in dado[1]:
                if Equipe_comite.objects.filter(coex= coex, cargo= dado[1]).exists():
                    equipe = Equipe_comite.objects.get(coex= coex, cargo= dado[1])
                    equipe.nome = dado[0]
                else:
                    equipe = Equipe_comite()
                    equipe.nome = dado[0]
            else:
                if Equipe_comite.objects.filter(coex= coex, cargo= dado[1]).exists():
                    equipe = Equipe_comite.objects.get(coex= coex, cargo= dado[1])
                    equipe.servidor = dado[0]
                    coex.nome_empresarial = nome_empresarial
                    coex.cnpj = cnpj
                    coex.save()
                    salvar_historico(request, coex, edicao, 'coex_coex')
                else:
                    equipe = Equipe_comite()
                    equipe.servidor = dado[0]

            equipe.coex = coex
            equipe.cargo = dado[1]
            equipe.save()
            salvar_historico(request, equipe, edicao, 'coex_equipe_comite')


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


def editar_contato(request, edicao):

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
        print(post)
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


def formulario_servidor_base(request, id_servidor, edicao):
    nome = request.POST.get('nome')
    nome_social = request.POST.get('nome_social')
    sexo = request.POST.get('sexo')
    data_nascimento = request.POST.get('data_nascimento')
    nacionalidade = request.POST.get('nacionalidade')

    valor = request.POST.get('naturalidade')
    valor = valor.split('-')
    naturalidade = valor[0]
    uf = valor[1].strip()

    cpf = request.POST.get('cpf')
    cpf = re.sub('\D', '', cpf)
    rg = request.POST.get('rg')
    pis = request.POST.get('pis')
    titulo = request.POST.get('titulo')
    situacao = request.POST.get('situacao')

    servidor = Servidor.objects.filter(id= id_servidor)
    inputs_base = {'nome': nome, 'nome_social': nome_social, 'sexo': sexo, 'data_nascimento': data_nascimento, 'nacionalidade': nacionalidade, 'naturalidade': naturalidade, 'uf': uf, 'cpf': cpf, 'rg': rg, 'pis': pis, 'titulo_eleitor': titulo, 'situacao': situacao}
    modificacoes_base = dict_compare(servidor.values()[0], inputs_base)
    servidor= servidor[0]

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


def formulario_servidor_endereco(request, servidor):
    estado = request.POST.get('estado')
    municipio = request.POST.get('municipio')
    regiao = request.POST.get('regiao')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    bairro = request.POST.get('bairro')
    complemento = request.POST.get('complemento')

    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        edicao = False
        endereco = Servidor_endereco.objects.filter(servidor= servidor)

        inputs_endereco = {'uf': estado, 'municipio': municipio, 'regiao': regiao, 'cep': cep, 'rua': rua, 'numero': numero, 'bairro': bairro, 'complemento': complemento}
        modificacoes_endereco = dict_compare(endereco.values()[0], inputs_endereco)
        endereco= endereco [0]

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
    else:
        edicao = True
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

    atualizacao = Atualizacao_cadastral()
    atualizacao.servidor = servidor
    atualizacao.ultima_atualizacao = datetime.today()
    atualizacao.log = request.session['log']
    atualizacao.save()


def contatos_editar(request, id_servidor):
    edicao= True
    def atualizar_contato(request, query, lista, endereco,  edicao, tipo):
        for item in query:
            if item.contato not in (lista):
                excluir = True
                modificacoes_contato = {'tipo_contato': item.tipo_contato, 'contato': item.contato}
                salvar_historico(request, item, edicao, 'lotacao_servidor_contato', modificacoes_contato, excluir)
                item.delete()

        for item in lista:
            if not Servidor_contato.objects.filter(tipo_contato= tipo, contato= item, servidor= id_servidor).exists():
                modificacoes_contato = None
                contato = Servidor_contato()
                contato.tipo_contato = tipo
                contato.contato = item
                contato.servidor = servidor
                contato.save()

                salvar_historico(request, contato, edicao, 'lotacao_servidor_contato', modificacoes_contato)

    celulares = []
    emails = []
    telefones = []

    posts = request.POST
    servidor = Servidor.objects.get(id= id_servidor)

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


def comite_inativar(request, escola_id, user):
    edicao=False

    data_inativo = request.POST.get('data_inativo')
    motivo = request.POST.get('motivo')

    if Coex.objects.filter(escola = escola_id).exists():
        comite = Coex.objects.get(escola = escola_id)

        comite.status = 0
        comite.user_inativou = user
        comite.data_inativo = data_inativo
        comite.motivo = motivo
        comite.save()

    salvar_historico(request, comite, edicao, 'tecnologia_link')


def coex_excluir(request, id_documento):
    documento = Arquivo.objects.get(id = id_documento)
    documento.delete()
