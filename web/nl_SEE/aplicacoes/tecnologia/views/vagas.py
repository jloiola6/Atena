from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.tecnologia.exportar import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.administracao.models import *
from aplicacoes.tecnologia.models import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.tecnologia.filtros import *



def central_vagas(request):
    if not verificacao_maxima(request, [20]) or verificar_manutencao():
        return HttpResponseRedirect('/')   

    template_name = 'tecnologia/vagas/vagas.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 20)

    # id_contratos = [] 
    # for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 11).values('contrato'):
    #     id_contratos.append(id['contrato'])

    # itens = Contrato_item.objects.filter(contrato__id__in= id_contratos, contrato__tipo_contrato = "Serviços")
    # itens = itens.exclude(contrato__empresa__cnpj= '07.928.901/0001-97')
 
    # for item in itens: 
    #     print(item)
    #     contrato = item.contrato
    #     servicos = Link.objects.filter(item= item, status= 'ATIVO')
    #     print(servicos)
    #     quantidade_servicos = servicos.count()
    #     quantidade = item.quantidade.replace('.', '')
    #     vagas_restantes = int(quantidade) - quantidade_servicos
            
    #     item.qtd_vagas = vagas_restantes
    #     if item.qtd_vagas == 0:
    #         item.vagas = 0
    #     else:
    #         item.vagas = 1
    #     item.save()

    itens = filtro_vagas(request)
    
    empresas = Contrato_empresa.objects.all().order_by('nome')
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
    gets_ultima = f'page={paginator.num_pages}'

    for item in itens:
        if(len(item.descricao) >= 100):
            item.descricao = item.descricao[0:99] + '...'
    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_vagas(request)

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
            gets_ultima = gets.replace(f'page={page}', f'page={gets_ultima}')
    
    return TemplateResponse(request, template_name, locals())

    