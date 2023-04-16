from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.terceirizacao.exportar import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.administracao.models import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.terceirizacao.filtros import *


def central_vagas(request):
    if verificar_manutencao() or not verificacao_maxima(request, [18]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/vagas/vagas.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 18)
    permissao_contrato = Permissao.objects.filter(usuario__login= user, servico__id= 16).exists()

    # id_contratos = [] 
    # for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 78).values('contrato'):
    #     id_contratos.append(id['contrato'])

    # itens = Contrato_item.objects.filter(contrato__id__in= id_contratos) 
    # for item in itens: 
    #     contrato = item.contrato
    #     if contrato.tipo_contrato == 'Postos de trabalho - Vigilância Armada': 
    #         postos = Contrato_posto_vigilante.objects.filter(item= item)
    #         quantidade_postos = postos.count()
    #         vagas_restantes = int(item.quantidade) - quantidade_postos  
    #     elif 'Postos de trabalho' in contrato.tipo_contrato: 
    #         servidores = Contrato_lotacao.objects.filter(item= item, status= 1)
    #         quantidade_servidores = servidores.count()
    #         if '.' in item.quantidade:
    #             quantidade = item.quantidade.split('.')
    #             vagas_restantes = str(int(quantidade[0]) - quantidade_servidores) + quantidade[1]
    #         else:
    #             vagas_restantes = int(item.quantidade) - quantidade_servidores
            
    #     item.qtd_vagas = vagas_restantes
    #     if item.qtd_vagas == 0:
    #         item.vagas = 0
    #     else:
    #         item.vagas = 1
    #     item.save()
    itens = filtro_vagas(request)
    
    id_contratos = [] 
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 78).values('contrato'):
        id_contratos.append(id['contrato'])

    #Alterar dps
    empresas = []
    nomes_empresas = []
    for i in Contrato_contrato.objects.filter(id__in= id_contratos).values('empresa__id','empresa__nome'):
        if i['empresa__nome'] not in nomes_empresas:
            empresas.append((i['empresa__id'], i['empresa__nome']))
            nomes_empresas.append(i['empresa__nome'])

    qtd_itens = itens.count()
    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(itens, 15)
    itens = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = paginator.num_pages

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_vagas(request)

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
        gets_ultima = gets.replace(f'page={page}', f'page={gets_ultima}')
    
    return TemplateResponse(request, template_name, locals())

    