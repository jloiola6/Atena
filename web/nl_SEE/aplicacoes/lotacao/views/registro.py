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
from aplicacoes.lotacao.exportar import *

def registro(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [33]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/registro/index.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())


def registro_lotacoes(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [33]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/registro/registro-lotacoes.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 33)

    lotacoes = filtro_registro(request)
    quantidade_lotacoes = lotacoes.count()

    registro_filtro = Historico.objects.filter(tabela= 'lotacao_servidor_lotacao').values('log__usuario__nome', 'log__usuario__id').distinct().order_by('log__usuario__nome')
    municipios = Cidade.objects.filter(estado = 1).values_list('nome', flat= True)

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    lotacao_aux = lotacoes[valor_paginacao-15:valor_paginacao]

    lotacoes1= []
    for lotacao in lotacao_aux:
        lotacoes_filtro= Historico.objects.filter(tabela= 'lotacao_servidor_lotacao', objeto= lotacao['id']).order_by('-id').values('log__usuario__nome', 'log__usuario__id', 'data', 'objeto')

        if lotacoes_filtro.exists():
            lotacoes1.append((lotacoes_filtro, lotacao['contrato__servidor__nome'], lotacao['unidade_adm__endereco__municipio'], lotacao['unidade_escolar__municipio'], lotacao['unidade_adm__nome'], lotacao['unidade_escolar__escola__nome_escola'], lotacao['numero_memorando']))
        else:
            lotacoes_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
            lotacoes1.append((lotacoes_filtro, lotacao['contrato__servidor__nome'], lotacao['unidade_adm__endereco__municipio'], lotacao['unidade_escolar__municipio'], lotacao['unidade_adm__nome'], lotacao['unidade_escolar__escola__nome_escola'], lotacao['numero_memorando']))


        # if municipio != None and municipio != '':
        #         print(municipio)
        #         lotacoes_filtro = lotacoes_filtro.filter(unidade_escolar__municipio= municipio)
        #         print(lotacoes_filtro)

    if request.method == "POST":
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_registro(request)


    paginator = Paginator(lotacoes, 15)
    lotacoes = paginator.get_page(page)

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


    return TemplateResponse(request, template_name, locals())


def registro_contratos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [33]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/registro/registro-contratos.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 33)

    contratos = filtro_registro_contrato(request)
    quantidade_contratos = contratos.count()

    registro_filtro = Historico.objects.filter(tabela= 'lotacao_servidor_contrato').values('log__usuario__nome', 'log__usuario__id').distinct().order_by('log__usuario__nome')
    municipios = Cidade.objects.filter(estado = 1).values_list('nome', flat= True)


    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    contrato_aux = contratos[valor_paginacao-15:valor_paginacao]

    contrato1= []
    for contrato in contrato_aux:
        contratos_filtro= Historico.objects.filter(tabela= 'lotacao_servidor_contrato', objeto= contrato['id']).order_by('-id').values('log__usuario__nome', 'log__usuario__id', 'data', 'objeto')
        tecnico = request.GET.get('tecnico')
        if tecnico != None and tecnico != '':
            caux = list(Historico.objects.filter(tabela= 'lotacao_servidor_contrato', objeto= contrato['id']).values('log__usuario__id'))
            if(caux[-1]['log__usuario__id']) == int(tecnico):
                if contratos_filtro.exists():
                    contrato1.append((contratos_filtro, contrato['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))

                else:
                    contratos_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
                    contrato1.append((contratos_filtro['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))
        else:
            if contratos_filtro.exists():
                    contrato1.append((contratos_filtro, contrato['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))

            else:
                contratos_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
                contrato1.append((contratos_filtro['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))

    if request.method == "POST":
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_registro_contrato(request)

    paginator = Paginator(contratos, 15)
    contratos = paginator.get_page(page)

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

    return TemplateResponse(request, template_name, locals())