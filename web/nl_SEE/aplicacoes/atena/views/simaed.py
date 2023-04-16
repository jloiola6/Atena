from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.atena.models import *
from aplicacoes.administracao.models import *

from aplicacoes.atena.actions.simaed import *

from datetime import datetime
import pandas as pd

import time

# VIEWS E FUNÇÕES PARA A IMPORTAÇÃO DE DADOS DO SIMAED


def simaed(request):
    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'atena/simaed/index.html'

    importacoes = Importacao_simaed.objects.all().order_by('-id')

    if request.POST and request.FILES.get('arquivo'):
        # validar_arquivo(request)
        nova_importacao(request)

    return TemplateResponse(request, template_name, locals())


def importacao(request, id_importacao):
    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'atena/simaed/importacao.html'

    try:
        importacao = Importacao_simaed.objects.get(id= id_importacao)
    except:
        return HttpResponseRedirect('/atena/simaed')

    qtd_enturmacoes = Aux_simaed.objects.filter(importacao_simaed= importacao).count()

    escolas = Aux_simaed.objects.filter(importacao_simaed= importacao).values('inep_escola', 'escola').distinct().order_by('escola')
    qtd_escolas = escolas.count()

    if request.POST and 'importar-tudo' in request.POST:
        print('ENTURMAÇÕES ZERADAS')
        print()

        for escola in escolas:
            print(escola['inep_escola'], escola['escola'])
            migrar_enturmacoes(escola['inep_escola'], importacao)
            print()

    return TemplateResponse(request, template_name, locals())


def escola(request, id_importacao, inep):
    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'atena/simaed/escola.html'

    try:
        importacao = Importacao_simaed.objects.get(id= id_importacao)
        escola = Escola.objects.get(cod_inep= inep)
    except:
        return HttpResponseRedirect('/atena/simaed')

    turmas = Aux_simaed.objects.filter(inep_escola= inep, importacao_simaed= importacao).values('turma', 'etapa', 'nivel', 'turno', 'periodo_letivo').distinct().order_by('etapa')

    for turma in turmas:
        turma['alunos'] = Aux_simaed.objects.filter(inep_escola = inep, importacao_simaed= importacao, turma= turma['turma'], etapa= turma['etapa'], nivel= turma['nivel'], turno= turma['turno'], periodo_letivo= turma['periodo_letivo']).order_by('nome_aluno')
        turma['qtd_alunos'] = turma['alunos'].count()

    etapas = Aux_simaed.objects.filter(inep_escola= inep, importacao_simaed= importacao).values('nivel').distinct().order_by('nivel')

    for etapa in etapas:
        etapa['nome'] = Etapa.objects.get(id= etapa['nivel']).nome

    qtd_turmas = turmas.count()

    if request.POST and 'importar-escola' in request.POST:
        migrar_enturmacoes(inep)


    return TemplateResponse(request, template_name, locals())