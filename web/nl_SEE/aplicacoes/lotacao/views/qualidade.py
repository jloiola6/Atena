from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.administracao.models import *
from aplicacoes.lotacao.models import Servidor, Servico
from aplicacoes.lotacao.actions.qualidade import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.exportar import *
from aplicacoes.terceirizacao.models import *

from datetime import date, timedelta

def qualidade(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/index.html'
    user = request.session['username']

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    return TemplateResponse(request, template_name, locals())

def agendamentos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')


    template_name = 'lotacao/qualidade/agendamentos.html'
    user = request.session['username']

    servicos = Agendamento.objects.all().values('atendimento__servico__id', 'atendimento__servico__nome').distinct()
    servidores = Agendamento.objects.all().values('servidor__id', 'servidor__nome').distinct()
    atendentes = Agendamento.objects.all().values('atendimento__atendente__nome').distinct()

    agendamentos = filtro_agendamento(request)
    qtd_agendamentos = agendamentos.count()

    # LISTA COM AS OPÇÕES DE STATUS
    lista_status = [{'id': 0, 'status': 'Pendente'}, {'id': 1, 'status': 'Concluído'}, {'id': 2, 'status': 'Cancelado'}, {'id': 3, 'status': 'Não compareceu'}]

    # DEFININDO OS ATENDIMENTOS QUE POSSAM SER AGENDADOS
    qr_atendimentos = Atendimento.objects.all()
    atendimentos = []

    for atendimento in qr_atendimentos:
        if Atendimento_dia.objects.filter(atendimento= atendimento).exists():
            atendimentos.append(atendimento)

    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(agendamentos, 15)
    agendamentos = paginator.get_page(page)

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
        servico = request.POST.get('servico')

        if servico:
            return HttpResponseRedirect(f'/lotacao/agendamento-formulario/{servico}')

        else:
            alterar_status_agendamento(request)
            return HttpResponseRedirect(f'/lotacao/agendamentos')

    return TemplateResponse(request, template_name, locals())

def relatorio(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/relatorios.html'
    user = request.session['username']

    qr_atendimentos = Atendimento.objects.all()
    atendimentos = []

    for atendimento in qr_atendimentos:
        if Atendimento_dia.objects.filter(atendimento= atendimento).exists():
            atendimentos.append(atendimento)

    if request.method == 'POST':
        if request.POST.get('relatorio') == 'relatorio-pdf':
            return exportar_relatorio(request)

    return TemplateResponse(request, template_name, locals())

def perfil_agendamento(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/perfil-agendamento.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())

def agendamento_formulario(request, id_atendimento):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/agendamento-formulario.html'
    user = request.session['username']

    atendimento = Atendimento.objects.get(id= id_atendimento)
    servidores = Servidor.objects.filter().values('nome', 'id').order_by('nome')

    # OPERAÇÕES PARA A GERAÇÃO DOS DIAS E HORÁRIOS DISPONÍVEIS PARA AGENDAMENTO
    DIAS_SEMANA = ['Segunda Feira', 'Terça Feira', 'Quarta Feira', 'Quinta Feira', 'Sexta Feira', 'Sábado', 'Domingo']

    # INICIALIZANDO OS DIAS E HORARIOS DO ATENDIMENTO
    atendimento_dias = Atendimento_dia.objects.filter(atendimento= atendimento)

    # GUARDANDO OS DIAS DA SEMANA QUE TÊM O ATENDIMENTO
    atendimento_dias_semana = atendimento_dias.values_list('dia', flat= True).distinct()

    hoje = date.today()

    dias_validos = []
    qtd_dias_validos = 1

    i = 0

    #fazendo a verificacao se o horario vai estar disponivel
    verificacao = True
    servico = request.build_absolute_uri().split('/')[-1]

    #filtro pegando o id do servico
    agendamentos = Agendamento.objects.filter(atendimento_id = servico).values('data', 'hora_atendimento')

    #verificar se a data e hora estao disponiveis -> mudar a variavel verificacao se nao estiver !


    while qtd_dias_validos <= 7:
        dia = hoje + timedelta(days= i)
        dia_semana = dia.isoweekday()

        if dia_semana in atendimento_dias_semana:
            horarios = []
            atendimento_horarios = Atendimento_dia.objects.filter(atendimento= atendimento, dia= dia_semana).values_list('hora', flat= True)

            for horario in atendimento_horarios:

                disponivel = not Agendamento.objects.filter(atendimento= atendimento, data= dia, hora_atendimento= horario, status = 0).exists()


                horarios.append({'hora': horario, 'disponivel': disponivel})

            dias_validos.append({'dia': dia, 'dia_semana_numero': dia_semana,'dia_semana': DIAS_SEMANA[dia_semana-1], 'horarios': horarios})
            qtd_dias_validos += 1
        i += 1

    if request.method == 'POST':
        ''' agora verificamos se ja existe este serviço nesse dia e nessa hora no banco, se existir ele apenas atualiza a pagina e se salvar ele retorna pra agendamentos'''
        if formulario_agendamento(request):
            return HttpResponseRedirect(f'/lotacao/agendamentos')
        else:
            servico = str(request.build_absolute_uri()).split('/')[-1]
            return HttpResponseRedirect(f'/lotacao/agendamento-formulario/{servico}')

    return TemplateResponse(request, template_name, locals())

def atendimento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/atendimento-formulario.html'
    user = request.session['username']

    servidores = Servidor.objects.filter().values('nome', 'id').order_by('nome')
    servicos_existentes = Servico.objects.all().order_by('nome')

    atendimentos = Atendimento.objects.filter().values('id', 'servico__nome', 'atendente__nome')
    qtd_atendimentos = atendimentos.count()

    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(atendimentos, 15)
    atendimentos = paginator.get_page(page)

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
        formulario_atendimento(request)

        return HttpResponseRedirect(f'/lotacao/atendimento-formulario')

    return TemplateResponse(request, template_name, locals())

def atendimento(request, id_atendimento):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/atendimento.html'
    user = request.session['username']

    atendimento = Atendimento.objects.get(id= id_atendimento)

    atendimento_dias = Atendimento_dia.objects.filter(atendimento= atendimento).order_by('dia', 'hora')

    SEMANA = ['Segunda Feria', 'Terça Feira', 'Quarta Feira', 'Quinta Feira', 'Sexta Feira']


    if request.method == 'POST':
        formulario_atendimento_dia(request, atendimento)

        return HttpResponseRedirect(f'/lotacao/atendimento/{id_atendimento}')
        
    return TemplateResponse(request, template_name, locals())

def aniversarios(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/aniversarios.html'
    user = request.session['username']

    hoje = date.today()
    mes_atual = hoje.month

    if request.GET.get('mes'):
        mes_atual = request.GET.get('mes')

    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro',
    ]

    mes_nome = meses[int(mes_atual)-1]

    servidores = Servidor.objects.filter(data_nascimento__month= mes_atual).values('data_nascimento', 'nome').order_by('data_nascimento', 'nome').distinct()

    servidores_casa = Servidor_lotacao.objects.filter(unidade_adm__endereco= 1, contrato__servidor__data_nascimento__month= mes_atual, status=1).values('contrato__servidor__nome', 'contrato__servidor__data_nascimento', 'unidade_adm__nome').order_by('contrato__servidor__data_nascimento__day', 'contrato__servidor__nome')
    qtd_servidores_casa = len(servidores_casa)

    servidores_terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa__endereco= 1, status= 1, servidor__data_nascimento__month= mes_atual).values('servidor__nome', 'servidor__data_nascimento', 'unidade_administrativa__nome').order_by('servidor__data_nascimento__day', 'servidor__nome')
    qtd_servidores_terceirizados = len(servidores_terceirizados)

    page_casa = request.GET.get('page_casa')
    if page_casa is None:
        page_casa = 1

    paginator_casa = Paginator(servidores_casa, 15)
    servidores_casa = paginator_casa.get_page(page_casa)

    gets_primeira = 'page_casa=1'
    gets_proxima = f'page_casa={str(int(page_casa)+1)}'
    gets_anterior = f'page_casa={str(int(page_casa)-1)}'
    gets_ultima = f'page_casa={paginator_casa.num_pages}'

    if '?' in request.get_full_path():

        gets_casa = (request.get_full_path().split('?')[1])

        if 'page_casa' not in gets_casa:
            gets_casa = f'page_casa={page_casa}&' + gets_casa

        proxima_pagina = str(int(page_casa)+1)
        pagina_anterior = str(int(page_casa)-1)

        gets_primeira = gets_casa.replace(f'page_casa={page_casa}', 'page_casa=1')
        gets_proxima = gets_casa.replace(f'page_casa={page_casa}', f'page_casa={proxima_pagina}')
        gets_anterior = gets_casa.replace(f'page_casa={page_casa}', f'page_casa={pagina_anterior}')
        gets_ultima = gets_casa.replace(f'page_casa={page_casa}', gets_ultima)

    page_terceirizado = request.GET.get('page_terceirizado')
    if page_terceirizado is None:
        page_terceirizado = 1

    paginator_terceirizado = Paginator(servidores_terceirizados, 15)
    servidores_terceirizados = paginator_terceirizado.get_page(page_terceirizado)

    primeira_gets = 'page_terceirizado=1'
    proxima_gets = f'page_terceirizado={str(int(page_terceirizado)+1)}'
    anterior_gets = f'page_terceirizado={str(int(page_terceirizado)-1)}'
    ultima_gets = f'page_terceirizado={paginator_terceirizado.num_pages}'

    if '?' in request.get_full_path():

        gets_terceirizado = (request.get_full_path().split('?')[1])
        print(gets_terceirizado)

        if 'page_terceirizado' not in gets_terceirizado:
            gets_terceirizado = f'page_terceirizado={page_terceirizado}&' + gets_terceirizado

        proxima_pagina = str(int(page_terceirizado)+1)
        pagina_anterior = str(int(page_terceirizado)-1)

        primeira_gets = gets_terceirizado.replace(f'page_terceirizado={page_terceirizado}', 'page_terceirizado=1')
        proxima_gets = gets_terceirizado.replace(f'page_terceirizado={page_terceirizado}', f'{proxima_gets}')
        anterior_gets = gets_terceirizado.replace(f'page_terceirizado={page_terceirizado}', f'{anterior_gets}')
        ultima_gets = gets_terceirizado.replace(f'page_terceirizado={page_terceirizado}', ultima_gets)

    return TemplateResponse(request, template_name, locals())

def formulario_espera(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/lista-formulario.html'
    user = request.session['username']

    #Importaçõe
    servidores = Servidor.objects.filter().values('id', 'nome').order_by('nome')
    # atendimentos = Atendimento.objects.filter().values('id', 'atendente__id', 'atendente__nome', 'servico__id', 'servico__nome').order_by('servico__nome')

    # DEFININDO OS ATENDIMENTOS QUE POSSAM SER AGENDADOS
    qr_atendimentos = Atendimento.objects.all()
    ids_atendimentos_disponiveis = []

    for atendimento in qr_atendimentos:
        if Atendimento_dia.objects.filter(atendimento= atendimento).exists():
            ids_atendimentos_disponiveis.append(atendimento.id)
    atendimentos = Atendimento.objects.filter(id__in = ids_atendimentos_disponiveis).values('id', 'atendente__id', 'atendente__nome', 'servico__id', 'servico__nome').order_by('servico__nome')
    if request.method == 'POST':
        lista_espera_act(request)
        
        return HttpResponseRedirect(f'/lotacao/lista-espera')

    return TemplateResponse(request, template_name, locals())

def lista_espera(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    agenda = filtro_lista_espera(request)
    
    servidores = Agendamento.objects.filter(status = 4).values('servidor__id', 'servidor__nome').distinct()
    servicos = Agendamento.objects.filter(status = 4).values('atendimento__servico__id', 'atendimento__servico__nome').distinct()

    qtd_lista = agenda.count()

    template_name = 'lotacao/qualidade/lista-espera.html'
    user = request.session['username']

    if request.method == 'POST':
        filtro_lista_espera(request)

        return HttpResponseRedirect(f'/lotacao/lista-espera/')

    return TemplateResponse(request, template_name, locals())

def marcar_consulta(request, id_agendamento):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [36]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/qualidade/marcar-consulta.html'
    user = request.session['username']

    agendamento_lista = Agendamento.objects.get(id= request.build_absolute_uri().split('/')[-1])

    #fazendo a verificacao se o horario vai estar disponivel
    verificacao = True
    servico = request.build_absolute_uri().split('/')[-1]

    #filtro pegando o id do servico
    agendamentos = Agendamento.objects.filter(atendimento_id = servico).values('data', 'hora_atendimento')

    # OPERAÇÕES PARA A GERAÇÃO DOS DIAS E HORÁRIOS DISPONÍVEIS PARA AGENDAMENTO
    DIAS_SEMANA = ['Segunda Feira', 'Terça Feira', 'Quarta Feira', 'Quinta Feira', 'Sexta Feira', 'Sábado', 'Domingo']

    # INICIALIZANDO OS DIAS E HORARIOS DO ATENDIMENTO
    atendimento_dias = Atendimento_dia.objects.filter(atendimento= agendamento_lista.atendimento)

    # GUARDANDO OS DIAS DA SEMANA QUE TÊM O ATENDIMENTO
    atendimento_dias_semana = atendimento_dias.values_list('dia', flat= True).distinct()

    hoje = date.today()

    dias_validos = []
    qtd_dias_validos = 1

    i = 0

    #verificar se a data e hora estao disponiveis -> mudar a variavel verificacao se nao estiver !
    while qtd_dias_validos <= 7:
        dia = hoje + timedelta(days= i)
        dia_semana = dia.isoweekday()

        if dia_semana in atendimento_dias_semana:
            horarios = []
            atendimento_horarios = Atendimento_dia.objects.filter(atendimento= agendamento_lista.atendimento, dia= dia_semana).values_list('hora', flat= True)

            for horario in atendimento_horarios:

                disponivel = not Agendamento.objects.filter(atendimento= agendamento_lista.atendimento, data= dia, hora_atendimento= horario, status = 0).exists()


                horarios.append({'hora': horario, 'disponivel': disponivel})

            dias_validos.append({'dia': dia, 'dia_semana_numero': dia_semana,'dia_semana': DIAS_SEMANA[dia_semana-1], 'horarios': horarios})
            qtd_dias_validos += 1
        i += 1

    if request.method == 'POST':
        formulario_agendamento_lista(request, agendamento_lista.id)
        return HttpResponseRedirect(f'/lotacao/agendamentos')
        

    return TemplateResponse(request, template_name, locals())
