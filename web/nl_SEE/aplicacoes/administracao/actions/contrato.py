from aplicacoes.administracao.models import * 
from aplicacoes.core.actions import dict_compare, salvar_historico

from aplicacoes.terceirizacao.models import *

import re


def formulario_item_limpeza(request, contrato, itens):
    edicao = False

    for i in range(0, len(itens)-1, 8):    
        contrato_item = Contrato_item()
        contrato_item.contrato = contrato
        contrato_item.numero_item = request.POST.get(itens[i])
        contrato_item.numero_lote = request.POST.get(itens[i+1])
        contrato_item.metragem_contratada = request.POST.get(itens[i+2])
        contrato_item.metragem_mensal = request.POST.get(itens[i+3])
        contrato_item.valor_unitario = request.POST.get(itens[i+4])
        contrato_item.quantidade = request.POST.get(itens[i+5])
        qtd_vagas = request.POST.get(itens[i+5]).split('.')[0]
        contrato_item.qtd_vagas = int(qtd_vagas)
        contrato_item.valor_total = request.POST.get(itens[i+6])
        contrato_item.descricao = request.POST.get(itens[i+7])

        if qtd_vagas == 0:
            contrato_item.vagas = 0
        else:
            contrato_item.vagas = 1

        contrato_item.status = 1
        contrato_item.save()
        salvar_historico(request, contrato_item, edicao, 'administracao_contrato_item')    

    valor_total = request.POST.get('valor_total_contrato')
    valor_global = request.POST.get('valor_global')
    meses_vigencia = request.POST.get('meses_vigencia')
    contrato.valor_total = valor_total
    contrato.valor_global = valor_global
    contrato.meses_vigencia = meses_vigencia
    contrato.save()

    return contrato
    

def formulario_item_padrao(request, contrato, itens):
    edicao = False

    for i in range(0, len(itens)-1, 6):    
        contrato_item = Contrato_item()
        contrato_item.contrato = contrato
        contrato_item.numero_item = request.POST.get(itens[i])
        contrato_item.numero_lote = request.POST.get(itens[i+1])
        contrato_item.quantidade = request.POST.get(itens[i+2])
        qtd_vagas = request.POST.get(itens[i+2]).split('.')[0]
        contrato_item.qtd_vagas = int(qtd_vagas)
        contrato_item.valor_unitario = request.POST.get(itens[i+3])
        contrato_item.valor_total = request.POST.get(itens[i+4])
        contrato_item.descricao = request.POST.get(itens[i+5])

        if qtd_vagas == 0:
            contrato_item.vagas = 0
        else:
            contrato_item.vagas = 1

        contrato_item.status = 1
        
        contrato_item.save()
        salvar_historico(request, contrato_item, edicao, 'administracao_contrato_item')    

    valor_total = request.POST.get('valor_total_contrato')
    valor_global = request.POST.get('valor_global')
    meses_vigencia = request.POST.get('meses_vigencia')
    contrato.valor_total = valor_total
    contrato.valor_global = valor_global
    contrato.meses_vigencia = meses_vigencia
    contrato.save()

    return contrato


def formulario_item_trabalho(request, contrato, itens):
    edicao = False

    for i in range(0, len(itens)-1, 7):    
        contrato_item = Contrato_item()
        contrato_item.contrato = contrato
        contrato_item.numero_item = request.POST.get(itens[i])
        contrato_item.numero_lote = request.POST.get(itens[i+1])
        contrato_item.quantidade = request.POST.get(itens[i+2])
        qtd_vagas = request.POST.get(itens[i+2]).split('.')[0]
        contrato_item.qtd_vagas = int(qtd_vagas)
        contrato_item.remuneracao = request.POST.get(itens[i+3])
        contrato_item.valor_unitario = request.POST.get(itens[i+4])
        contrato_item.valor_total = request.POST.get(itens[i+5])
        contrato_item.descricao = request.POST.get(itens[i+6])

        if qtd_vagas == 0:
            contrato_item.vagas = 0
        else:
            contrato_item.vagas = 1

        contrato_item.status = 1
        
        contrato_item.save()
        salvar_historico(request, contrato_item, edicao, 'administracao_contrato_item')    

    valor_total = request.POST.get('valor_total_contrato')
    valor_global = request.POST.get('valor_global')
    meses_vigencia = request.POST.get('meses_vigencia')
    contrato.valor_total = valor_total
    contrato.valor_global = valor_global
    contrato.meses_vigencia = meses_vigencia
    contrato.save()

    return contrato


def formulario_contrato(request):
    edicao = False

    #Dados do Item
    tipo_contrato = request.POST.get('tipo_contrato')
    unidade_administrativa = request.POST.get('administrativa')
    numero_contrato = request.POST.get('numero_contrato')
    id_empresa = request.POST.get('empresa')
    numero_sei = request.POST.get('numero_sei')
    documento_sei = request.POST.get('numero_documento_sei')
    objeto = request.POST.get('objeto')
    data_inicio = request.POST.get('data_inicio')
    data_termino = request.POST.get('data_termino')
    fonte_recurso = request.POST.get('fonte_recurso')
    situacao = request.POST.get('situacao')

    contrato = Contrato_contrato()
    contrato.tipo_contrato = tipo_contrato
    contrato.numero_contrato = numero_contrato
    contrato.empresa = Contrato_empresa.objects.get(id = id_empresa)
    contrato.numero_sei = numero_sei
    contrato.documento_sei = documento_sei
    contrato.objeto = objeto
    contrato.data_inicio = data_inicio
    contrato.data_termino = data_termino
    contrato.fonte_recurso = fonte_recurso
    contrato.situacao = situacao
    contrato.save()
    salvar_historico(request, contrato, edicao, 'administracao_contrato_contrato')

    fonte_contrato = Fonte_contrato()
    fonte_contrato.contrato = contrato
    fonte_contrato.fonte_recurso = fonte_recurso
    fonte_contrato.save()
    salvar_historico(request, fonte_contrato, edicao, 'administracao_fonte_contrato')

    vinculacao_contrato = Vinculacao_contrato()
    vinculacao_contrato.contrato = contrato
    vinculacao_contrato.unidade_administrativa = Unidade_administrativa.objects.get(id= unidade_administrativa)
    vinculacao_contrato.save()
    salvar_historico(request, vinculacao_contrato, edicao, 'administracao_vinculacao_contrato')

    posts = request.POST
    c = 1
    itens = []
    for post in posts:
        if c > 12:
            itens.append(post)
        else:
            c += 1
    
    for i in range(3):
        del itens[-1]

    if tipo_contrato == 'Postos de trabalho - Limpeza':
        formulario_item_limpeza(request, contrato, itens)
    elif tipo_contrato in ('Produtos', 'Serviços'):
        formulario_item_padrao(request, contrato, itens)
    elif tipo_contrato in ('Postos de trabalho', 'Postos de trabalho - Vigilância Armada'):
        formulario_item_trabalho(request, contrato, itens)

    return contrato


def formulario_empresa(request):
    edicao = False

    #Dados da Empresa
    nome = request.POST.get('nome')
    razao_social = request.POST.get('razao_social')
    cnpj = request.POST.get('cnpj')
    cnpj = re.sub('\D', '', cnpj)
    telefone = request.POST.get('telefone')
    telefone = re.sub('\D', '', telefone)
    email = request.POST.get('email')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    bairro = request.POST.get('bairro')
    cep = request.POST.get('cep')
    cep = re.sub('\D', '', cep)
    
    valor = request.POST.get('naturalidade')
    naturalidade = valor.split('-')
    municipio = naturalidade[0]
    uf = naturalidade[1]

    contrato = Contrato_empresa()
    contrato.nome = nome
    contrato.razao_social = razao_social
    contrato.cnpj = cnpj
    contrato.telefone = telefone
    contrato.email = email
    contrato.rua = rua
    contrato.numero = numero
    contrato.bairro = bairro
    contrato.cep = cep
    contrato.municipio = municipio
    contrato.uf = uf
    contrato.save()
    salvar_historico(request, contrato, edicao, 'administracao_contrato_empesa')

