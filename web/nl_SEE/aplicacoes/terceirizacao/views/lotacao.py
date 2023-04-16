from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao, global_municipios
from aplicacoes.lotacao.actions.lotacao import *

from aplicacoes.terceirizacao.exportar import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import *
from aplicacoes.terceirizacao.filtros import *
from aplicacoes.terceirizacao.exportar import *

from datetime import *


def lotacoes(request):
    if verificar_manutencao() or not verificacao_maxima(request, [17]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/lotacao/lotacoes.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 17)
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()

    lotacoes = filtro_lotacoes(request)
    quantidade_lotacoes = lotacoes.count()

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
            
    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(lotacoes, 15)
    lotacoes = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    unidades_administrativas = Unidade_administrativa.objects.all().values('id', 'sigla', 'nome').exclude(categoria= 1).order_by('nome')
    unidades_educacionais = Endereco.objects.all().values('id', 'escola__nome_escola').order_by('escola__nome_escola')
    municipios = {'municipio': global_municipios}
    
    empresa = request.GET.get('empresa')
    administrativa = request.GET.get('administrativa')
    if administrativa != None and administrativa != '':
        todos_servidores = True

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel(request)
    
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_lotacoes(request, nome ,data)

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


def lotacao_perfil(request):
    id_endereco = request.GET.get('id_endereco')
    id_unidade = request.GET.get('id_unidade') 
    if id_endereco != None:
        return HttpResponseRedirect(f'/administracao/servidores?id={id_endereco}')
    else:
        unidade = Unidade_administrativa.objects.get(id= id_unidade).categoria.id
        if unidade == 2:
            return HttpResponseRedirect(f'/administracao/diretoria?id={id_unidade}')
        elif unidade == 3:
            return HttpResponseRedirect(f'/administracao/departamento?id={id_unidade}')
        elif unidade == 4:
            return HttpResponseRedirect(f'/administracao/divisao?id={id_unidade}')
        elif unidade == 5:
            return HttpResponseRedirect(f'/administracao/nucleo?id={id_unidade}')