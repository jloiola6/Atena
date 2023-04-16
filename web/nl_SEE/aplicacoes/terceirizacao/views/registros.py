from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.core.models import *
from aplicacoes.atena.models import *
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from aplicacoes.usuario.models import Permissao
from aplicacoes.terceirizacao.models import *
from aplicacoes.administracao.models import *

def registro_lotacoes(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [35]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/registro/registro-lotacoes.html'
    user = request.session['username']

    dados = []
    historico = Historico.objects.filter(tabela = 'terceirizacao_contrato_lotacao').values('objeto', 'log__usuario__id', 'data', 'log__usuario__nome').order_by('-objeto')

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    historico_aux = historico[valor_paginacao-15:valor_paginacao]

    for aux in historico_aux:
        nomeServidor = Contrato_lotacao.objects.filter(id = aux['objeto']).values_list('item__contrato__numero_contrato', 'servidor__nome', 'endereco__municipio', 'unidade_administrativa__nome', 'endereco__escola__nome_escola')
        for aux2 in nomeServidor:
            if aux2[3] != None and aux2[3] != '':
                dados.append((aux2[0], aux2[1], aux2[3], aux2[2], aux['log__usuario__nome'], aux['data']))
            else:
                dados.append((aux2[0], aux2[1], aux2[4], aux2[2], aux['log__usuario__nome'], aux['data']))
    qtd_lotacao = len(historico)


    paginator = Paginator(historico, 15)
    historico = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

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