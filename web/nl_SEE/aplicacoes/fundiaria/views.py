from pydoc import doc
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from .models import *
from itertools import chain

from aplicacoes.usuario.models import Permissao, Servico as Usuario_servico
from aplicacoes.usuario.views import logout, verification
from aplicacoes.atena.models import Detalhes

from aplicacoes.administracao.models import *
from aplicacoes.core.views import (global_municipios, global_regioes, global_zoneamentos, verificar_manutencao)
from unidecode import unidecode
from aplicacoes.fundiaria.models import *
from aplicacoes.coex.models import *
from aplicacoes.fundiaria.filtros import *
from aplicacoes.fundiaria.actions.fundiaria import *
from django.core.paginator import Paginator

from aplicacoes.fundiaria.actions.fundiaria import *
from aplicacoes.fundiaria.exportar import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao


def index(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19]):
        return HttpResponseRedirect('/')


    template_name = 'fundiaria/index.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())


def unidades_adm(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19]):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'fundiaria/unidades_adm.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 19)

    adm_fundiaria = Fundiaria.objects.filter(unidade_adm__isnull= False).values_list('unidade_adm__id', flat = True)
    unidades_administrativa = Unidade_administrativa.objects.filter(id__in = adm_fundiaria)

    aplicacao = 'fundiaria-unidade-adm'

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
    try:
        quantidade_unidades_adm = unidades_administrativa.count()
    except:
        quantidade_unidades_adm = len(unidades_administrativa)

    paginator = Paginator(unidades_administrativa, 15)
    unidades_administrativa = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'


    return TemplateResponse(request, template_name, locals())


def unidades_educacionais(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19]):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'fundiaria/unidades_educacionais.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 19)

    escola_fundiaria = Fundiaria.objects.values_list('endereco__escola__id', flat = True)
    # adm_fundiaria = Fundiaria.objects.values_list('unidade_adm__id', flat = True)

    # unidade_administrativa = Unidade_administrativa_endereco.objects.filter(unidade__in = adm_fundiaria).values('unidade__id','','','','','')
    # unidade_administrativa = Unidade_administrativa_endereco.objects.filter(unidade__in = adm_fundiaria).values('id', '')
    enderecos = Endereco.objects.filter(tipo='S', escola__id__in = escola_fundiaria).values('escola', 'escola__cod_inep', 'escola__nome_escola', 'municipio', 'regiao', 'tipo_localizacao').order_by('escola__nome_escola')
    aplicacao = 'fundiaria-unidade-escolar'

    login = ('ana.marina', 'erick.nascimento', 'fabio.santos', 'franklin.farias', 'joaopedro.passos', 'joaoteixeira.netto', 'josecarlos.souza', 'tharlis.seixas')
    if user not in login:
        enderecos = enderecos.exclude(id__in = [669, 723, 724, 722])

    #Consultando as etapas de ensino para filtro
    name_tipificacoes = []
    tipificacoes = []
    for tipificacao in Escola.objects.all().values('tipificacao').distinct().exclude(tipificacao= None).order_by('tipificacao'):
        name = (tipificacao['tipificacao'])
        tipificacoes.append((f'id-{name}', name, tipificacao['tipificacao']))
        name_tipificacoes.append(name)

    #Consultando as etapas de ensino para filtro
    name_etapas = []
    etapas = []
    for etapa in Etapa_escola.objects.all().values('etapa__nome').distinct():
        name = (etapa['etapa__nome']).replace(' ', '_')
        etapas.append((f'id-{name}', name, etapa['etapa__nome']))
        name_etapas.append(name)

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        name = ('ETNIA_' + detalhe['etnia']).replace(' ', '_')
        etnias.append((f'id-{name}', name, detalhe['etnia']))
        name_etnia.append(name)

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        name = ('LOCALIZACAO_' + detalhe['localizacao']).replace(' ', '_')
        localizacoes.append((f'id-{name}', name, detalhe['localizacao']))
        name_localizacao.append(name)

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        name = ('ALDEIA_' + detalhe['aldeia']).replace(' ', '_')
        aldeias.append((f'id-{name}', name, detalhe['aldeia']))
        name_aldeia.append(name)

    #resgatando informações globais na aplicação Core
    municipios = global_municipios
    regioes = global_regioes

    #Definindo os names dos inputs checkbox de região
    name_regioes = []
    for regiao in regioes:
        name_regioes.append(unidecode(regiao).replace(' ','-').replace('/', '').replace('--', '-').lower())

    #Definindo os names dos inputs checkbox de municipios
    name_municipios = []
    for municipio in municipios:
        name_municipios.append(unidecode(municipio).replace(' ', '-'))

    #Criando um zip dos label e names dos inputs para usar na tag do front
    qtd_regioes = zip(regioes, name_regioes)
    qtd_municipios = zip(municipios, name_municipios)

    #Definindo informações de id, names e label para inputs checkbox tipo de localização
    tipo_localizacao = [('id-urbano', 'localizacao_urbano', 'Urbano'), ('id-rural', 'localizacao_rural', 'Rural'), ('id-indigena', 'localizacao_indigena', 'Indígena')]

    #Atualizando dados da tabela de acordo com os filtros
    enderecos = filtro_unidades(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes)
            # exportar_excel(request, enderecos, municipios, name_regioes, regioes, tipo_localizacao, name_modalidades, name_etapas, name_etnia, name_localizacao, name_aldeia)
            # exportar_excel(request, name_municipios, name_modalidades, name_regioes, regioes, tipo_localizacao)
        # else:
        #     exportar_pdf(request, name_municipios, name_modalidades, name_regioes, regioes, tipo_localizacao)


    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
    try:
        quantidade_escolas = enderecos.count()
    except:
        quantidade_escolas = len(enderecos)

    paginator = Paginator(enderecos, 15)
    enderecos = paginator.get_page(page)


    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        # if len(gets.split('&')) > 1:
            #Paginação + filtros passados pela url
        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if "page" not in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

        #Garantindo a existencia dos campos filtrados na página de acordo com os gets na url
        # filtros_modalidades = []
        filtros_etapas = []
        filtros_municipio = []
        filtros_regional = []
        filtros_localizacao = []
        filtros_etnias = []
        filtros_aldeias = []
        filtros_localizacao_inidigena = []
        filtros_tipificacoes = []

        for item in gets.split('&'):
            item = item.split('=')
            valor = item[0].replace('Ensino_M%C3%A9dio_-_Regular', 'Ensino_Médio_-_Regular')
            if item[0] == 'cod_inep':
                cod_inep = item[1]
            elif item[0] == 'nome_unidade':
                nome_unidade = item[1].replace('+', ' ')
            elif valor in name_municipios:
                filtros_municipio.append(valor)
            elif valor in name_regioes:
                filtros_regional.append(valor)
            # elif item[0] in name_modalidades:
            #     filtros_modalidades.append(item[0])
            elif valor in name_etapas:
                filtros_etapas.append(valor)
            elif valor in name_etnia:
                filtros_etnias.append(valor)
            elif valor in name_aldeia:
                filtros_aldeias.append(valor)
            elif valor in name_localizacao:
                filtros_localizacao_inidigena.append(valor)
            elif valor in name_tipificacoes:
                filtros_tipificacoes.append(valor)

            for i in tipo_localizacao:
                if i[1] == valor:
                    filtros_localizacao.append(valor)

    return TemplateResponse(request, template_name, locals())

def fundiaria_perfil(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19]):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/fundiaria_perfil.html'

    user = request.session['username']

    cod_inep = request.GET.get('inep')
    id_adm = request.GET.get('adm')

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 19)

    # VARIÁVEIS NECESSÁRIAS PARA A CONSTRUÇÃO DA PARTIAL DE PERFIL DE UNIDADE
    aplicacao = 'Fundiária'

    if cod_inep != None and cod_inep != '':
        unidade = True

        id_endereco = request.GET.get('id_endereco')

        try:
            escola = Escola.objects.get(cod_inep= cod_inep)
        except:
            return HttpResponseRedirect('/fundiaria')

        escola_etapas = Etapa_escola.objects.filter(escola= escola)

        # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
        possui_anexo = Endereco.objects.filter(escola= escola).count() > 1

        # CASO A ESCOLA POSSUA ANEXOS E NENHUM AINDA TENHA SIDO SELECIONADO, ENCAMINHAR PARA A PÁGINA DE SELEÇÃO DE ANEXOS
        if not possui_anexo:
            endereco = Endereco.objects.get(escola= escola)
        else:
            enderecos = Endereco.objects.filter(escola= escola).order_by('-tipo')

        # INICIALIZANDO O ENDEREÇO NO CASO DE UM ANEXO TER SIDO SELECIONADO OU CASO A ESCOLA NÃO POSSUA
        try:
            if id_endereco:
                endereco = Endereco.objects.get(escola= escola, id= id_endereco)
            else:
                endereco = Endereco.objects.get(escola= escola)
        except:
            return HttpResponseRedirect('/fundiaria')

        # INICIALIZANDO OS DADOS DO COMITE EXECUTIVO DE ACORDO COM A ESCOLA
        if Coex.objects.filter(escola= escola, status=1).exists():
            coex = Coex.objects.get(escola= escola, status=1)

            if Consorcio.objects.filter(cnpj= coex.cnpj, status=1).exists():
                consorcio = Consorcio.objects.get(cnpj= coex.cnpj, status=1)

        # INICIALIZANDO OS CONTATOS DA UNIDADE DE ACORDO COM O ENDEREÇO
        possui_contatos = Contato.objects.filter(endereco= endereco).count() > 0
        if possui_contatos:
            contatos = Contato.objects.filter(endereco= endereco)

        # INICIALIZANDO OS DADOS DA EQUIPE GESTORA DA UNIDADE
        diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'

        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
            diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).exists():
            pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
            ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
            administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
            secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    elif id_adm != None and id_adm != '':
        unidade = Unidade_administrativa.objects.get(id= id_adm)
        endereco = True

    if (endereco and not Fundiaria.objects.filter(unidade_adm= unidade).exists()) or (Fundiaria.objects.filter(endereco= endereco).exists() and unidade):
        if id_adm != None and id_adm != '':
            fundiaria = Fundiaria.objects.get(unidade_adm = unidade)
            endereco = unidade.endereco
        else:
            fundiaria = Fundiaria.objects.get(endereco = endereco)

        if Extincao.objects.filter(fundiaria = fundiaria):
            extincoes = Extincao.objects.get(fundiaria = fundiaria)

        qtd_documentos = 0

        if Arquivo.objects.filter(fundiaria = fundiaria).exists():
            qtd_documentos = Arquivo.objects.filter(fundiaria = fundiaria).count()
            qr_documentos = Arquivo.objects.filter(fundiaria = fundiaria)[:3]

            documentos = []

            for documento in qr_documentos:
                formato_documento = str(documento.arquivo).split('.')[1]
                caminho = str(documento.path_arquivo())
                dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
                documentos.append(dict_documento)

        qtd_imagens = 0

        if Imagens.objects.filter(fundiaria = fundiaria).exists():
            qtd_imagens = Imagens.objects.filter(fundiaria = fundiaria).count()
            imagens = Imagens.objects.filter(fundiaria = fundiaria)[:4]

    fundiaria_id = fundiaria.id
    energia_eletrica = Energia.objects.filter(fundiaria = fundiaria_id)

    if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Frente').exists():
        img_frente = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Frente')
    else:
        img_frente = "Não contém imagem"

    if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Aérea').exists():
        img_aerea = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Aérea')
    else:
        img_aerea = "Não contém imagem"

    if request.method == 'POST':
        if request.POST.get('btn-exportar') == 'exportar':
            return exportar_pdf_escola(request, fundiaria, img_frente, img_aerea)
        else:
            adicionar_google(request)
            return HttpResponseRedirect(f'/fundiaria/unidade_perfil?inep={cod_inep}')

    return TemplateResponse(request, template_name, locals())

def fundiaria_perfil_antigo(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19]):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/fundiaria_perfil.html'

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 19)
    aplicacao = Usuario_servico.objects.get(id= 19).aplicacao.nome


    cod_inep = request.GET.get('inep')
    id_adm = request.GET.get('adm')
    if cod_inep != None and cod_inep != '':
        unidade = True

        id_endereco = request.GET.get('id_endereco')

        escola = Escola.objects.get(cod_inep= cod_inep)
        if Coex.objects.filter(escola= escola, status=1).exists():
            coex = Coex.objects.get(escola= escola, status=1)
        possui_anexo = Endereco.objects.filter(escola= escola).count() > 1
        escola_etapas = Etapa_escola.objects.filter(escola= escola)

        if id_endereco != None:
            endereco = Endereco.objects.get(id= id_endereco)
        else:
            endereco = None

        if not possui_anexo:
            endereco = Endereco.objects.get(escola= escola)
        else:
            enderecos = Endereco.objects.filter(escola= escola).order_by('-tipo')

        possui_contatos = Contato.objects.filter(endereco= endereco).count() > 0
        if possui_contatos:
            contatos = Contato.objects.filter(endereco= endereco)

        diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
            diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).exists():
            pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
            ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
            administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
            secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    elif id_adm != None and id_adm != '':
        unidade = Unidade_administrativa.objects.get(id= id_adm)
        endereco = True

    if (endereco and not Fundiaria.objects.filter(unidade_adm= unidade).exists()) or (Fundiaria.objects.filter(endereco= endereco).exists() and unidade):
        if id_adm != None and id_adm != '':
            fundiaria = Fundiaria.objects.get(unidade_adm = unidade)
            endereco = unidade.endereco
        else:
            fundiaria = Fundiaria.objects.get(endereco = endereco)

        if Extincao.objects.filter(fundiaria = fundiaria):
            extincoes = Extincao.objects.get(fundiaria = fundiaria)

        qtd_documentos = 0

        if Arquivo.objects.filter(fundiaria = fundiaria).exists():
            qtd_documentos = Arquivo.objects.filter(fundiaria = fundiaria).count()
            qr_documentos = Arquivo.objects.filter(fundiaria = fundiaria)[:3]

            documentos = []

            for documento in qr_documentos:
                formato_documento = str(documento.arquivo).split('.')[1]
                caminho = str(documento.path_arquivo())
                dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
                documentos.append(dict_documento)

        qtd_imagens = 0

        if Imagens.objects.filter(fundiaria = fundiaria).exists():
            qtd_imagens = Imagens.objects.filter(fundiaria = fundiaria).count()
            imagens = Imagens.objects.filter(fundiaria = fundiaria)[:4]

    fundiaria_id = fundiaria.id
    energia_eletrica = Energia.objects.filter(fundiaria = fundiaria_id)

    if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Frente').exists():
        img_frente = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Frente')
    else:
        img_frente = "Não contém imagem"

    if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Aérea').exists():
        img_aerea = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Aérea')
    else:
        img_aerea = "Não contém imagem"

    if request.method == 'POST':
        if request.POST.get('btn-exportar') == 'exportar':
            return exportar_pdf_escola(request, fundiaria, img_frente, img_aerea)
        else:
            adicionar_google(request)
            return HttpResponseRedirect(f'/fundiaria/unidade_perfil?inep={cod_inep}')

    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/documento-formulario.html'
    user = request.session['username']

    fundiaria_id = request.GET.get('id_fundiaria')

    if fundiaria_id != None and Fundiaria.objects.filter(id= fundiaria_id).exists():
        # categorias=["Decreto de criação","Portaria de funcionamento","Resolução", "Geolocalização", "Dados arquitetônicos", "Outros"]
        categorias=["Folha de rosto", "Decreto de desapropriação", "Planta", "Memorial descritivo", "Matrícula", "Laudo de avaliação", "Vistoria", "Registro patrimonial", "Processo completo", "Outros"]
        fundiaria = Fundiaria.objects.get(id = fundiaria_id)
        if fundiaria.endereco != None:
            endereco = fundiaria.endereco
            cod_inep = endereco.escola.cod_inep
        else:
            unidade = fundiaria.unidade_adm

        if request.method == 'POST' and request.FILES.get('arquivo'):
            formulario_documento(request, fundiaria)

            qtd_documentos = Arquivo.objects.filter(fundiaria= fundiaria).count()

            if qtd_documentos > 3:
                return HttpResponseRedirect(f'/fundiaria/gerenciador-documentos?id_fundiaria={fundiaria_id}')
            else:
                if fundiaria.endereco != None:
                    return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={cod_inep}')
                else:
                    return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?adm={unidade.id}')
    else:
        return HttpResponseRedirect('/fundiaria')

    return TemplateResponse(request, template_name, locals())


def imagem_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/imagem-formulario.html'
    user = request.session['username']

    fundiaria_id = request.GET.get('id_fundiaria')

    if fundiaria_id != None and Fundiaria.objects.filter(id= fundiaria_id).exists():
        # categorias=["Obras","Comunicação", "Avaliação", "Outros"]
        fundiaria = Fundiaria.objects.get(id = fundiaria_id)
        if fundiaria.endereco != None:
            endereco = fundiaria.endereco
            cod_inep = endereco.escola.cod_inep
        else:
            unidade = fundiaria.unidade_adm

        if request.method == 'POST' and request.FILES.get('arquivo'):
            formulario_imagem(request, fundiaria)

            qtd_imagens = Imagens.objects.filter(fundiaria= fundiaria).count()

            if qtd_imagens > 4:
                return HttpResponseRedirect(f'/fundiaria/galeria-imagem?id_fundiaria={fundiaria_id}')
            elif fundiaria.endereco != None:
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={cod_inep}')
            else:
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?adm={unidade.id}')

    else:
        return HttpResponseRedirect('/fundiaria')

    return TemplateResponse(request, template_name, locals())


def infraestrutura_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')


    template_name = 'fundiaria/infraestrutura-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 19)

    formas_ocupacoes = ['Próprio', 'Alugado', 'Cedido']
    regularizacao = ['Totalmente regularizada','Parcialmente regularizada','Não regularizada']
    convenio = ['Cedido do município para o estado','Cedido do estado para o município','Igreja em convênio com o estado']

    id_fundiaria = request.GET.get('id_fundiaria')
    if id_fundiaria != '' and id_fundiaria != None:
        edicao = True

        energia_eletrica = Energia.objects.filter(fundiaria = id_fundiaria)
        fundiaria = Fundiaria.objects.get(id= id_fundiaria)
        if fundiaria.endereco != None:
            escola = fundiaria.endereco.escola
        else:
            unidade = fundiaria.unidade_adm


        if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Frente').exists():
            imagem_frente = True
            img_frente = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Frente')
        if Imagens.objects.filter(fundiaria= fundiaria, descricao= 'Aérea').exists():
            imagem_aerea = True
            img_aerea = Imagens.objects.get(fundiaria= fundiaria, descricao= 'Aérea')
    else:
        edicao = False
        escola_fundiaria = Fundiaria.objects.filter(endereco__isnull= False).values_list('endereco__escola__id', flat = True)
        escolas = Escola.objects.all().exclude(id__in= escola_fundiaria).values('id', 'cod_inep', 'nome_escola').order_by('nome_escola')

        departamentos_fundiaria = Fundiaria.objects.filter(unidade_adm__isnull= False).values_list('unidade_adm__id', flat = True)
        departamentos = Unidade_administrativa.objects.all().exclude(id__in= departamentos_fundiaria).values('id', 'sigla', 'nome').order_by('nome')

    if request.method == 'POST':
        valor =  formulario_infraestrutura(request, edicao)
        if edicao:
            if valor[1] == 'escola':
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={valor[0]}')
            else:
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?adm={valor[0]}')
        else:
            if valor[1] == 'escola':
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={valor[0]}')
            else:
                return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?adm={valor[0]}')

    return TemplateResponse(request, template_name, locals())


def extincao_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/extincao-formulario.html'
    user = request.session['username']

    fundiaria_id = request.GET.get('id_fundiaria')
    fundiaria = Fundiaria.objects.get(id = fundiaria_id)
    if fundiaria.endereco != None:
        endereco = fundiaria.endereco
        cod_inep = endereco.escola.cod_inep
    else:
        unidade = fundiaria.unidade_adm

    if request.method == "POST":
        formulario_extincao(request, fundiaria)
        if fundiaria.endereco != None:
            return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={cod_inep}')
        else:
            return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?adm={unidade.id}')

    return TemplateResponse(request, template_name, locals())


def galeria_imagem(request):
    if verificar_manutencao() or not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/galeria-imagens.html'
    user = request.session['username']

    fundiaria_id = request.GET.get('id_fundiaria')

    fundiaria = Fundiaria.objects.get(id = fundiaria_id)
    if fundiaria.endereco != None:
        escola = fundiaria.endereco.escola
    else:
        unidade = fundiaria.unidade_adm

    imagens = Imagens.objects.filter(fundiaria= fundiaria)

    return TemplateResponse(request, template_name, locals())


def gerenciador_documentos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/gerenciador-documentos.html'
    user = request.session['username']

    fundiaria_id = request.GET.get('id_fundiaria')
    fundiaria = Fundiaria.objects.get(id = fundiaria_id)
    if fundiaria.endereco != None:
        escola = fundiaria.endereco.escola
    else:
        unidade = fundiaria.unidade_adm

    qr_documentos = Arquivo.objects.filter(fundiaria = fundiaria)

    documentos = []
    folha_rosto = []
    decretos = []
    plantas = []
    memoriais = []
    matriculas = []
    laudos = []
    vistorias = []
    patrimoniais = []
    completos = []
    outros = []

    for documento in qr_documentos:
        formato_documento = str(documento.arquivo).split('.')[1]
        caminho = str(documento.path_arquivo())
        dict_documento = {'id': documento.id, 'descricao': documento.descricao, 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
        documentos.append(dict_documento)

        if dict_documento['categoria'] == 'Folha de rosto':
            folha_rosto.append(dict_documento)

        elif dict_documento['categoria'] == 'Decreto de desapropriação':
            decretos.append(dict_documento)

        elif dict_documento['categoria'] == 'Planta':
            plantas.append(dict_documento)

        elif dict_documento['categoria'] == 'Memorial descritivo':
            memoriais.append(dict_documento)

        elif dict_documento['categoria'] == 'Matrícula':
            matriculas.append(dict_documento)

        elif dict_documento['categoria'] == 'Laudo de avaliação':
            laudos.append(dict_documento)

        elif dict_documento['categoria'] == 'Vistoria':
            vistorias.append(dict_documento)

        elif dict_documento['categoria'] == 'Registro patrimonial':
            patrimoniais.append(dict_documento)

        elif dict_documento['categoria'] == 'Processo completo':
            completos.append(dict_documento)

        elif dict_documento['categoria'] == 'Outros':
            outros.append(dict_documento)

    return TemplateResponse(request, template_name, locals())


def editar_dados(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/editar_dados.html'
    user = request.session['username']
    dependencias = ['Estadual', 'Federal', 'Municipal', 'Privado']

    id_escola = request.GET.get('id')
    if id_escola in (None, ''):
        return HttpResponseRedirect('/fundiaria/index')

    escola = Escola.objects.get(id= id_escola)
    etapas = Etapa.objects.all()

    etapa_existentes = []
    for item in Etapa_escola.objects.filter(escola= escola):
        etapa_existentes.append(item.etapa)

    if request.method == 'POST':
        inep = formulario_dados(request, etapa_existentes)
        return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={inep}')

    return TemplateResponse(request, template_name, locals())


def editar_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/editar_endereco.html'
    user = request.session['username']
    municipios = global_municipios
    zoneamentos = global_zoneamentos
    localizacao_diferenciada = ['', 'Terra Indígena', 'Quilombo', 'Área de Assentamento']

    id_endereco = request.GET.get('id')
    if id_endereco in (None, ''):
        return HttpResponseRedirect('/fundiria/index')

    endereco = Endereco.objects.get(id= id_endereco)
    if Detalhes_Indigena.objects.filter(escola= endereco.escola).exists():
        detalhes_indigenas = Detalhes_Indigena.objects.get(escola= endereco.escola)

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        etnias.append(detalhe['etnia'])

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        localizacoes.append(detalhe['localizacao'])

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        aldeias.append(detalhe['aldeia'])

    if request.method == 'POST':
        formulario_endereco(request)
        return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={endereco.escola.cod_inep}')

    return TemplateResponse(request, template_name, locals())


def editar_contatos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [19], True):
        return HttpResponseRedirect('/')

    template_name = 'fundiaria/editar-contatos.html'
    user = request.session['username']
    id_endereco = request.GET.get('id')
    edicao = True

    endereco = Endereco.objects.get(id= id_endereco)
    contatos = Contato.objects.filter(endereco= endereco)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        editar_contato(request, edicao)
        return HttpResponseRedirect(f'/fundiaria/fundiaria-perfil?inep={endereco.escola.cod_inep}')

    return TemplateResponse(request, template_name, locals())