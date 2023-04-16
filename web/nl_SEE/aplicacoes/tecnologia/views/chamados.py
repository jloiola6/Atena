from calendar import c
from logging import NullHandler
from tempfile import template
from urllib import request
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
from aplicacoes.tecnologia.actions.chamados import *
from aplicacoes.lotacao.models import Servidor, Servidor_lotacao
from django.core.paginator import Paginator


def chamados(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [21, 31, 32]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados.html'
    user = request.session['username']

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    return TemplateResponse(request, template, locals())

def chamados_tecnico(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [31]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados-tecnico.html'
    user = request.session['username']
    tecnico = Usuarios.objects.get(login= user)

    chamados_tecnico = Solicitacao.objects.filter(tecnico_atribuido= tecnico.servidor).exclude(situacao= 'Finalizado').order_by('-id')
    chamados_orfaos = Solicitacao.objects.filter(tecnico_atribuido= None, situacao__in=('Aberto', 'Pausado')).order_by('-id')

    chamados_tecnico_internos = chamados_tecnico.filter(tipo_chamado= 'Interno')
    chamados_tecnico_externos = chamados_tecnico.filter(tipo_chamado= 'Externo')

    chamados_orfaos_internos = chamados_orfaos.filter(tipo_chamado= 'Interno')
    chamados_orfaos_externos = chamados_orfaos.filter(tipo_chamado= 'Externo')

    return TemplateResponse(request, template, locals())

def chamados_help(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [32]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados-help.html'
    user = request.session['username']

    unidades_adm = Unidade_administrativa.objects.all().order_by('nome')
    enderecos = Endereco.objects.all().order_by('escola__nome_escola')

    consulta_chamados = Solicitacao.objects.values('unidade_administrativa__id', 'unidade_administrativa__sigla', 'unidade_administrativa__nome').distinct()
    endereco_chamados = Solicitacao.objects.values('endereco_escola__escola__id', 'endereco_escola__escola__cod_inep', 'endereco_escola__escola__nome_escola', 'endereco_escola__municipio').distinct()

    chamados = filtro_chamados(request)

    quantidade_chamados = chamados.count()

    page = request.GET.get('page')
    if page is None:
        page = 1
    # Paginação
    paginator = Paginator(chamados, 15)
    chamados = paginator.get_page(page)

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

    if request.method == 'GET':
        tipo_solicitacao = request.GET.get('tipo_solicitacao')

        if tipo_solicitacao:
            tipo_unidade = request.GET.get('tipo_unidade')

            if tipo_unidade == 'Unidade Administrativa':
                unidade = request.GET.get('unidade_administrativa')
                tipo_chamado = request.GET.get('tipo_chamado')
            else:
                unidade = request.GET.get('unidade_escolar')
                tipo_chamado = request.GET.get('tipo_chamado_escola')

            return HttpResponseRedirect(f'/tecnologia/chamado-formulario?tipo_solicitacao={tipo_solicitacao}&tipo_unidade={tipo_unidade}&unidade={unidade}&tipo_chamado={tipo_chamado}')

    return TemplateResponse(request, template, locals())

def chamados_adm(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [21]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados-adm.html'
    user = request.session['username']

    tipos_chamado = Tipos_solicitacao.objects.all()
    tipos_servico = Tipos_solicitacao.objects.all().values('tipo').distinct()

    if request.method == 'POST':
        adicionar_tipo_servico(request)

        return HttpResponseRedirect('/tecnologia/chamados-adm')

    return TemplateResponse(request, template, locals())

def chamado_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [21, 32]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados-formulario.html'
    user = request.session['username']

    tipo_solicitacao = request.GET.get('tipo_solicitacao')
    tipo_unidade = request.GET.get('tipo_unidade')
    id_unidade = request.GET.get('unidade')
    tipo_chamado = request.GET.get('tipo_chamado')

    if 'Administrativa' in tipo_unidade:
        unidade = Unidade_administrativa.objects.get(id= id_unidade)
        # servidores_lotados = Servidor_lotacao.objects.filter(unidade_adm = unidade).values('contrato__servidor__id', 'contrato__servidor__nome').distinct()
        servidores_lotados = []
        for solicitante in list(chain(Servidor_lotacao.objects.filter(unidade_adm = unidade, status=1).values('contrato__servidor__id', 'contrato__servidor__nome').distinct(), Contrato_lotacao.objects.filter(unidade_administrativa = unidade).values('servidor__id', 'servidor__nome').distinct())):
            try:
                servidores_lotados.append((solicitante['contrato__servidor__id'], solicitante['contrato__servidor__nome']))
            except:
                servidores_lotados.append((solicitante['servidor__id'], solicitante['servidor__nome']))
    else:
        unidade = Endereco.objects.get(id= id_unidade)
        # servidores_lotados = Servidor_lotacao.objects.filter(unidade_escolar = unidade).values('contrato__servidor__id', 'contrato__servidor__nome').distinct()
        servidores_lotados = []
        for solicitante in list(chain(Servidor_lotacao.objects.filter(unidade_escolar = unidade, status=1).values('contrato__servidor__id', 'contrato__servidor__nome').distinct(), Contrato_lotacao.objects.filter(endereco = unidade).values('servidor__id', 'servidor__nome').distinct())):
            try:
                servidores_lotados.append((solicitante['contrato__servidor__id'], solicitante['contrato__servidor__nome']))
            except:
                servidores_lotados.append((solicitante['servidor__id'], solicitante['servidor__nome']))

    tipos_servico = Tipos_solicitacao.objects.all().values('tipo').distinct().order_by('tipo')
    servicos = Tipos_solicitacao.objects.all().order_by('acao')

    tecnicos = []
    for item in list(chain(Servidor_lotacao.objects.filter(unidade_adm__hierarquia = 11, status= 1), Contrato_lotacao.objects.filter(unidade_administrativa__hierarquia = 11, status= 1))):
        try:
            tecnicos.append((item.contrato.servidor.id, item.contrato.servidor.nome))
        except:
            tecnicos.append((item.servidor.id, item.servidor.nome))

    if request.method == 'POST':
        formulario_chamado(request, tipo_solicitacao, tipo_unidade, unidade, tipo_chamado)

        return HttpResponseRedirect('/tecnologia/chamados-help')

    return TemplateResponse(request, template, locals())


def chamado_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [21, 31, 32]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamado-perfil.html'
    user = request.session['username']
    usuario = Usuarios.objects.get(login= user)
    chamado_id  = request.GET.get('id')
    perfil = request.GET.get('perfil')

    solicitacao = Solicitacao.objects.get(id = chamado_id)
    user_solicitante = Servidor.objects.get(id= solicitacao.user_solicitante)
    chamados = Solicitacao_chamado.objects.filter(solicitacao= solicitacao, sub_chamado= 0)
    subchamados = Solicitacao_chamado.objects.filter(solicitacao= solicitacao, sub_chamado= 1)
    equipamentos = Solicitacao_equipamento.objects.filter(solicitacao= solicitacao)
    tecnico_atribuido = solicitacao.tecnico_atribuido

    tecnicos = Solicitacao_tecnico.objects.filter(solicitacao= solicitacao)

    if Solicitacao_retirada.objects.filter(solicitacao = solicitacao).exists():
        equipamento_recolhido = Solicitacao_retirada.objects.get(solicitacao = solicitacao)
    else:
        equipamento_recolhido = None

    opcao_equipamentos = ['Computador', 'Notebook', 'Estabilizador', 'Nobreak', 'Datashow', 'Monitor de Video', 'Modem ADSL', 'Roteador sem fio', 'Outros']

    if solicitacao.tecnico_atribuido:
        tecnico_atual = usuario.servidor == solicitacao.tecnico_atribuido.id
    elif tecnicos:
        tecnico_atual = tecnicos.last().user_tecnico == usuario
    else:
        tecnico_atual = False

    lista_tecnicos = []
    for item in list(chain(Servidor_lotacao.objects.filter(unidade_adm__hierarquia = 11, status= 1), Contrato_lotacao.objects.filter(unidade_administrativa__hierarquia = 11, status= 1))):
        try:
            lista_tecnicos.append((item.contrato.servidor.id, item.contrato.servidor.nome))
        except:
            lista_tecnicos.append((item.servidor.id, item.servidor.nome))


    if request.method == 'POST':
        if request.POST.get('btn-iniciar') == 'iniciar':
            iniciar_chamado(request, solicitacao, user)

        elif request.POST.get('btn-exportar') == 'exportar':
            return exportar_chamados(request, solicitacao, equipamentos, chamados, equipamento_recolhido)

        elif request.POST.get('btn-finalizar') == 'Finalizado':
            finalizar_chamado(request, solicitacao, user, tecnicos.last(), request.POST.get('btn-finalizar'))

        elif request.POST.get('btn-pausar') == 'Pausado':
            finalizar_chamado(request, solicitacao, user, tecnicos.last(), 'Pausado')

        elif request.POST.get('btn-recolher') == 'recolher':
            recolher_equipamento(request, solicitacao, user, tecnicos.last())

        elif request.POST.get('btn-transferir') == 'Transferido':
            transferir_chamado(request, solicitacao, user, tecnicos.last(),tecnico_atribuido)

        return HttpResponseRedirect(f'/tecnologia/chamado-perfil?id={chamado_id}&perfil={perfil}')

    return TemplateResponse(request, template, locals())


def chamados_adicionar(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [21, 31, 32]):
        return HttpResponseRedirect('/')

    template = 'tecnologia/chamados/chamados-adicionar.html'
    user = request.session['username']
    usuario = Usuarios.objects.get(login= user)

    chamado_id = request.GET.get('id')
    solicitacao = Solicitacao.objects.get(id = chamado_id)

    tipos_servico = Tipos_solicitacao.objects.all().values('tipo').distinct().order_by('tipo')
    servicos = Tipos_solicitacao.objects.all().order_by('acao')

    if request.method == 'POST':
        adicionar_chamados(request, solicitacao)
        return HttpResponseRedirect(f'/tecnologia/chamado-perfil?id={chamado_id}')


    return TemplateResponse(request, template, locals())