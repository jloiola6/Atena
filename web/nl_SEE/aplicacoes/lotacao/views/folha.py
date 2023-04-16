from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.core.models import *
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from aplicacoes.usuario.models import Permissao
from aplicacoes.lotacao.exportar import *

def folha_pagamento(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [34]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/folha/folha-pagamento.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 34)


    page = request.GET.get('page')
    if page is None:
        page = 1
    contratos_aux = []
    contratos_id = []
    servidores = filtro_folha(request)
    valor_paginacao = 15 * int(page)
    servidores_aux = servidores[valor_paginacao - 15: valor_paginacao]
    cargos_id = []
    cargos_id1 = []
    referencia = [i for i in range(1, 11)]

    # Melhorar isso depois
    for servidor in servidores_aux:
        if Servidor_lotacao.objects.filter(contrato_id = servidor['id']).exists():
            contratos_aux.append((Servidor_lotacao.objects.filter(contrato_id = servidor['id'], status = 1).values('id')))
    for ids in contratos_aux:
        for id in ids:
            contratos_id.append(id['id'])
    contratos = Servidor_lotacao.objects.filter(id__in = contratos_id).values('contrato_id', 'carga_horaria', 'funcao', 'tipo_lotacao').order_by('contrato__servidor__nome')
    contratos_aux = []
    for contrato in contratos:
        contratos_aux.append(contrato['contrato_id'])

    for id_cargos in servidores_aux:
        cargos_id.append(id_cargos['cargo_id'])
    cargos = Cargo_vencimento.objects.filter(cargo_id__in = cargos_id, ref = 1)

    for id_cargos in cargos:
        if id_cargos.cargo_id not in cargos_id1:
            cargos_id1.append(id_cargos.cargo_id)

    ranger = [i for i in range(21)]
    quantidade_servidores = servidores.count()
    paginator = Paginator(servidores, 15)
    servidores = paginator.get_page(page)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_servidores(request)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_servidores(request)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    return TemplateResponse(request, template_name, locals())