from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.administracao.models import *
from aplicacoes.atena.models import Cidade
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.models import *
from aplicacoes.terceirizacao.actions.contrato import *
from aplicacoes.core.filtros_gerais.contrato import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.usuario.models import *
from aplicacoes.tecnologia.models import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.terceirizacao.exportar import exportar_excel_contratos
from aplicacoes.administracao.exportar import exportar_excel_contratos_adm, exportar_pdf_contratos
from aplicacoes.tecnologia.exportar import exportar_excel_contratos_tec, exportar_pdf_contratos_tec
from aplicacoes.core.geral_actions.contrato import *


def descobrir_aplicacao(request, template):
    url = request.get_full_path()
    if 'terceirizacao' in url:
        lista = [16]
        nome_aplicacao = url.split('/')[1]
        template = template.replace('aplicacao', nome_aplicacao)
        vinculo = 78
    elif 'administracao' in url:
        lista = [10]
        nome_aplicacao = url.split('/')[1]
        template = template.replace('aplicacao', nome_aplicacao)
        vinculo = None
    elif 'tecnologia' in url:
        lista = [13]
        nome_aplicacao = url.split('/')[1]
        template = template.replace('aplicacao', nome_aplicacao)
        vinculo = 11
    return lista, template, nome_aplicacao, vinculo


def contratos(request):
    template_name = 'aplicacao/contrato/contratos.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= permissoes[0])

    contratos = filtro_contratos(request, vinculo)
    quantidade_contratos = contratos.count()

    if vinculo == None:
        empresas = Contrato_empresa.objects.all().values('id','nome').distinct()
    else:
        id_contratos = []
        for id in Vinculacao_contrato.objects.filter(unidade_administrativa= vinculo).values('contrato'):
            id_contratos.append(id['contrato'])

        empresas = []
        id_empresas = []
        for i in Contrato_contrato.objects.filter(id__in= id_contratos).values('empresa__id','empresa__nome').distinct():
            if i['empresa__id'] not in id_empresas:
                empresas.append((i['empresa__id'], i['empresa__nome']))
                id_empresas.append(i['empresa__nome'])

    gestor_titular = request.GET.get('gestor')
    gestores= Contrato_gestor.objects.filter().values('gestor_titular', 'gestor_substituto', 'fiscal_titular', 'fiscal_substituto')

    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(contratos, 15)
    contratos = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    url = request.get_full_path()
    if request.method == 'POST':
        if 'administracao' in url:
            if request.POST.get('exportar-fieldset-formatos') == 'excel':
                return exportar_excel_contratos_adm(request, vinculo, gestor_titular)
        if 'terceirizacao' in url:
            if request.POST.get('exportar-fieldset-formatos') == 'excel':
                return exportar_excel_contratos(request, vinculo)
        if 'tecnologia' in url:
            if request.POST.get('exportar-fieldset-formatos') == 'excel':
                return exportar_excel_contratos_tec(request)
            if request.POST.get('exportar-fieldset-formatos') == 'pdf':
                return exportar_pdf_contratos_tec(request)

        if request.POST.get('exportar-fieldset-formatos') == 'pdf_adm':
            return exportar_pdf_contratos(request, vinculo, gestor_titular)


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


def contrato_perfil(request):
    template_name = 'aplicacao/contrato/contrato-perfil.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= permissoes[0])
    aplicacao = str(permissao.servico.aplicacao)

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
            gestores = Contrato_gestor.objects.get(contrato= contrato)

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
    template_name = 'aplicacao/contrato/fonte-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

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
            return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={id_contrato}')

        if request.method == 'POST':
            formulario_fonte(request, contrato)
            return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={id_contrato}')
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def item_perfil(request):
    template_name = 'aplicacao/contrato/item-perfil.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    aplicacao = Servico.objects.get(id= permissoes[0]).aplicacao.nome
    id_item = request.GET.get('id_item')

    links = Link.objects.filter(item= id_item, status= 'ATIVO').values('id', 'unidade_educacional__escola__cod_inep', 'unidade_educacional__escola__nome_escola', 'departamento__sigla', 'departamento__nome', 'tipo', 'fornecedor', 'operadora', 'tipo_banda', 'circuito', 'velocidade', 'status', 'item').order_by('-id')
    quantidade_links = links.count()

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
            quantidade_servidores = servidores.count()

            if contrato.tipo_contrato != 'Postos de trabalho - Limpeza':
                vagas_restantes = int(item.quantidade) - quantidade_servidores
            #     if '.' in item.quantidade:
            #         valor = str(item.quantidade).split('.')
            #         novo_valor = str(item.qtd_vagas) + '.' + valor[1]
            #         vagas_restantes = round(float(novo_valor) * int(item.metragem_contratada), 2)
            #     else:
            #         vagas_restantes = item.qtd_vagas * int(item.metragem_contratada)

            #     if vagas_restantes == '':
            #         vagas_restantes = 0
            # else:

            paginator = Paginator(servidores, 15)
            servidores = paginator.get_page(page)

            #Estabelecendo paginação da tabela
            gets_primeira = f'id_item={id_item}&page=1'
            gets_proxima = f'id_item={id_item}&page={str(int(page)+1)}'
            gets_anterior = f'id_item={id_item}&page={str(int(page)-1)}'
            gets_ultima = f'id_item={id_item}&page={paginator.num_pages}'

        elif 'Serviços' in contrato.tipo_contrato:
            vagas_restantes = int(item.quantidade) - quantidade_links

            paginator = Paginator(links, 15)
            links = paginator.get_page(page)

            #Estabelecendo paginação da tabela
            gets_primeira = f'id_item={id_item}&page=1'
            gets_proxima = f'id_item={id_item}&page={str(int(page)+1)}'
            gets_anterior = f'id_item={id_item}&page={str(int(page)-1)}'
            gets_ultima = f'id_item={id_item}&page={paginator.num_pages}'

    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def contrato_aditivo_perfil(request):
    template_name = 'aplicacao/contrato/contrato-aditivo-perfil.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= permissoes[0])

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


def contrato_aditivo_formulario(request):
    template_name = 'aplicacao/contrato/contrato-aditivo-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    print('T: ', template_name)
    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    tipo = request.GET.get('tipo')
    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)
        itens = Contrato_item.objects.filter(contrato= contrato, status= 1)

        if contrato.data_aditivo == None:
            data_termino = str(contrato.data_termino)
        else:
            data_termino = str(contrato.data_aditivo)

        ano_termino = str(int(str(data_termino)[:4]) + 1)
        data_final = ano_termino + data_termino[4:]

    if request.method == 'POST':
        if contrato.data_aditivo != None:
            data_final = contrato.data_aditivo
        formulario_contrato_aditivo(request, data_final, contrato, tipo)
        return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def gestores_formulario(request):
    template_name = 'aplicacao/contrato/gestores-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        servidores = Servidor_lotacao.objects.filter(unidade_adm__isnull= False).values('contrato__servidor__nome').order_by('contrato__servidor__nome')
        contrato = Contrato_contrato.objects.get(id= id_contrato)

    if request.method == 'POST':
        formulario_gestores(request, contrato)
        return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def fiscais_formulario(request):
    template_name = 'aplicacao/contrato/fiscais-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        servidores = Servidor_lotacao.objects.filter(unidade_adm__isnull= False).values('contrato__servidor__nome').order_by('contrato__servidor__nome')
        contrato = Contrato_contrato.objects.get(id= id_contrato)

    if request.method == 'POST':
        formulario_fiscais(request, contrato)
        return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def responsavel_formulario(request):
    template_name = 'aplicacao/contrato/responsavel-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    estados = Estado.objects.all().order_by('nome')
    cidades = Cidade.objects.all().order_by('estado__nome')

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)

    if request.method == 'POST':
        formulario_responsavel(request, contrato)
        return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def postos_formulario(request):
    template_name = 'aplicacao/contrato/postos-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    endrecos = Endereco.objects.all()
    unidades_administrativas = Unidade_administrativa.objects.all().exclude(id= 1)

    id_item = request.GET.get('id_item')
    if id_item != None:
        item = Contrato_item.objects.get(id = id_item)
        contrato = item.contrato

    if request.method == 'POST':
        formulario_postos(request, item)
        return HttpResponseRedirect(f'/{nome_aplicacao}/item_perfil?id_item={item.id}')

    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    template_name = 'aplicacao/contrato/documento-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Contrato_contrato.objects.get(id= id_contrato)

        if request.method == 'POST' and request.FILES.get('arquivo'):
            formulario_documento(request, contrato)
            return HttpResponseRedirect(f'/{nome_aplicacao}/contrato-perfil?id_contrato={id_contrato}')
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def fonte_perfil(request):
    template_name = 'aplicacao/contrato/fonte-perfil.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= permissoes[0])
    aplicacao = str(permissao.servico.aplicacao)

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
    template_name = 'aplicacao/contrato/empenho-formulario.html'
    permissoes, template_name, nome_aplicacao, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    id_fonte = request.GET.get('id_fonte')
    if id_fonte != None:
        fonte = Fonte_contrato.objects.get(id= id_fonte)
        contrato = fonte.contrato

        if request.method == 'POST':
            formulario_empenho(request, fonte, contrato)
            return HttpResponseRedirect(f'/{nome_aplicacao}/fonte-perfil?id_fonte={id_fonte}')

    return TemplateResponse(request, template_name, locals())