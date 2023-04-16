import re

from aplicacoes.fundiaria.models import *
from aplicacoes.core.uploads import handle_uploaded_file
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.administracao.models import *



def formulario_documento(request, fundiaria):
    edicao = False

    descricao = request.POST.get('descricao')
    categoria = request.POST.get('categorias')
    arquivo = request.FILES.get('arquivo')
    
    files = request.FILES
    if len(files) > 1:
        versao = Arquivo.objects.filter(fundiaria = fundiaria, grupo__isnull= False).last()
        if versao == None:
            grupo = 'Grupo 1'
        else:
            versao = int(versao.grupo.split()[-1])
            grupo = f'Grupo {versao + 1}'

        anexar_documentos(request, fundiaria, edicao, descricao, categoria, '', files, grupo)
    else:    
        anexar_documentos(request, fundiaria, edicao, descricao, categoria, arquivo)


def formulario_imagem(request, fundiaria, img_fundiaria=None, name_descricao=None):
    edicao = False

  
    if img_fundiaria:
        descricao = name_descricao
        arquivo = img_fundiaria
    else:
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')

    files = request.FILES
    if len(files) > 1 and img_fundiaria == None:
        versao = Imagens.objects.filter(fundiaria = fundiaria, grupo__isnull= False).last()
        if versao == None:
            grupo = 'Grupo 1'
        else:
            versao = int(versao.grupo.split()[-1])
            grupo = f'Grupo {versao + 1}'

        anexar_imagem(request, fundiaria, edicao, descricao, '', files, grupo)
    else:    
        anexar_imagem(request, fundiaria, edicao, descricao, arquivo)


def anexar_imagem(request, fundiaria, edicao, descricao, arquivo, files=None, grupo=None):
    if files != None:
        for name in files:
            file = files[name]
            imagem = Imagens.objects.filter(fundiaria = fundiaria)
            versao = imagem.count() + 1

            if versao > 1:
                nome = f'Imagem({versao}).' + str(file).split('.')[-1]
            else:
                nome = 'Imagem.' + str(file).split('.')[-1]

            # categorias = request.POST.get('categorias')

            documento = Imagens()
            documento.fundiaria = fundiaria
            documento.descricao = descricao

            if fundiaria.endereco:
                documento.arquivo = handle_uploaded_file(file, nome, 'Fundiaria/', fundiaria.endereco.escola.nome_escola)
            else:
                documento.arquivo = handle_uploaded_file(file, nome, 'Fundiaria/', fundiaria.unidade_adm.nome)
            
            # documento.categoria = categorias
            documento.categoria = ''
            documento.grupo = grupo
            documento.save()
            salvar_historico(request, documento, edicao, 'fundiaria_imagens')
    else:
        imagem = Imagens.objects.filter(fundiaria = fundiaria)
        versao = imagem.count() + 1

        if versao > 1:
            nome = f'Imagem({versao}).' + str(arquivo).split('.')[-1]
        else:
            nome = 'Imagem.' + str(arquivo).split('.')[-1]

        # categorias = request.POST.get('categorias')

        documento = Imagens()
        documento.fundiaria = fundiaria
        documento.descricao = descricao

        if fundiaria.endereco:
            documento.arquivo = handle_uploaded_file(arquivo, nome, 'Fundiaria/', fundiaria.endereco.escola.nome_escola)
        else:
            documento.arquivo = handle_uploaded_file(arquivo, nome, 'Fundiaria/', fundiaria.unidade_adm.nome)
        
        # documento.categoria = categorias
        documento.categoria = ''
        documento.save()
        salvar_historico(request, documento, edicao, 'fundiaria_imagens')


def anexar_documentos(request, fundiaria, edicao, descricao, categoria, arquivo, files=None, grupo=None):
    if files != None:
        for name in files:
            file = files[name]
            documentos = Arquivo.objects.filter(fundiaria = fundiaria)
            versao = documentos.count() + 1

            if versao > 1:
                nome = f'Documento({versao}).' + str(file).split('.')[-1]
            else:
                nome = 'Documento.' + str(file).split('.')[-1]

            # categorias = request.POST.get('categorias')

            documento = Arquivo()
            documento.fundiaria = fundiaria
            documento.descricao = descricao

            if fundiaria.endereco:
                documento.arquivo = handle_uploaded_file(file, nome, 'Fundiaria/', fundiaria.endereco.escola.nome_escola)
            else:
                documento.arquivo = handle_uploaded_file(file, nome, 'Fundiaria/', fundiaria.unidade_adm.nome)
            
            # documento.categoria = categorias
            documento.categoria = categoria
            documento.grupo = grupo
            documento.save()
            salvar_historico(request, documento, edicao, 'fundiaria_imagens')
    else:
        documentos = Arquivo.objects.filter(fundiaria = fundiaria)
        versao = documentos.count() + 1

        if versao > 1:
            nome = f'Documento({versao}).' + str(arquivo).split('.')[-1]
        else:
            nome = 'Documentos.' + str(arquivo).split('.')[-1]

        # categorias = request.POST.get('categorias')

        documento = Arquivo()
        documento.fundiaria = fundiaria
        documento.descricao = descricao

        if fundiaria.endereco:
            documento.arquivo = handle_uploaded_file(arquivo, nome, 'Fundiaria/', fundiaria.endereco.escola.nome_escola)
        else:
            documento.arquivo = handle_uploaded_file(arquivo, nome, 'Fundiaria/', fundiaria.unidade_adm.nome)
        
        # documento.categoria = categorias
        documento.categoria = categoria
        documento.save()
        salvar_historico(request, documento, edicao, 'fundiaria_imagens')


def formulario_infraestrutura(request, edicao):
    unidade = request.POST.get('unidade')
    departamento = request.POST.get('departamento')
    regularizacao = request.POST.get('regularizacao')
    forma_ocupacao = request.POST.get('forma_ocupacao')
    convenio = request.POST.get('convenio')
    matricula = request.POST.get('matricula')
    metragem = request.POST.get('metragem')
    area_utilizada = request.POST.get('area_utilizada')
    area = request.POST.get('area')
    perimetro = request.POST.get('perimetro')
    conta_agua = request.POST.get('conta_agua')
    ppi = request.POST.get('ppi')
    bci = request.POST.get('bci')
    decreto = request.POST.get('decreto-criacao')
    portaria = request.POST.get('portaria-autorizacao')
    tipo = request.POST.get('tipo')
    arquivo1 = request.FILES.get('arquivo1')
    arquivo2 = request.FILES.get('arquivo2')

    # if tipo == 'Departamento SEE': 
    #     unidade_adm = Unidade_administrativa.objects.get(id= departamento)
    #     unidade = True
    # else:
    #     unidade = Endereco.objects.get(escola__id = unidade, tipo= 'S')
    #     unidade_adm = True

    posts = request.POST
    energia_eletrica = []
    for i in posts:
        if 'energia_eletrica' in i:
            energia_eletrica.append(i)

    if edicao:
        fundiaria = Fundiaria.objects.filter(id= request.GET.get('id_fundiaria'))
        inputs_fundiaria = {'forma_ocupacao': forma_ocupacao, 'area_imovel': metragem, 'area_utilizada': area_utilizada, 'area_construida': area, 'perimetro': perimetro, 'ppi': ppi, 'conta_agua': conta_agua, 'matricula_imoveis': matricula}
        modificacoes_escola = dict_compare(fundiaria.values()[0], inputs_fundiaria)
        fundiaria = fundiaria[0]

        fundiaria.forma_ocupacao = forma_ocupacao
        if forma_ocupacao == 'Cedido':
            fundiaria.convenio = convenio
        fundiaria.regularizacao = regularizacao
        fundiaria.area_imovel = metragem
        fundiaria.area_utilizada = area_utilizada
        fundiaria.area_construida = area
        fundiaria.perimetro = perimetro
        fundiaria.ppi = ppi
        fundiaria.bci = bci
        fundiaria.decreto_criacao = decreto
        fundiaria.portaria_autorizacao = portaria
        fundiaria.energia_eletrica = energia_eletrica
        fundiaria.conta_agua = conta_agua
        fundiaria.matricula_imoveis = matricula
        fundiaria.save()
        salvar_historico(request, fundiaria, edicao, 'fundiaria_fundiaria')

        if fundiaria.unidade_adm != None:
            tipo = 'Departamento SEE'
            unidade_adm = fundiaria.unidade_adm
        else:
            tipo = 'Escola'
            unidade = fundiaria.endereco

        for item in Energia.objects.filter(fundiaria = fundiaria):
            if item.energia_eletrica:
                excluir = True
                modificacoes_energia= {'fundiaria': item.fundiaria.id, 'energia_eletrica': item.energia_eletrica}
                salvar_historico(request, item, edicao, 'fundiaria_energia', modificacoes_energia, excluir)
                item.delete()
        
        for item in energia_eletrica:
            if not Energia.objects.filter(fundiaria= fundiaria, energia_eletrica= item).exists():
                modificacoes_energia = {'fundiaria': fundiaria.id, 'energia_eletrica': item}
                energia = Energia()
                energia.fundiaria = fundiaria
                energia.energia_eletrica = request.POST.get(item)
                energia.save()
                salvar_historico(request, energia, edicao, 'fundiaria_energia', modificacoes_energia)
        
        if arquivo1 != None and Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Frente').exists():
            banco_arquivo = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Frente')
            caminho_arquivo = str(banco_arquivo.arquivo).split('/')[-1]

            if tipo == 'Departamento SEE':
                nome_pasta = fundiaria.unidade_adm.nome
            else:
                nome_pasta = fundiaria.endereco.escola.nome_escola 

            handle_uploaded_file(arquivo1, caminho_arquivo, 'Fundiaria/', nome_pasta)
            salvar_historico(request, banco_arquivo, True, 'fundiaria_imagens', 'Alteração na imagem')
        elif arquivo1 != None:
            anexar_imagem(request, fundiaria, False, 'Frente', arquivo1)

        if arquivo2 != None and Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Aérea').exists():
            banco_arquivo = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Aérea')
            caminho_arquivo = str(banco_arquivo.arquivo).split('/')[-1]

            if tipo == 'Departamento SEE':
                nome_pasta = fundiaria.unidade_adm.nome
            else:
                nome_pasta = fundiaria.endereco.escola.nome_escola 

            handle_uploaded_file(arquivo2, caminho_arquivo, 'Fundiaria/', nome_pasta)
            salvar_historico(request, banco_arquivo, True, 'fundiaria_imagens', 'Alteração na imagem')
        elif arquivo2 != None:
            anexar_imagem(request, fundiaria, False, 'Aérea', arquivo2)
    else:
        if tipo == 'Departamento SEE': 
            unidade_adm = Unidade_administrativa.objects.get(id= departamento)
            unidade = True
        else:
            unidade = Endereco.objects.get(escola__id = unidade, tipo= 'S')
            unidade_adm = True

        if (unidade and not Fundiaria.objects.filter(unidade_adm= unidade_adm).exists()) or (Fundiaria.objects.filter(endereco= unidade).exists() and unidade_adm):
            
            fundiaria = Fundiaria()
            if tipo == 'Departamento SEE': 
                fundiaria.unidade_adm = unidade_adm
            else:
                fundiaria.endereco = unidade

            fundiaria.forma_ocupacao = forma_ocupacao
            if forma_ocupacao == 'Cedido':
                fundiaria.convenio = convenio
            fundiaria.regularizacao = regularizacao
            fundiaria.area_imovel = metragem
            fundiaria.area_utilizada = area_utilizada
            fundiaria.area_construida = area
            fundiaria.perimetro = perimetro
            fundiaria.ppi = ppi
            fundiaria.bci = bci
            fundiaria.decreto_criacao = decreto
            fundiaria.portaria_autorizacao = portaria
            fundiaria.energia_eletrica = energia_eletrica
            fundiaria.conta_agua = conta_agua
            fundiaria.matricula_imoveis = matricula
            fundiaria.save()
            salvar_historico(request, fundiaria, edicao, 'fundiaria_fundiaria')
        
        for cod in energia_eletrica:
            energia = Energia()
            energia.fundiaria = fundiaria
            energia.energia_eletrica = request.POST.get(cod)
            energia.save()
            salvar_historico(request, energia, edicao, 'fundiaria_energia')
        
        anexar_imagem(request, fundiaria, False, 'Frente', arquivo1)
        anexar_imagem(request, fundiaria, False, 'Aérea', arquivo2)
    
    if tipo == 'Departamento SEE': 
        return (unidade_adm.id, 'adm')
    else:
        return (unidade.escola.cod_inep, 'escola')


def formulario_extincao(request, fundiaria):
    edicao = False

    data_extincao = request.POST.get('data_extincao')
    data_paralizacao = request.POST.get('data_paralizacao')
    escola_guardia = request.POST.get('escola_guardia')
    decreto_extincao = request.POST.get('decreto_extincao')

    if not Extincao.objects.filter(fundiaria= fundiaria).exists():
        extincao = Extincao()
        extincao.fundiaria = fundiaria
        extincao.data_extincao = data_extincao
        extincao.data_paralizacao = data_paralizacao
        extincao.escola_guardia = escola_guardia
        extincao.decreto_extincao = decreto_extincao
        extincao.save()
        salvar_historico(request, extincao, edicao, 'fundiaria_extincao')


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
        salvar_historico(request, escola, edicao, 'fundiaria_escola', modificacoes_escola)

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
                salvar_historico(request, etapa_escola, situacao, 'fundiaria_etapa_escola', modificacoes_etapa)
    
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


def editar_contato(request, edicao):

    def atualizar_contato(request, query, lista, endereco, edicao, tipo):
        for item in query:
            if item.contato not in (lista):
                excluir = True
                modificacoes_contato = {'tipo_contato': item.tipo_contato, 'contato': item.contato, 'endereco_id': item.endereco.id}
                salvar_historico(request, item, edicao, 'fundiaria_contato', modificacoes_contato, excluir)
                item.delete()
        
        for item in lista:
            if not Contato.objects.filter(tipo_contato= tipo, contato= item, endereco= endereco).exists():
                modificacoes_contato = None
                contato = Contato()
                contato.tipo_contato = tipo
                contato.contato = item
                contato.endereco = endereco
                contato.save()

                salvar_historico(request, contato, edicao, 'fundiaria_contato', modificacoes_contato)

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