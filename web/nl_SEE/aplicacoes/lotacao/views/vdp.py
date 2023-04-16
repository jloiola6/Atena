from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.servidor import *
from django.db.models import Sum


from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from aplicacoes.lotacao.filtros import *

from aplicacoes.usuario.models import Permissao
from aplicacoes.lotacao.exportar import *

def vdp_tabela(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [24]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/vdp/tabela-vdp.html'
    user = request.session['username'] 
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 24)

    vdp = filtro_vdp(request)
    quantidade_vdp = vdp.count()
    
    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(vdp, 15)
    vdp = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():

        gets = (request.get_full_path().split('?')[1])
        
        if 'page' not in gets:
            gets = f'page={page}&' + gets

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', gets_ultima)

    if request.method == 'POST':
        if request.POST.get('btn-exportar-vdp') == 'exportar':
            return exportar_pdf_vdp(request)

    return TemplateResponse(request, template_name, locals())


def anos_vdp(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [24]):
        return HttpResponseRedirect('/')

    vdps = []
    total_bruto =  Servidor_vdp.objects.values('ano_periodo').order_by('ano_periodo').annotate(total_bruto=Sum('valor_bruto'))
    for vdp in Servidor_vdp.objects.values_list('ano_periodo', flat= True).distinct():
        quantidade = Servidor_vdp.objects.filter(ano_periodo= vdp).count()
        for total in total_bruto:
            if total['ano_periodo'] == vdp:
                valor = ("{0:,}".format(total['total_bruto']).replace(',', '.'))[:-2]
        vdps.append((vdp, quantidade, valor))

    template_name = 'lotacao/vdp/anos-vdp.html'
    user = request.session['username'] 
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 24)

    return TemplateResponse(request, template_name, locals())