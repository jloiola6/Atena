from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.atena.models import * 
from aplicacoes.administracao.models import * 
from aplicacoes.lotacao.models import * 
from aplicacoes.terceirizacao.models import Contrato_lotacao 
from aplicacoes.terceirizacao.models import * 
from aplicacoes.usuario.models import * 
from aplicacoes.administracao.exportar import *
from aplicacoes.administracao.filtros import *
from aplicacoes.administracao.actions.contrato import *

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.contrato import *


def contratos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10]):
        return HttpResponseRedirect('/')
   
    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'administracao/contratos/contratos.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 10)

    # contratos = Contrato_contrato.objects.all()
    contratos = filtro_contratos(request)
    empresas = Contrato_empresa.objects.all()

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima 
    quantidade_contratos = contratos.count()
    paginator = Paginator(contratos, 15)
    contratos = paginator.get_page(page)

    
    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_contratos(request)

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        if len(gets.split('&')) > 1:
            #Paginação + filtros passados pela url
            proxima_pagina = str(int(page)+1)
            pagina_anterior = str(int(page)-1)

            gets = f'page={page}&' + gets

            gets_primeira = gets.replace(f'page={page}', 'page=1')
            gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
            gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
            gets_ultima = gets.replace(f'page={page}', gets_ultima)
    
    return TemplateResponse(request, template_name, locals())


def contrato_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    tipo_contrato = request.GET.get('tipo')
    if tipo_contrato == 'limpeza':
        template_name = 'administracao/contratos/contrato-limpeza-formulario.html'
    elif tipo_contrato == 'produto':
        template_name = 'administracao/contratos/contrato-produto-formulario.html'
    elif tipo_contrato == 'servico':
        template_name = 'administracao/contratos/contrato-servico-formulario.html'
    elif tipo_contrato == 'trabalho':
        template_name = 'administracao/contratos/contrato-trabalho-formulario.html'
    elif tipo_contrato == 'vigilante':
        template_name = 'administracao/contratos/contrato-vigilante-formulario.html'
    user = request.session['username']

    fontes = ('100 (RP)', '200 (RP)', '300 (RP)', '500 (RP)')
    empresas = Contrato_empresa.objects.all()
    unidades_administrativas = Unidade_administrativa.objects.all().exclude(categoria= 1).order_by('nome')

    if request.method == 'POST':
        contrato = formulario_contrato(request)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())

def contrato_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/contrato-perfil.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 10)
    
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)
        itens = Contrato_item.objects.filter(contrato = contrato, status= 1)
        empresa = contrato.empresa

        if Contrato_aditivo.objects.filter(contrato= contrato).exists():
            contrato_aditivo = Contrato_aditivo.objects.filter(contrato= contrato)
            ultimo_contrato = contrato_aditivo.last()
            quantidade_contrato_aditivo = contrato_aditivo.count()

        if Contrato_gestor.objects.filter(contrato= contrato).exists():
            gestores = Contrato_gestor.objects.filter(contrato= contrato)
            # quantidade_gestores = gestores.count()
        
        if Contrato_responsavel.objects.filter(contrato= contrato).exists():
            responsavel = Contrato_responsavel.objects.get(contrato= contrato)
        
        if Fonte_contrato.objects.filter(contrato= contrato).exists():
            fontes = Fonte_contrato.objects.filter(contrato= contrato)

            fontes_base = ('100 (RP)', '200 (RP)', '300 (RP)', '500 (RP)')
            contrato_fontes = fontes.distinct().values_list('fonte_recurso', flat= True)
            fontes_restantes = []
            for fonte in fontes_base:
                if fonte not in contrato_fontes:
                    fontes_restantes.append(fonte)

        if Contrato_documento.objects.filter(contrato= contrato).exists():
            documentos = Contrato_documento.objects.filter(contrato= contrato)
        
        
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def fonte_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/fonte-formulario.html'
    user = request.session['username']

    fontes_base = ('100 (RP)', '200 (RP)', '300 (RP)', '500 (RP)')
    
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)
        
        contrato_fontes = Fonte_contrato.objects.filter(contrato= contrato).distinct().values_list('fonte_recurso', flat= True)
        fontes = []
        for fonte in fontes_base:
            if fonte not in contrato_fontes:
                fontes.append(fonte)
        
        if fontes == []:
            return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={id_contrato}')


        if request.method == 'POST':
            formulario_fonte(request, contrato)
            return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={id_contrato}')
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def item_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/item-perfil.html'
    user = request.session['username']
    aplicacao = Servico.objects.get(id= 10).aplicacao.nome

    id_item = request.GET.get('id_item')
    if id_item != None:
        item = Contrato_item.objects.get(id = id_item)

        page = request.GET.get('page')
        if page is None:
            page = '1'

        contrato = item.contrato
        if contrato.tipo_contrato == 'Postos de trabalho - Vigilância Armada': 
            postos = Contrato_posto_vigilante.objects.filter(item= item)
            quantidade_postos = postos.count()
            vagas_restantes = int(item.quantidade) - quantidade_postos

            paginator = Paginator(postos, 15)
            postos = paginator.get_page(page)

            #Estabelecendo paginação da tabela
            gets_primeira = f'id_item={id_item}&page=1'
            gets_proxima = f'id_item={id_item}&page={str(int(page)+1)}'
            gets_anterior = f'id_item={id_item}&page={str(int(page)-1)}'
            gets_ultima = f'id_item={id_item}&page={paginator.num_pages}'

        elif 'Postos de trabalho' in contrato.tipo_contrato: 
            servidores = Contrato_lotacao.objects.filter(item= item, status= 1).order_by('servidor__nome')
            # servidores = Contrato_lotacao.objects.filter(item= item, status= 1)
            quantidade_servidores = servidores.count()

            if contrato.tipo_contrato == 'Postos de trabalho - Limpeza':
                if '.' in item.quantidade:
                    valor = str(item.quantidade).split('.')
                    novo_valor = str(int(valor[0]) - quantidade_servidores) + '.' + valor[1]
                    vagas_restantes = round(float(novo_valor) * int(item.metragem_contratada), 2)
                else:
                    vagas_restantes = ((int(item.quantidade) - quantidade_servidores) * item.metragem_contratada)
                
                if vagas_restantes == '':
                    vagas_restantes = 0
            else:
                vagas_restantes = int(item.quantidade) - quantidade_servidores


            paginator = Paginator(servidores, 15)
            servidores = paginator.get_page(page)

            #Estabelecendo paginação da tabela
            gets_primeira = f'id_item={id_item}&page=1'
            gets_proxima = f'id_item={id_item}&page={str(int(page)+1)}'
            gets_anterior = f'id_item={id_item}&page={str(int(page)-1)}'
            gets_ultima = f'id_item={id_item}&page={paginator.num_pages}'
        
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def contrato_aditivo_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/contrato-aditivo-perfil.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if Contrato_aditivo.objects.filter(id= id_contrato).exists():
        contrato_aditivo = Contrato_aditivo.objects.get(id= id_contrato)
        contrato = contrato_aditivo.contrato

        if Contrato_item_mudanca.objects.filter(contrato_aditivo= contrato_aditivo).exists():
            itens = Contrato_item_mudanca.objects.filter(contrato_aditivo= contrato_aditivo)
            quantidade_itens = itens.count()

    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def empresa_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/empresa-formulario.html'
    user = request.session['username']

    estados = Estado.objects.all().order_by('nome')
    cidades = Cidade.objects.all().order_by('nome')

    #Fazer tela de edição depois

    if request.method == 'POST':
        formulario_empresa(request)
        return HttpResponseRedirect(f'/administracao/contratos')

    return TemplateResponse(request, template_name, locals())


def contrato_aditivo_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/contrato-aditivo-formulario.html'
    user = request.session['username']

    #Fazer tela de edição depois
    tipo = request.GET.get('tipo')
    id_contrato = request.GET.get('id_contrato')

    if id_contrato != None:
        tipo_inativar = ('Aditivo', 'Supressão')
        contrato = Contrato_contrato.objects.get(id= id_contrato)
        itens = Contrato_item.objects.filter(contrato= contrato, status= 1)

        if Contrato_aditivo.objects.filter(contrato= contrato).exists():
            ultimo_aditivo = Contrato_aditivo.objects.filter(contrato= contrato).last()
            data_final = data_termino = str(ultimo_aditivo.data_termino)
        else:
            data_termino = data_final = str(contrato.data_termino)

        if tipo == 'Aditivo':
            ano_termino = str(int(str(data_final)[:4]) + 1)
            data_final = ano_termino + data_final[4:]

    if request.method == 'POST':
        formulario_contrato_aditivo(request, data_final, contrato, tipo)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def gestores_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/gestores-formulario.html'
    user = request.session['username']

    servidores = Servidor_lotacao.objects.filter(unidade_adm__isnull= False).values('contrato__servidor__nome').order_by('contrato__servidor__nome')

    #Fazer tela de edição depois
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)

    if request.method == 'POST':
        formulario_gestores(request, contrato)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def fiscais_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/fiscais-formulario.html'
    user = request.session['username']

    #Fazer tela de edição depois
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        servidores = Servidor_lotacao.objects.filter(unidade_adm__isnull= False).values('contrato__servidor__nome').order_by('contrato__servidor__nome')
        contrato = Contrato_contrato.objects.get(id= id_contrato)
        # atribuicoes = ('Fiscal Titular', 'Fiscal Substituto')

    if request.method == 'POST':
        formulario_fiscais(request, contrato)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def responsavel_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/responsavel-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)
    
    if request.method == 'POST':
        formulario_responsavel(request, contrato)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def postos_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/postos-formulario.html'
    user = request.session['username']

    endrecos = Endereco.objects.all()
    unidades_administrativas = Unidade_administrativa.objects.all().exclude(id= 1)

    id_item = request.GET.get('id_item')
    if id_item != None:
        item = Contrato_item.objects.get(id = id_item)
        contrato = item.contrato
    
    if request.method == 'POST':
        formulario_postos(request, item)
        return HttpResponseRedirect(f'/administracao/item-perfil?id_item={item.id}')

    return TemplateResponse(request, template_name, locals())


def vigilantes_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/vigilantes-formulario.html'
    
    id_posto = request.GET.get('id_posto')
    if id_posto != None:
        posto = Contrato_posto_vigilante.objects.get(id = id_posto)
        item = posto.item
    else:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        formulario_postos_funcionario(request, posto)
        return HttpResponseRedirect(f'/administracao/item-perfil?id_item={item.id}')

    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/documento-formulario.html'
    user = request.session['username']

    
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)
                    
        if request.method == 'POST' and request.FILES.get('arquivo'):
            formulario_documento(request, contrato)
            return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={id_contrato}')
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def fonte_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/fonte-perfil.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 10)
    aplicacao = Servico.objects.get(id= 10).aplicacao.nome

    id_fonte = request.GET.get('id_fonte')
    if id_fonte != None:
        fonte = Fonte_contrato.objects.get(id= id_fonte)
        contrato = fonte.contrato

    if Contrato_empenho.objects.filter(fonte_id= id_fonte).exists():
        empenhos = Contrato_empenho.objects.filter(fonte_id= id_fonte)
        count = empenhos.count()

        page = request.GET.get('page')
        if page is None:
            page = 1

        paginator = Paginator(empenhos, 15)
        empenhos = paginator.get_page(page)

        #Estabelecendo paginação da tabela
        gets_primeira = 'page=1'
        proxima_pagina = f'page={str(int(page)+1)}'
        pagina_anterior = f'page={str(int(page)-1)}'
        ultima_pagina = f'page={paginator.num_pages}'

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
            gets_ultima = gets.replace(f'page={page}', ultima_pagina)

    return TemplateResponse(request, template_name, locals())


def empenho_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contratos/empenho-formulario.html'
    user = request.session['username']

    id_fonte = request.GET.get('id_fonte')
    if id_fonte != None:
        fonte = Fonte_contrato.objects.get(id= id_fonte)
        contrato = fonte.contrato

        if request.method == 'POST':
            formulario_empenho(request, fonte, contrato)
            return HttpResponseRedirect(f'/administracao/fonte-perfil?id_fonte={id_fonte}')
       

    return TemplateResponse(request, template_name, locals())
