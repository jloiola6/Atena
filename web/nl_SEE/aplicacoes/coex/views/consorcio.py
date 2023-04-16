from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.coex.models import *
from aplicacoes.administracao.models import *
from aplicacoes.coex.actions.consorcio import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao

def consorcio(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'coex/consorcio/consorcios.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    nome_consorcio = request.GET.get("nome_consorcio")
    cnpj_consorcio = request.GET.get("cnpj")

    consorcios = Consorcio.objects.all()

    if nome_consorcio != '' and nome_consorcio != None:
        consorcios = consorcios.filter(nome_consorcio__icontains= nome_consorcio)

    if cnpj_consorcio != '' and cnpj_consorcio != None:
        consorcios = consorcios.filter(cnpj= cnpj_consorcio)

    busca_consorcio = Consorcio.objects.all().values('nome_consorcio')

    page = request.GET.get('page')
    if page is None:
        page = '1'

    quantidade_consorcios = len(consorcios)
    paginator = Paginator(consorcios, 15)
    consorcios = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if not 'page' in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', gets_primeira)
        gets_proxima = gets.replace(f'page={page}', gets_proxima)
        gets_anterior = gets.replace(f'page={page}', gets_anterior)
        gets_ultima = gets.replace(f'page={page}', gets_ultima)

    return TemplateResponse(request, template_name, locals())


def consorcio_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/consorcio-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)
    edicao = False

    escola_coex = Coex.objects.values_list('escola__id', flat = True)
    escolas_id = Escola.objects.all().exclude(id__in= escola_coex).values_list('id', flat= True).exclude(id__in=[669, 722, 738, 740])
    escolas = Endereco.objects.filter(id__in= escolas_id, tipo='S').values('escola__id', 'escola__nome_escola', 'municipio', 'escola__cod_inep')

    id_consorcio = request.GET.get('id')
    if id_consorcio != None and id_consorcio != '':
        if Consorcio.objects.filter(id= id_consorcio).exists():
            consorcio = Consorcio.objects.get(id= id_consorcio)
            edicao = True

            equipe_presidente = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
            equipe_tesoureiro = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
            equipe_secretario1 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 1').values('nome').last()
            equipe_secretario2 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 2').values('nome').last()
            equipe_secretario3 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 3').values('nome').last()
            equipe_secretario4 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 4').values('nome').last()

            possui_equipe = Equipe_comite.objects.filter(consorcio= consorcio).exists()

    if request.method == "POST":
        id_consorcio = formulario_consorcio(request, edicao)
        return HttpResponseRedirect(f'/coex/consorcio-perfil?id={id_consorcio}')

    return TemplateResponse(request, template_name, locals())


def consorcio_perfil(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/consorcio-perfil.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_consorcio = request.GET.get("id")
    consorcio = Consorcio.objects.get(id = id_consorcio)

    escolas_id = Escola_consorcio.objects.filter(consorcio= id_consorcio, status=1).values_list("escola__id", flat= True)
    escolas = Endereco.objects.filter(escola__id__in= escolas_id, tipo= 'S').values("escola__id", "escola__cod_inep", "escola__nome_escola", "municipio")
    qtd_escolas = escolas.count()

    coex = Coex.objects.filter(escola__in= escolas_id, status=1)
    qr_arquivo = Arquivo_consorcio.objects.filter(consorcio = consorcio)
    print(qr_arquivo)

    possui_equipe = Equipe_comite.objects.filter(consorcio= consorcio).exists()

    if possui_equipe:
        equipe_presidente = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 4').values('nome').last()

    qtd_documentos = 0

    if Arquivo_consorcio.objects.filter(consorcio = consorcio).exists():
        qtd_documentos = Arquivo_consorcio.objects.filter(consorcio = consorcio).count()
        qr_documentos = Arquivo_consorcio.objects.filter(consorcio = consorcio)[:3]

        documentos = []
        for documento in qr_documentos:
            formato_documento = str(documento.arquivo).split('.')[1]
            caminho = str(documento.path_arquivo())
            dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
            documentos.append(dict_documento)

    if 'btn-excluir' in request.POST:
        valor = request.POST.get('btn-excluir')
        id_documento = valor.split('-')[-1]
        coex_excluir_consorcio(request, id_documento)
        return HttpResponseRedirect(f'/coex/consorcio-perfil?id={consorcio.id}')


    return TemplateResponse(request, template_name, locals())


def vincular_escola(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/vincular-escola.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_consorcio = request.GET.get("id")
    consorcio = Consorcio.objects.get(id = id_consorcio)

    escola_coex = Coex.objects.filter(status=1).values_list('escola__id', flat = True)
    escolas_id = Escola.objects.all().exclude(id__in= escola_coex).values_list('id', flat= True)
    escolas = Endereco.objects.filter(id__in= escolas_id, tipo='S').values('escola__id', 'escola__nome_escola', 'municipio', 'escola__cod_inep')

    if request.method == "POST":
        vinculo_escola(request)
        return HttpResponseRedirect(f'/coex/consorcio-perfil?id={id_consorcio}')

    return TemplateResponse(request, template_name, locals())


def desvincular_escola(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/desvincular-escola.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_consorcio = request.GET.get("id")
    consorcio = Consorcio.objects.get(id = id_consorcio)
    escolas = Escola_consorcio.objects.filter(consorcio= consorcio, status=1).values('escola__id', 'escola__cod_inep', 'escola__nome_escola')

    if request.method == "POST":
        desvinculo_escola(request, consorcio)
        return HttpResponseRedirect(f'/coex/consorcio-perfil?id={id_consorcio}')

    return TemplateResponse(request, template_name, locals())


def formulario_documento_consorcio(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/documento-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_consorcio = request.GET.get("id")
    escola_consorcio = Escola_consorcio.objects.filter(id = id_consorcio, status= 1)
    consorcio = Consorcio.objects.get(id= id_consorcio)
    qr_documentos = Arquivo_consorcio.objects.filter(consorcio = consorcio).values('id').count()

    categorias = ["ATA's","Documentos Pessoais","Edital","Estatuto","Lista de presença","Requerimento","Outros"]

    if request.method == "POST":
        consorcio_documento(request, consorcio)
        if qr_documentos > 3:
            return HttpResponseRedirect(f'/coex/consorcio-perfil?id={id_consorcio}')
        else:
            return HttpResponseRedirect(f'/coex/gerenciador-documentos-consorcio?id={id_consorcio}')

    return TemplateResponse(request, template_name, locals())


def gerenciador_documentos_consorcio(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    template_name = 'coex/consorcio/gerenciador-documentos-consorcio.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id = request.GET.get("id")
    consorcio = Consorcio.objects.get(id = id)

    qr_documentos = Arquivo_consorcio.objects.filter(consorcio = consorcio)

    documentos = []
    pessoais = []
    ata = []
    estatuto = []
    requerimento = []
    edital = []
    presenca = []
    outros = []

    for documento in qr_documentos:
        formato_documento = str(documento.arquivo).split('.')[1]
        caminho = str(documento.path_arquivo())
        dict_documento = {'id': documento.id, 'descricao': documento.descricao, 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
        documentos.append(dict_documento)

        if dict_documento['categoria'] == "ATA's":
            ata.append(dict_documento)
        elif dict_documento['categoria'] == "Documentos Pessoais":
            pessoais.append(dict_documento)
        elif dict_documento['categoria'] == "Edital":
            edital.append(dict_documento)
        elif dict_documento['categoria'] == "Estatuto":
            estatuto.append(dict_documento)
        elif dict_documento['categoria'] == "Lista de presença":
            presenca.append(dict_documento)
        elif dict_documento['categoria'] == "Requerimento":
            requerimento.append(dict_documento)
        elif dict_documento['categoria'] == "Outros":
            outros.append(dict_documento)

    if 'btn-excluir' in request.POST:
        valor = request.POST.get('btn-excluir')
        id_documento = valor.split('-')[-1]
        coex_excluir_consorcio(request, id_documento)

        return HttpResponseRedirect(f'/coex/gerenciador-documentos-consorcio?id={consorcio.id}')

    return TemplateResponse(request, template_name, locals())