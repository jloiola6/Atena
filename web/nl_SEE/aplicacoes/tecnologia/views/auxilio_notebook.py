import requests
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao

from aplicacoes.tecnologia.filtros import filtro_auxilio
from aplicacoes.core.views import global_municipios
from aplicacoes.tecnologia.exportar import exportar_devolucao_notebook
from aplicacoes.tecnologia.action import devolucao_auxilio
from aplicacoes.lotacao.models import Servidor, Servidor_contato, Servidor_banco, Servidor_endereco
from aplicacoes.tecnologia.models import Auxilio_notebook

from datetime import datetime,date

def main(request):
    if not verificacao_maxima(request, [28, 29, 30]) or verificar_manutencao():
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'tecnologia/auxilio-notebook/index.html'

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    return TemplateResponse(request, template_name, locals())


def auxilio_notebook(request):
    if not verificacao_maxima(request, [28]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/auxilio-notebook/auxilio-tabela.html'
    user = request.session['username']
    municipios = global_municipios

    escolas = requests.get('https://auxilio.see.ac.gov.br/api/dados-escolas/?chave=d55dafc14c6801c9dc99b3d8778598cf').json()

    dados = filtro_auxilio(request, 'solicitacao')

    solicitacoes = dados[0]
    quantidade_solicitacoes = dados[1]
    gets_primeira = dados[2]
    gets_anterior = dados[3]
    gets_proxima = dados[4]
    gets_ultima = dados[5]

    if request.method == 'POST':
        requests.get(f"https://auxilio.see.ac.gov.br/api/atualizar-auxilio/?chave=d55dafc14c6801c9dc99b3d8778598cf&auxilio_id={request.POST.get('auxilio_id')}&situacao={request.POST.get('situacao')}&motivo={request.POST.get('motivo')}&username={user}")
        return HttpResponseRedirect('/tecnologia/tabela-auxilio')

    return TemplateResponse(request, template_name, locals())


def notas_notebook(request):
    if not verificacao_maxima(request, [29]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/auxilio-notebook/notas-tabela.html'
    user = request.session['username']
    municipios = global_municipios

    escolas = requests.get('https://auxilio.see.ac.gov.br/api/dados-escolas/?chave=d55dafc14c6801c9dc99b3d8778598cf').json()

    dados = filtro_auxilio(request, 'notas')

    solicitacoes = dados[0]
    quantidade_solicitacoes = dados[1]
    gets_primeira = dados[2]
    gets_anterior = dados[3]
    gets_proxima = dados[4]
    gets_ultima = dados[5]

    notas = []
    documentos = []
    verificador = []

    for nota in dados[6]:
        dicionario = {
            'id': nota['id'],
            'auxilio__id': nota['auxilio__id'],
            "auxilio__usuario__nome": nota['auxilio__usuario__nome'],
            "auxilio__usuario__cpf": nota['auxilio__usuario__cpf'],
            "auxilio__usuario__email": nota['auxilio__usuario__email'],
            "auxilio__usuario__cargo": nota['auxilio__usuario__cargo'],
            "auxilio__usuario__lotacao__nome": nota['auxilio__usuario__lotacao__nome'],
            "auxilio__usuario__lotacao__municipio": nota['auxilio__usuario__lotacao__municipio'],
            'situacao': nota['situacao'],
            'nota': nota['auxilio__nota'],
            'adm_nota': nota['auxilio__adm_nota'],
            'motivo': nota['auxilio__motivo'],
        }

        if not nota['auxilio__id'] in verificador:
            notas.append(dicionario)
            verificador.append(nota['auxilio__id'])

        documentos.append({
            'id': nota['id'],
            'auxilio__id': nota['auxilio__id'],
            'situacao': nota['situacao'],
            'nome_arquivo': str(nota['arquivo']).split('/')[-1],
            'path_arquivo': 'https://auxilio.see.ac.gov.br/media/' + str(nota['arquivo']),
            'adm': nota['adm'],
            'motivo': nota['motivo']
        })

        nota_id = documentos[-1]['id']

    if request.method == 'POST':
        requests.get(f"https://auxilio.see.ac.gov.br/api/atualizar-nota/?chave=d55dafc14c6801c9dc99b3d8778598cf&situacao={request.POST.get('situacao')}&nota_id={request.POST.get('nota_id')}&motivo={request.POST.get('motivo')}&diferenca={request.POST.get('diferenca')}&username={user}")

        return HttpResponseRedirect('/tecnologia/tabela-notas')

    return TemplateResponse(request, template_name, locals())


def devolucao_notebook(request):
    if not verificacao_maxima(request, [30]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/auxilio-notebook/devolucao-tabela.html'
    user = request.session['username']
    devolucao = True
    municipios = global_municipios

    escolas = requests.get('https://auxilio.see.ac.gov.br/api/dados-escolas/?chave=d55dafc14c6801c9dc99b3d8778598cf').json()

    situacao_devolucao = request.GET.get('situacao')

    if situacao_devolucao == 'D':
        dado_devolucao = filtro_auxilio(request, 'devolucao')

        dados_devolucoes = dado_devolucao[0]
        quantidade_devolucoes = dado_devolucao[1]

        page = request.GET.get('page')
        if page is None:
            page = '1'

        paginator = Paginator(dados_devolucoes, 15)
        devolucao_pages = paginator.get_page(page)

        gets_primeira = 'page=1'
        gets_proxima = f'page={str(int(page)+1)}'
        gets_anterior = f'page={str(int(page)-1)}'
        gets_ultima = f'page={paginator.num_pages}'

        if '?' in request.get_full_path():

            gets = (request.get_full_path().split('?')[1])

            proxima_pagina = str(int(page)+1)
            pagina_anterior = str(int(page)-1)

            if 'page' not in gets:
                gets = f'page={page}&' + gets

            gets_primeira = gets.replace(f'page={page}', 'page=1')
            gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
            gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
            gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

    else:
        dados = filtro_auxilio(request, 'devolucao')

        solicitacoes = dados[0]
        quantidade_solicitacoes = dados[1]
        gets_primeira = dados[2]
        gets_anterior = dados[3]
        gets_proxima = dados[4]
        gets_ultima = dados[5]

        if request.method == 'POST':
            if request.POST.get('devolucao') == 'devolucao':
                return devolucao_auxilio(request)
            # elif request.POST.get('exportar-devolucao') == 'exportar-devolucao':
            #     return exportar_devolucao_notebook(request, user, dados)

            return HttpResponseRedirect('/tecnologia/tabela-auxilio')

    return TemplateResponse(request, template_name, locals())


def servidor_perfil(request):
    if not verificacao_maxima(request, [30]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/auxilio-notebook/servidor-perfil.html'
    user = request.session['username']
    devolucao = True
    municipios = global_municipios
    id_auxilio = int(request.GET.get('id'))

    dados = requests.get(f'https://auxilio.see.ac.gov.br/api/dado-nota/?chave=d55dafc14c6801c9dc99b3d8778598cf&id={id_auxilio}').json()
    auxilio = dados[0]
    notas = dados[1]

    documentos = []
    for nota in notas:
        documentos.append({
            'id': nota['id'],
            'auxilio__id': nota['auxilio__id'],
            'situacao': nota['situacao'],
            'nome_arquivo': str(nota['arquivo']).split('/')[-1],
            'path_arquivo': 'https://auxilio.see.ac.gov.br/media/' + str(nota['arquivo']),
            'adm': nota['adm'],
            'motivo': nota['motivo']
        })
    documento = documentos[-1]

    servidor= Servidor.objects.get(cpf = auxilio['usuario__cpf'])
    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

    if Servidor_contato.objects.filter(servidor= servidor).exists():
        servidor_contato = Servidor_contato.objects.filter(servidor= servidor)

    if Servidor_banco.objects.filter(servidor= servidor).exists():
        servidor_banco = Servidor_banco.objects.get(servidor= servidor)

    if Auxilio_notebook.objects.filter(auxilio= auxilio['id']).exists():
        devolucoes = Auxilio_notebook.objects.get(auxilio= auxilio['id'])

        caminho = str(devolucoes.path_arquivo())
        dict_documento = {'id': devolucoes.id, 'caminho': caminho}

    data= date.today()

    if request.method == 'POST':
        if request.POST.get('devolucao') == 'devolucao':
            devolucao_auxilio(request, auxilio, documento['id'], data)
            return HttpResponseRedirect(f'/tecnologia/servidor-perfil?id={id_auxilio}')
        elif request.POST.get('exportar-devolucao') == 'exportar-devolucao':
            return exportar_devolucao_notebook(request, user, dados, auxilio)

    return TemplateResponse(request, template_name, locals())