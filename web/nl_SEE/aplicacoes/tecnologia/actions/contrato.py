from traceback import print_tb
from requests import post
from aplicacoes.administracao.models import *
from aplicacoes.core.uploads import *
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.atena.models import Cidade

import re

def formulario_contrato_aditivo(request, data_final):
    edicao = False
    contrato = Contrato_contrato.objects.get(id= request.GET.get('id_contrato'))

    #Dados do Item
    data_aditivo = request.POST.get('data_termino')
    valor_total = request.POST.get('valor_total')

    contrato_aditivo = Contrato_aditivo()
    contrato_aditivo.contrato = contrato
    contrato_aditivo.data_inicio = data_final
    contrato_aditivo.data_termino = data_aditivo
    contrato_aditivo.valor_total = valor_total
    contrato_aditivo.save()
    salvar_historico(request, contrato_aditivo, edicao, 'administracao_contrato_aditivo')


    posts = request.POST
    c = 1
    itens = []
    for i in posts:
        if c > 2:
            itens.append(i)
        else:
            c += 1
    del itens[-1]

    edicao = True
    for i in range(0, len(itens)-1, 7):
        contrato_item = Contrato_item.objects.filter(contrato= contrato, numero_item= request.POST.get(itens[i]))
        inputs_itens = {'quantidade': request.POST.get(itens[i+3]), 'valor_unitario': request.POST.get(itens[i+4]), 'valor_total': request.POST.get(itens[i+5]), 'status': int(request.POST.get(itens[i+6]))}
        modificacoes_contrato_item = dict_compare(contrato_item.values()[0], inputs_itens)
        contrato_item = contrato_item[0]

        # mudanca_item = False
        # if modificacoes_contrato_item != {}:
            # mudanca_item = True
        mudanca = Contrato_item_mudanca()
        mudanca.numero_item = contrato_item.numero_item
        mudanca.numero_lote = contrato_item.numero_lote
        mudanca.descricao = contrato_item.descricao
        mudanca.quantidade_antigo = contrato_item.quantidade
        mudanca.valor_unitario_antigo = contrato_item.valor_unitario
        mudanca.valor_total_antigo = contrato_item.valor_total
        mudanca.status_antigo = contrato_item.status

        contrato_item.quantidade = request.POST.get(itens[i+3])
        contrato_item.valor_unitario = request.POST.get(itens[i+4])
        contrato_item.valor_total = request.POST.get(itens[i+5])
        contrato_item.status = int(request.POST.get(itens[i+6]))
        contrato_item.save()
        salvar_historico(request, contrato_item, edicao, 'administracao_contrato_item', modificacoes_contrato_item)

        # if mudanca_item:
        #     edicao = False
        mudanca.quantidade_novo = contrato_item.quantidade
        mudanca.valor_unitario_novo = contrato_item.valor_unitario
        mudanca.valor_total_novo = contrato_item.valor_total
        mudanca.contrato_aditivo = contrato_aditivo
        mudanca.status_novo = int(request.POST.get(itens[i+6]))
        mudanca.save()
        salvar_historico(request, mudanca, edicao, 'administracao_contrato_item_mudanca')

    # valor_total = request.POST.get('valor_total_contrato')
    contrato.data_aditivo = data_aditivo
    contrato.valor_total_aditivo = valor_total
    contrato.save()


def formulario_fonte(request, contrato):
    edicao = False
    fonte_recurso = request.POST.get('fonte_recurso')

    fonte_contrato = Fonte_contrato()
    fonte_contrato.contrato = contrato
    fonte_contrato.fonte_recurso = fonte_recurso
    fonte_contrato.save()
    salvar_historico(request, fonte_contrato, edicao, 'administracao_fonte_contrato')


def formulario_gestores(request, contrato):
    edicao = False

    posts = request.POST
    c = 1
    itens = []
    for post in posts:
        if c > 1:
            itens.append(post)
        else:
            c += 1

    for i in range(0, len(itens), 8):
        gestor = Contrato_gestor()
        gestor.contrato = contrato
        gestor.atribuicao = request.POST.get(itens[i])
        gestor.nome = request.POST.get(itens[i+1])
        gestor.doe = request.POST.get(itens[i+2])
        gestor.portaria = request.POST.get(itens[i+3])
        gestor.data_portaria = request.POST.get(itens[i+4])
        gestor.data_publicacao = request.POST.get(itens[i+5])
        gestor.data_inicio = request.POST.get(itens[i+6])
        gestor.data_termino = request.POST.get(itens[i+7])
        gestor.situacao = 'Ativo'
        gestor.save()
        salvar_historico(request, gestor, edicao, 'administracao_contrato_gestor')


def formulario_fiscais(request, contrato):
    edicao = False

    posts = request.POST
    c = 1
    itens = []
    for post in posts:
        if c > 1:
            itens.append(post)
        else:
            c += 1

    for i in range(0, len(itens), 8):
        gestor = Contrato_gestor()
        gestor.contrato = contrato
        gestor.atribuicao = request.POST.get(itens[i])
        gestor.nome = request.POST.get(itens[i+1])
        gestor.doe = request.POST.get(itens[i+2])
        gestor.portaria = request.POST.get(itens[i+3])
        gestor.data_portaria = request.POST.get(itens[i+4])
        gestor.data_publicacao = request.POST.get(itens[i+5])
        gestor.data_inicio = request.POST.get(itens[i+6])
        gestor.data_termino = request.POST.get(itens[i+7])
        gestor.situacao = 'Ativo'
        gestor.save()
        salvar_historico(request, gestor, edicao, 'administracao_contrato_gestor')


def formulario_fiscais(request, contrato):
    edicao = False

    posts = request.POST
    c = 1
    itens = []
    for post in posts:
        if c > 1:
            itens.append(post)
        else:
            c += 1

    for i in range(0, len(itens), 8):
        gestor = Contrato_gestor()
        gestor.contrato = contrato
        gestor.atribuicao = request.POST.get(itens[i])
        gestor.nome = request.POST.get(itens[i+1])
        gestor.doe = request.POST.get(itens[i+2])
        gestor.portaria = request.POST.get(itens[i+3])
        gestor.data_portaria = request.POST.get(itens[i+4])
        gestor.data_publicacao = request.POST.get(itens[i+5])
        gestor.data_inicio = request.POST.get(itens[i+6])
        gestor.data_termino = request.POST.get(itens[i+7])
        gestor.situacao = 'Ativo'
        gestor.save()
        salvar_historico(request, gestor, edicao, 'administracao_contrato_gestor')


def formulario_responsavel(request, contrato):
    edicao = False

    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    cpf = re.sub('\D', '', cpf)
    rg = request.POST.get('rg')
    orgao = request.POST.get('orgao')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    bairro = request.POST.get('bairro')
    cep = request.POST.get('cep')
    cep = re.sub('\D', '', cep)
    valor = request.POST.get('municipio')
    valor = valor.split('-')
    municipio = valor[0]
    uf = valor[1]


    responsavel = Contrato_responsavel()
    responsavel.contrato = contrato
    responsavel.nome = nome
    responsavel.cpf = cpf
    responsavel.rg = rg
    responsavel.orgao = orgao
    responsavel.rua = rua
    responsavel.numero = numero
    responsavel.bairro = bairro
    responsavel.cep = cep
    responsavel.municipio = municipio
    responsavel.uf = uf
    responsavel.save()
    salvar_historico(request, responsavel, edicao, 'administracao_contrato_responsavel')


def formulario_documento(request, contrato):
    edicao = False

    descricao = request.POST.get('descricao')
    arquivo = request.FILES.get('arquivo')

    versao = Contrato_documento.objects.filter(contrato= contrato).count() + 1
    if versao > 0:
        nome = f'Documento({versao}).' + str(arquivo).split('.')[-1]
    else:
        nome = 'Documento.' + str(arquivo).split('.')[-1]


    documento = Contrato_documento()
    documento.contrato = contrato
    documento.descricao = descricao
    documento.arquivo = handle_uploaded_file(arquivo, nome, contrato.numero_contrato)

    documento.save()

    salvar_historico(request, documento, edicao, 'administracao_contrato_documento')


def formulario_empenho(request, fonte, contrato):
    edicao = False

    tipo = request.POST.get('tipo')
    numero_empenho = request.POST.get('numero_empenho')
    data_emissao = request.POST.get('data_emissao')
    cod_orcamentario = request.POST.get('cod_orcamentario')
    cod_despesa = request.POST.get('cod_despesa')
    valor = request.POST.get('valor')
    arquivo = request.FILES.get('arquivo')

    empenho = Contrato_empenho()

    if arquivo != None and arquivo != '':
        versao = Contrato_documento.objects.filter(contrato= contrato).count() + 1
        if versao > 0:
            nome = f'Documento({versao}).' + str(arquivo).split('.')[-1]
        else:
            nome = 'Documento.' + str(arquivo).split('.')[-1]

        documento = Contrato_documento()
        documento.contrato = contrato
        documento.descricao = f'Empenho ({fonte}): {numero_empenho}'
        documento.arquivo = handle_uploaded_file(arquivo, nome, contrato.numero_contrato)
        documento.save()
        salvar_historico(request, documento, edicao, 'administracao_contrato_documento')

        empenho.documento = documento

    empenho.fonte = fonte
    empenho.tipo = tipo
    empenho.num_empenho = numero_empenho
    empenho.data_emissao = data_emissao
    empenho.cod_orcamento = cod_orcamentario
    empenho.cod_despesa = cod_despesa
    empenho.valor = valor
    empenho.save()
    salvar_historico(request, empenho, edicao, 'administracao_contrato_empenho')