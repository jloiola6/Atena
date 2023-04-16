from itertools import chain

from .models import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import *
from aplicacoes.terceirizacao.models import Contrato_lotacao

import re


def filtro_unidades(request, enderecos, municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes):
    filtro_indigena = False
    inep = request.GET.get('cod_inep')
    nome = request.GET.get('nome_unidade')

    #Filtro pelo INEP
    if inep != None and inep != '':
        enderecos = enderecos.filter(escola__cod_inep= int(inep))
    
    #Filtro pelo Nome
    if nome != None and nome != '':
        enderecos = enderecos.filter(escola__nome_escola__icontains= nome)
    
    #Filtro pelo tipo de localização
    localizacao_filtro = []
    for localizacao in tipo_localizacao:
        if request.GET.get(localizacao[1]) == 'on':
            localizacao_filtro.append(localizacao[2])
            if localizacao[0] == 'id-indigena':
                filtro_indigena = True
    if len(localizacao_filtro) > 0:
        enderecos = enderecos.filter(tipo_localizacao__in= localizacao_filtro)

    # Filtro pela Modalidade
    # modalidades_filtro = []
    # for modalidade in name_modalidades:
    #     name = modalidade.replace('_', ' ')
    #     if request.GET.get(name) == 'on':
    #         modalidades_filtro.append(name)
    # if len(modalidades_filtro) > 0:
    #     modalidades_escola = Modalidade_escola.objects.filter(modalidade__nome__in= modalidades_filtro).values('escola__id')
    #     escolas = []
    #     for modalidade in modalidades_escola:
    #         escolas.append(modalidade['escola__id'])
        
    #     enderecos = enderecos.filter(escola__id__in= escolas)

    #Filtro pela Tipificação
    tipificacao_filtro = []
    for tipíficacao in name_tipificacoes:
        if request.GET.get(tipíficacao) == 'on':
            tipificacao_filtro.append(tipíficacao)
    if len(tipificacao_filtro) > 0:
        enderecos = enderecos.filter(escola__tipificacao__in= tipificacao_filtro)


    #Filtro pela Etapas
    etapas_filtro = []
    for etapa in name_etapas:
        if request.GET.get(etapa) == 'on':
            name = (etapa).replace('_', ' ')
            etapas_filtro.append(name)
    if len(etapas_filtro) > 0:
        escolas_etapas = Etapa_escola.objects.filter(etapa__nome__in= etapas_filtro).values('escola_id').distinct()
        escolas = []
        for escola in escolas_etapas:
            escolas.append(escola['escola_id'])

        enderecos = enderecos.filter(escola__id__in= escolas)

    #Filtro pelo Municipio
    municipio_filtro = []
    for municipio in municipios:
        if request.GET.get(municipio) == 'on':
            municipio_filtro.append(municipio.replace('-', ' '))
    
    #Filtro pela Regional
    regioes_filtro = []
    for item in range(len(regioes)):
        if request.GET.get(name_regioes[item]) == 'on':
            regioes_filtro.append(regioes[item])
    
    if len(regioes_filtro) > 0 and len(municipio_filtro) > 0:
        enderecos = list(chain(enderecos.filter(regiao__in= regioes_filtro), enderecos.filter(municipio__in= municipio_filtro)))
    elif len(regioes_filtro) > 0:
        enderecos = enderecos.filter(regiao__in= regioes_filtro)
    elif len(municipio_filtro) > 0:
        enderecos = enderecos.filter(municipio__in= municipio_filtro)

    if filtro_indigena:
        etnia_filtro = []
        for etnia in name_etnia:
            if request.GET.get(etnia) == 'on':
                name = (etnia).replace('ETNIA_', '').replace('_', ' ')
                etnia_filtro.append(name)
        if len(etnia_filtro) > 0:
            detalhes_indigena = Detalhes_Indigena.objects.filter(etnia__in= etnia_filtro).values('escola_id') 
            escolas = []
            for turma in detalhes_indigena:
                escolas.append(turma['escola_id'])
            
            enderecos = enderecos.filter(escola__id__in= escolas)

        localizacao_filtro = []
        for localizacao in name_localizacao:
            if request.GET.get(localizacao) == 'on':
                name = (localizacao).replace('LOCALIZACAO_', '').replace('_', ' ')
                localizacao_filtro.append(name)
        if len(localizacao_filtro) > 0:
            detalhes_indigena = Detalhes_Indigena.objects.filter(localizacao__in= localizacao_filtro).values('escola_id')
            escolas = []
            for turma in detalhes_indigena:
                escolas.append(turma['escola_id'])

            enderecos = enderecos.filter(escola__id__in= escolas)

        aldeia_filtro = []
        for aldeia in name_aldeia:
            if request.GET.get(aldeia) == 'on':
                name = (aldeia).replace('ALDEIA_', '').replace('_', ' ')
                aldeia_filtro.append(name)
        if len(aldeia_filtro) > 0:
            detalhes_indigena = Detalhes_Indigena.objects.filter(aldeia__in= aldeia_filtro).values('escola_id')
            escolas = []
            for turma in detalhes_indigena:
                escolas.append(turma['escola_id'])

            enderecos = enderecos.filter(escola__id__in= escolas)

    return enderecos
