from datetime import datetime
from pytz import timezone

from .models import *

from aplicacoes.core.actions import dict_compare, salvar_historico

import re


def formulario_relatorio_aluno(request, edicao):
    #Capturando dados
    aluno = int(request.GET.get('id'))
    etapa = request.GET.get('etapa')

    if request.POST.get('aluno-fieldset-situacao') in ('transferido', 'desistente'):
        portugues = '-'
        arte = '-'
        ingles = '-'
        ed_fisica = '-'
        matematica = '-'
        fisica = '-'
        quimica = '-'
        biologia = '-'
        historia = '-'
        geografia = '-'
        filosofia = '-'
        sociologia = '-'
        espanhol = '-'
        projeto_vida = '-'
        lt_ch = '-'
        mt_cn = '-'
        area_conhecimento = '-'
        investigacao = '-'
        criativos = '-'
        sociocultural = '-'
        empreendedorismo = '-'
        if request.POST.get('aluno-fieldset-situacao') == 'transferido':
            resultado = 'Transferido'
        else:
            resultado = 'Desistente'


    elif  etapa == '3ª Série':
        portugues = request.POST.get('portugues')
        arte = '-'
        ingles = '-'
        ed_fisica = '-'
        matematica = request.POST.get('matematica')
        fisica = '-'
        quimica = '-'
        biologia = '-'
        historia = '-'
        geografia = '-'
        filosofia = '-'
        sociologia = '-'
        espanhol = '-'
        projeto_vida = request.POST.get('projeto_vida')
        lt_ch = '-'
        mt_cn = '-'
        if request.POST.get('aluno-fieldset-rota') == 'propedeutica':
            area_conhecimento = request.POST.get('aluno-fieldset-areas')
            investigacao = request.POST.get('investigacao')
            criativos = request.POST.get('criativos')
            sociocultural = request.POST.get('sociocultural')
            empreendedorismo = request.POST.get('empreendedorismo')
            resultado = request.POST.get('resultado')
        else:
            area_conhecimento = '-'
            investigacao = '-'
            criativos = '-'
            sociocultural = '-'
            empreendedorismo = '-'

        resultado = request.POST.get('resultado')

    else:
        portugues = request.POST.get('portugues')
        arte = request.POST.get('arte')
        ingles = request.POST.get('ingles')
        ed_fisica = request.POST.get('ed_fisica')
        matematica = request.POST.get('matematica')
        fisica = request.POST.get('fisica')
        quimica = request.POST.get('quimica')
        biologia = request.POST.get('biologia')
        historia = request.POST.get('historia')
        geografia = request.POST.get('geografia')
        filosofia = request.POST.get('filosofia')
        sociologia = request.POST.get('sociologia')
        espanhol = request.POST.get('espanhol')
        projeto_vida = request.POST.get('projeto_vida')
        lt_ch = request.POST.get('lt_ch')
        mt_cn = request.POST.get('mt_cn')
        area_conhecimento = '-'
        investigacao = '-'
        criativos = '-'
        sociocultural = '-'
        empreendedorismo = '-'

        resultado = request.POST.get('resultado')

    if edicao:
        relatorio = RelatorioFinal.objects.filter(aluno__id= request.GET.get('id'), etapa= etapa)
        inputs_relatorio = {'id': relatorio[0].id, 'portugues': portugues, 'arte': arte, 'ingles': ingles, 'ed_fisica': ed_fisica, 'matematica': matematica, 'fisica': fisica, 'quimica': quimica,  'biologia': biologia,  'historia': historia,  'geografia': geografia,  'filosofia': filosofia,  'sociologia': sociologia, 'espanhol': espanhol, 'projeto_vida': projeto_vida,  'lt_ch': lt_ch,  'mt_cn': mt_cn,  'investigacao': investigacao,  'criativos': criativos,  'sociocultural': sociocultural,  'empreendedorismo': empreendedorismo, 'area_conhecimento': area_conhecimento, 'resultado': resultado, 'etapa': etapa}
        modificacoes_relatorioFinal = dict_compare(relatorio.values()[0], inputs_relatorio)

        relatorio = relatorio[0]

    else:
        relatorio = RelatorioFinal()
        modificacoes_relatorioFinal = None
        aluno = Aluno.objects.get(id= aluno)
        relatorio.aluno = aluno
        relatorio.etapa = etapa

    #Salvando no banco dados do departamento
    relatorio.portugues = portugues
    relatorio.arte = arte
    relatorio.ingles = ingles
    relatorio.ed_fisica = ed_fisica
    relatorio.matematica = matematica
    relatorio.fisica = fisica
    relatorio.quimica = quimica
    relatorio.biologia = biologia
    relatorio.historia = historia
    relatorio.geografia = geografia
    relatorio.filosofia = filosofia
    relatorio.sociologia = sociologia
    relatorio.espanhol = espanhol
    relatorio.projeto_vida = projeto_vida
    relatorio.lt_ch = lt_ch
    relatorio.mt_cn = mt_cn
    relatorio.area_conhecimento = area_conhecimento
    relatorio.investigacao = investigacao
    relatorio.criativos = criativos
    relatorio.sociocultural = sociocultural
    relatorio.empreendedorismo = empreendedorismo
    relatorio.resultado = resultado
    relatorio.save()

    salvar_historico(request, relatorio, edicao, 'dinem_relatorioFinal', modificacoes_relatorioFinal)


def formulario_aluno(request, edicao, aluno, turma):
    #Capturando dados
    nome = request.POST.get('nome')
    cpf = request.POST.get('CPF')
    cpf = re.sub('\D', '', cpf)
    sexo = request.POST.get('sexo')
    data = request.POST.get('data')
    nome_mae = request.POST.get('nome_mae')
    nome_pai = request.POST.get('nome_pai')
    nacionalidade = request.POST.get('nacionalidade')
    valor = request.POST.get('naturalidade')
    if valor == 'Ji-Paraná - RO':
        valor = valor.split('-')
        naturalidade = f'{valor[0]}-{valor[1]}'
        uf = valor[-1]
    else:
        valor = valor.split('-')
        naturalidade = valor[0]
        uf = valor[-1]

    if edicao:
        aluno = Aluno.objects.filter(id= aluno.id)
        inputs_aluno = {'nome': nome, 'cpf': cpf, 'sexo': sexo, 'nascimento': data, 'nome_pai': nome_pai, 'nome_mae': nome_mae, 'nacionalidade': nacionalidade,  'uf': uf,  'naturalidade': naturalidade}
        modificacoes_aluno = dict_compare(aluno.values()[0], inputs_aluno)

        aluno = aluno[0]
    else:
        turma = Turmas.objects.get(id= turma.id)
        aluno = Aluno()
        modificacoes_aluno = None

    aluno.turma = turma
    aluno.nome = nome
    aluno.cpf = cpf
    aluno.sexo = sexo
    aluno.nascimento = data
    aluno.nome_pai = nome_pai
    aluno.nome_mae = nome_mae
    aluno.nacionalidade = nacionalidade
    aluno.uf = uf
    aluno.naturalidade = naturalidade
    aluno.save()
    turma.total_alunos = str(int(turma.total_alunos) + 1)
    turma.save()

    salvar_historico(request, aluno, edicao, 'administracao_aluno', modificacoes_aluno)