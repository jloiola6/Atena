from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.administracao.models import * 
from aplicacoes.administracao.relatorio import render_to_pdf
from aplicacoes.atena.models import Cidade

from aplicacoes.terceirizacao.exportar import *
from aplicacoes.administracao.actions.unidades_administrativas import *
from aplicacoes.administracao.filtros import *
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.lotacao.models import Servidor_lotacao
from aplicacoes.terceirizacao.models import Contrato_lotacao
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao, global_municipios, global_zoneamentos
from aplicacoes.administracao.exportar import exportar_pdf_servidor_lotado


def unidades_administrativas(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')
   
    template_name = 'administracao/unidades-administrativas/unidades.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    secretaria = Unidade_administrativa.objects.get(categoria= 1)
    endereco = Unidade_administrativa_endereco.objects.get(id= 1)

    unidades = Unidade_administrativa.objects.all().exclude(categoria= 1)

    diretorias = unidades.filter(categoria= 2)
    departamentos = unidades.filter(categoria= 3)
    divisoes = unidades.filter(categoria= 4)
    nucleos = unidades.filter(categoria= 5)
    centros = unidades.filter(categoria= 6)

    return TemplateResponse(request, template_name, locals())


def diretoria(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/diretoria.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)
    aplicacao = 'administracao'

    id_unidade= request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)
    endereco = unidade.endereco


    servidores = Servidor_lotacao.objects.filter(unidade_adm = unidade, status= 1)
    qtd_servidores = servidores.count()

    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa= unidade, status= 1)
    qtd_servidores_terceirizados = servidores_terceirizados.count()

    possui_departamentos = Unidade_administrativa.objects.filter(hierarquia= unidade.id).exists()
    if possui_departamentos:
        departamentos = Unidade_administrativa.objects.filter(categoria = 3, hierarquia= unidade.id)
        divisoes = Unidade_administrativa.objects.filter(categoria= 4)
        nucleos = Unidade_administrativa.objects.filter(categoria= 5)
        centros = Unidade_administrativa.objects.filter(categoria= 6)

    return TemplateResponse(request, template_name, locals())


def departamento(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/departamento.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)
    aplicacao = 'administracao'

    id_unidade= request.GET.get('id')

    unidade = Unidade_administrativa.objects.get(id= id_unidade)
    diretoria = Unidade_administrativa.objects.get(id= unidade.hierarquia)
    endereco = unidade.endereco

    servidores = Servidor_lotacao.objects.filter(unidade_adm = unidade, status= 1)
    qtd_servidores = servidores.count()

    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa = unidade, status= 1)
    qtd_servidores_terceirizados = servidores_terceirizados.count()

    possui_divisoes = Unidade_administrativa.objects.filter(hierarquia= unidade.id).exists()

    if possui_divisoes:
        divisoes = Unidade_administrativa.objects.filter(hierarquia= unidade.id)
        nucleos = Unidade_administrativa.objects.filter(categoria= 5)
        centros = Unidade_administrativa.objects.filter(categoria= 6)

    return TemplateResponse(request, template_name, locals())


def divisao(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/divisao.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)
    aplicacao = 'administracao'

    id_unidade= request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    departamento = Unidade_administrativa.objects.get(id= unidade.hierarquia)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)
    endereco = unidade.endereco

    servidores = Servidor_lotacao.objects.filter(unidade_adm = unidade, status= 1)
    qtd_servidores = servidores.count()
    
    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa = unidade, status= 1)
    qtd_servidores_terceirizados = servidores_terceirizados.count()

    possui_nucleos = Unidade_administrativa.objects.filter(hierarquia= unidade.id).exists()
    
    if possui_nucleos:
        nucleos = Unidade_administrativa.objects.filter(hierarquia= unidade.id)
        centros = Unidade_administrativa.objects.filter(categoria= 6)

    return TemplateResponse(request, template_name, locals())


def nucleo(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/nucleo.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    id_unidade = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    divisao = Unidade_administrativa.objects.get(id= unidade.hierarquia)
    departamento = Unidade_administrativa.objects.get(id= divisao.hierarquia)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)
    endereco = unidade.endereco

    servidores = Servidor_lotacao.objects.filter(unidade_adm = unidade, status= 1)
    qtd_servidores = servidores.count()
    
    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa = unidade, status= 1)
    qtd_servidores_terceirizados = servidores_terceirizados.count()

    possui_centros = Unidade_administrativa.objects.filter(hierarquia= unidade.id).exists()
    if possui_centros:
        centros = Unidade_administrativa.objects.filter(hierarquia= unidade.id)

    return TemplateResponse(request, template_name, locals())


def centro(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/centro.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)
    aplicacao = 'administracao'

    id_unidade = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    nucleo = Unidade_administrativa.objects.get(id= unidade.hierarquia)
    divisao = Unidade_administrativa.objects.get(id= nucleo.hierarquia)
    departamento = Unidade_administrativa.objects.get(id= divisao.hierarquia)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)
    endereco = unidade.endereco

    servidores = Servidor_lotacao.objects.filter(unidade_adm = unidade, status= 1)
    qtd_servidores = servidores.count()
    
    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa = unidade, status= 1)
    qtd_servidores_terceirizados = servidores_terceirizados.count()


    return TemplateResponse(request, template_name, locals())


def departamento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/departamento-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    id_diretoria= request.GET.get('id')
    diretoria = Unidade_administrativa.objects.get(id= id_diretoria)

    municipios = Cidade.objects.filter(estado__id= 1)

    if request.method == 'POST':
        formulario_departamento(request)
        return HttpResponseRedirect(f'/administracao/diretoria?id={id_diretoria}')

    return TemplateResponse(request, template_name, locals())


def divisao_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades-administrativas/divisao-formulario.html'
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    id_departamento= request.GET.get('id')
    departamento = Unidade_administrativa.objects.get(id= id_departamento)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)
    
    municipios = Cidade.objects.filter(estado__id= 1)

    if request.method == 'POST':
        formulario_divisao(request)
        return HttpResponseRedirect(f'/administracao/departamento?id={id_departamento}')

    return TemplateResponse(request, template_name, locals())


def nucleo_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/nucleo-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    id_divisao= request.GET.get('id')
    divisao = Unidade_administrativa.objects.get(id= id_divisao)
    departamento = Unidade_administrativa.objects.get(id= divisao.hierarquia)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)

    municipios = Cidade.objects.filter(estado__id= 1)

    if request.method == 'POST':
        formulario_nucleo(request)
        return HttpResponseRedirect(f'/administracao/divisao?id={id_divisao}')


    return TemplateResponse(request, template_name, locals())


def polo_centro_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/polo-centro-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    id_nucleo= request.GET.get('id')
    nucleo = Unidade_administrativa.objects.get(id= id_nucleo)
    divisao = Unidade_administrativa.objects.get(id= nucleo.hierarquia)
    departamento = Unidade_administrativa.objects.get(id= divisao.hierarquia)
    diretoria = Unidade_administrativa.objects.get(id= departamento.hierarquia)

    municipios = Cidade.objects.filter(estado__id= 1)

    if request.method == 'POST':
        formulario_polo_centro(request)
        return HttpResponseRedirect(f'/administracao/nucleo?id={id_nucleo}')


    return TemplateResponse(request, template_name, locals())

# def servidores_lotados(request):
#     if verificar_manutencao():
#         return HttpResponseRedirect('/')   

#     if not verificacao_maxima(request, [2]):
#         return HttpResponseRedirect('/')

#     template_name = 'administracao/unidades-administrativas/servidores-lotados.html'
#     user = request.session['username']

#     if request.GET.get('pdf'):
#         render_to_pdf('administracao/unidades-administrativas/servidores-lotados.html')

#     id_unidade = request.GET.get('id')
#     unidade = Unidade_administrativa.objects.get(id= id_unidade)

#     servidores = filtro_servidores(request)
#     quantidade_servidores = len(servidores)


#     #Coleta a página atual para atualzar informações na tabela
#     page = request.GET.get('page')
#     if page is None:
#         page = '1'

#     paginator = Paginator(servidores, 15)
#     servidores = paginator.get_page(page)
    
#     #Estabelecendo paginação da tabela
#     gets_primeira = 'id={id_unidade}&page=1'
#     gets_proxima = f'id={id_unidade}&page={str(int(page)+1)}'
#     gets_anterior = f'id={id_unidade}&page={str(int(page)-1)}'
#     gets_ultima = f'id={id_unidade}&page={paginator.num_pages}'


#     return TemplateResponse(request, template_name, locals())


def servidores_lotados(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades-administrativas/servidores-lotados.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 2)

    # if request.GET.get('pdf'):
    #     render_to_pdf('administracao/unidades-administrativas/servidores-lotados.html')

    id_unidade = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    servidores = filtro_servidores(request, id_unidade)
    quantidade_servidores = len(servidores)

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    paginator = Paginator(servidores, 15)
    servidores = paginator.get_page(page)
    
    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    proxima_pagina = f'page={str(int(page)+1)}'
    pagina_anterior = f'page={str(int(page)-1)}'
    pagina_ultima = f'page={paginator.num_pages}'

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_servidor_lotado(request)

        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_servidor_lotado(request, id_unidade)

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])
        
        if 'page' not in gets:
            gets = f'page={page}&' + gets
        # if len(gets.split('&')) > 1:
            #Paginação + filtros passados pela url
        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        # gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', pagina_ultima)
 

    return TemplateResponse(request, template_name, locals())


def editar_endereco_adm(request):
    if verificar_manutencao() or not verificacao_maxima(request, [2], True):
        return HttpResponseRedirect('/')
        
    template_name = 'administracao/unidades-administrativas/editar-endereco.html'
    user = request.session['username']

    municipios = global_municipios
    zoneamentos = global_zoneamentos

    id = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id)
    
    # if id_endereco in (None, ''):
    #     return HttpResponseRedirect('/fundiria/index')

    # endereco = Endereco.objects.get(id= id)
    
    if request.method == 'POST':
        endereco_editar(request)
        return HttpResponseRedirect(f'/administracao/departamento?id={unidade.id}')

    return TemplateResponse(request, template_name, locals())