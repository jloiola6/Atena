from datetime import datetime
from pkgutil import iter_modules
from traceback import print_tb
from requests import post
from aplicacoes.administracao.models import *
from aplicacoes.lotacao.models import Servidor
from aplicacoes.core.uploads import *
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.atena.models import Cidade
from aplicacoes.tecnologia.models import *
from aplicacoes.tecnologia.views import *
import re


def formulario_chamado(request, tipo_solicitacao, tipo_unidade, unidade, tipo_chamado):
    edicao = False
    data_atual = datetime.now()
    # Hora formatada para maquina de produção
    data = str(data_atual).split(' ')
    hora_completa = data[-1]
    hora = hora_completa.split(':')
    data_formatada = f'{data[0]} {int(hora[0]) - 5}:{hora[1]}:{hora[2]}'

    user = request.session['username']
    user_criador = Usuarios.objects.get(login=user).id
    tecnico = request.POST.get('tecnico')
    prioridade = request.POST.get('prioridade')
    user_solicitante = request.POST.get('nome_solicitante')
    contato = request.POST.get("contato")

    solicitacao = Solicitacao()

    if tipo_unidade == 'Unidade Administrativa':
        solicitacao.unidade_administrativa = unidade
    else:
        solicitacao.endereco_escola = unidade
    solicitacao.user_criador = Usuarios.objects.get(id = user_criador)

    if tecnico != '':
        solicitacao.tecnico_atribuido = Servidor.objects.get(id= tecnico)
    solicitacao.user_solicitante = user_solicitante
    solicitacao.tipo_chamado = tipo_chamado
    solicitacao.prioridade = prioridade
    solicitacao.tipo_unidade = tipo_unidade
    solicitacao.data_abertura = data_formatada
    solicitacao.contato = contato
    solicitacao.situacao = "Aberto"
    solicitacao.save()

    c = 0
    lista = []
    for dado in request.POST:
        if 'tipo-servico' in dado:
            tipo_servico = request.POST.get(dado)
            valor = dado.split('-')[-1]
            servico = request.POST.get(f'servico-{tipo_servico}-{valor}')
            descricao = request.POST.get(f'descricao_chamado{valor}')

            lista.append((tipo_servico, servico, descricao))

    if tipo_solicitacao == "chamado":
        for item in lista:
            chamado = Solicitacao_chamado()

            chamado.solicitacao = solicitacao
            chamado.tipo = item[0]
            chamado.servico = item[1]
            chamado.descricao_chamado = item[2]
            chamado.sub_chamado = 0
            chamado.save()
            salvar_historico(request, chamado, edicao, 'tecnologia_solicitacao_chamado')

    elif tipo_solicitacao =="solicitacao_equipamento":
        for item in range(0, len(lista), 4):
            solicitacao_equipamento = Solicitacao_equipamento()

            solicitacao_equipamento.solicitacao = solicitacao
            solicitacao_equipamento.numero_documento = lista[item]
            solicitacao_equipamento.equipamento = lista[item+1]
            solicitacao_equipamento.quantidade = int(lista[item+2])
            solicitacao_equipamento.descricao = lista[item+3]
            solicitacao_equipamento.save()
            salvar_historico(request, solicitacao_equipamento, edicao, 'tecnologia_solicitacao_equipamento')

        salvar_historico(request, solicitacao, edicao, 'tecnologia_cadastro_chamado')


def iniciar_chamado(request, solicitacao, user):
    data_atual = datetime.now()

    usuario = Usuarios.objects.get(login= user)
    servidor = Servidor.objects.get(id= usuario.servidor)

    iniciar = Solicitacao_tecnico()
    iniciar.solicitacao = solicitacao
    iniciar.data_inicio = data_atual
    iniciar.user_tecnico = usuario
    iniciar.situacao = 'Iniciado'

    solicitacao.situacao = 'Em atendimento'
    solicitacao.tecnico_atribuido = servidor
    solicitacao.save()

    iniciar.save()

def finalizar_chamado(request, solicitacao, user, tecnico, situacao):
    datafinal = datetime.now()
    tecnico.data_fim = datafinal

    tempo2 = str(datafinal - tecnico.data_inicio.replace(tzinfo=None)).split(':')
    tempo_tecnico = 0
    tempo = []

    if 'days,' in tempo2[0]:
        manipulacao = tempo2[0]
        manipulacao = manipulacao.split(' days,')
        tempo.append(manipulacao[0])
        tempo.append(manipulacao[1])
        tempo.append(tempo2[1])
        tempo.append(tempo2[2])
        passo = 4

        for i in range(0, passo, passo):
        #Calculo para N Dia (Máximo 30)
            if passo == 4:
                tempo_tecnico += int(tempo[i+2])
                if int(tempo[i]) > 0:
                    tempo_tecnico += int(tempo[i]) * 24 * 60
                if int(tempo[i+1]) > 0:
                    tempo_tecnico += int(tempo[i+1]) * 60
                if int(str(tempo[i+3]).split('.')[0]) > 30:
                    tempo_tecnico += 1
    elif 'day,' in tempo2[0]:
        manipulacao = tempo2[0]
        manipulacao = manipulacao.split(' day,')
        tempo.append(manipulacao[0])
        tempo.append(manipulacao[1])
        tempo.append(tempo2[1])
        tempo.append(tempo2[2])
        passo = 4

        for i in range(0, passo, passo):
        #Calculo para N Dia (Máximo 30)
            if passo == 4:
                tempo_tecnico += int(tempo[i+2])
                if int(tempo[i]) > 0:
                    tempo_tecnico += int(tempo[i]) * 24 * 60
                if int(tempo[i+1]) > 0:
                    tempo_tecnico += int(tempo[i+1]) * 60
                if int(str(tempo[i+3]).split('.')[0]) > 30:
                    tempo_tecnico += 1
    else:
        passo = 3
        for i in range(0, passo, passo):
            #Calculo para 1 Dia
            if passo == 3:
                tempo_tecnico += int(tempo2[i+1])
                if int(tempo2[i]) > 0:
                    tempo_tecnico += int(tempo2[i]) * 60
                if int(str(tempo2[i+2]).split('.')[0]) > 30:
                    tempo_tecnico += 1

    tecnico.total = tempo_tecnico
    tecnico.situacao = situacao

    if situacao == 'Pausado':
        tecnico.motivo = request.POST.get('motivo')

    solicitacao.user_finalizador = Usuarios.objects.get(login= user).nome
    solicitacao.data_finalizacao = datafinal
    solicitacao.descricao = request.POST.get('atividades-realizadas')
    solicitacao.situacao = situacao
    tecnico.save()

    total = 0
    for item in Solicitacao_tecnico.objects.filter(solicitacao= solicitacao):
        if item.total:
            total += item.total

    solicitacao.tempo_total = total
    solicitacao.save()


def recolher_equipamento(request, solicitacao, user, tecnico):
    data_atual = datetime.now()
    equipamento = request.POST.get('equipamento')
    recolher_equipamento = Solicitacao_retirada()

    recolher_equipamento.solicitacao = solicitacao
    recolher_equipamento.num_serie = request.POST.get('serie')
    recolher_equipamento.patrimonio = request.POST.get('patrimonio')
    recolher_equipamento.horario_retirada = data_atual
    if equipamento == 'Outros':
        recolher_equipamento.equipamento = request.POST.get('outros')
    else:
        recolher_equipamento.equipamento = equipamento

    recolher_equipamento.save()


def adicionar_chamados(request, solicitacao):
    edicao = False

    c = 0
    lista = []
    for dado in request.POST:
        if 'tipo-servico' in dado:
            tipo_servico = request.POST.get(dado)
            valor = dado.split('-')[-1]
            servico = request.POST.get(f'servico-{tipo_servico}-{valor}')
            descricao = request.POST.get(f'descricao_chamado{valor}')

            lista.append((tipo_servico, servico, descricao))

    for item in lista:
        chamado = Solicitacao_chamado()

        chamado.solicitacao = solicitacao
        chamado.tipo = item[0]
        chamado.servico = item[1]
        chamado.descricao_chamado = item[2]
        chamado.sub_chamado = 1
        chamado.save()
        salvar_historico(request, chamado, edicao, 'tecnologia_solicitacao_chamado')

def adicionar_tipo_servico(request):
    edicao = False

    tipo_servico = request.POST.get('tipo')
    servico = request.POST.get('servico')

    novo_tipo = Tipos_solicitacao()
    novo_tipo.tipo = tipo_servico
    novo_tipo.acao = servico
    novo_tipo.save()
    salvar_historico(request, novo_tipo, edicao, 'tecnologia_tipos_solicitacao')


def transferir_chamado(request, solicitacao, user, tecnicos, tecnico_atribuido):
    edicao = True
    tecnico = request.POST.get('tecnico')

    solicitacao.tecnico_atribuido = Servidor.objects.get(id=tecnico)
    solicitacao.save()

    if tecnicos:
        tecnicos.user_tecnico = Usuarios.objects.get(servidor= tecnico)
        tecnicos.save()

    salvar_historico(request, solicitacao, edicao, 'tecnologia_solicitacao')
