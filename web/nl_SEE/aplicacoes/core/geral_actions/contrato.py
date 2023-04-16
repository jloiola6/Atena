from aplicacoes.administracao.models import * 
from aplicacoes.core.uploads import * 
from aplicacoes.core.actions import dict_compare, salvar_historico

from aplicacoes.terceirizacao.models import *

import re


def formulario_contrato_aditivo(request, data_final, contrato, tipo):
    edicao = False

    # #Dados do Item
    data_aditivo = request.POST.get('data')
    valor_total = request.POST.get('valor_total')
    meses_vigencia = request.POST.get('meses_vigencia')

    contrato_aditivo = Contrato_aditivo()
    contrato_aditivo.tipo = tipo
    contrato_aditivo.contrato = contrato
    if tipo == 'Aditivo':
        if contrato.data_aditivo == None:
            contrato_aditivo.data_inicio = contrato.data_termino
        else:
            contrato_aditivo.data_inicio = data_final

        contrato_aditivo.data_termino = data_aditivo
    else:
        contrato_aditivo.data_inicio = data_aditivo
        contrato_aditivo.data_termino = data_final

    contrato.data_aditivo = contrato_aditivo.data_termino
    contrato.save()

    contrato_aditivo.valor_total = valor_total
    contrato_aditivo.meses_vigencia = meses_vigencia
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

    itens.pop()
    itens.pop()
    edicao = True

    if contrato.tipo_contrato  == 'Postos de trabalho - Limpeza':
        valor_maximo = 10
    elif 'Postos de trabalho' in contrato.tipo_contrato:
        valor_maximo = 9
    elif contrato.tipo_contrato in ('Produtos', 'Serviços'):
        valor_maximo = 8

    for i in range(0, len(itens)-1, valor_maximo):
        if contrato.tipo_contrato  == 'Postos de trabalho - Limpeza':
            inputs_itens = {'metragem_mensal': request.POST.get(itens[i+4]), 'valor_unitario': request.POST.get(itens[i+5]), 'quantidade': request.POST.get(itens[i+6]), 'valor_total': request.POST.get(itens[i+7]), 'status': int(request.POST.get(itens[i+9]))}
        elif 'Postos de trabalho' in contrato.tipo_contrato:
            inputs_itens = {'quantidade': request.POST.get(itens[i+3]), 'remuneracao': request.POST.get(itens[i+4]), 'valor_unitario': request.POST.get(itens[i+5]), 'valor_total': request.POST.get(itens[i+6]), 'status': int(request.POST.get(itens[i+8]))}
        elif contrato.tipo_contrato in ('Produtos', 'Serviços'):
            inputs_itens = {'quantidade': request.POST.get(itens[i+3]), 'valor_unitario': request.POST.get(itens[i+4]), 'valor_total': request.POST.get(itens[i+5]), 'status': int(request.POST.get(itens[i+7]))}

        contrato_item = Contrato_item.objects.filter(id= request.POST.get(itens[i]))
        
        modificacoes_contrato_item = dict_compare(contrato_item.values()[0], inputs_itens)
        contrato_item = contrato_item[0]

        mudanca = Contrato_item_mudanca()
        mudanca.contrato_aditivo = contrato_aditivo
        mudanca.numero_item = contrato_item.numero_item
        mudanca.numero_lote = contrato_item.numero_lote
        mudanca.metragem_contratada_antigo = contrato_item.metragem_contratada
        mudanca.metragem_mensal_antigo = contrato_item.metragem_mensal
        mudanca.descricao = contrato_item.descricao
        mudanca.quantidade_antigo = contrato_item.quantidade
        mudanca.valor_unitario_antigo = contrato_item.valor_unitario
        mudanca.valor_total_antigo = contrato_item.valor_total
        mudanca.remuneracao_antigo = contrato_item.remuneracao
        mudanca.status_antigo = contrato_item.status

        if modificacoes_contrato_item != {}:
            if contrato.tipo_contrato  == 'Postos de trabalho - Limpeza':
                contrato_item.metragem_mensal = request.POST.get(itens[i+6])
                contrato_item.valor_unitario = request.POST.get(itens[i+4])
                contrato_item.quantidade = request.POST.get(itens[i+3])
                contrato_item.valor_total = request.POST.get(itens[i+7])
                contrato_item.status = request.POST.get(itens[i+9])

                mudanca.metragem_mensal_novo = contrato_item.metragem_mensal
                mudanca.valor_unitario_novo = contrato_item.valor_unitario
                mudanca.quantidade_novo = contrato_item.quantidade
                mudanca.valor_total_novo = contrato_item.valor_total
                mudanca.status_novo = contrato_item.status

            elif 'Postos de trabalho' in contrato.tipo_contrato:
                contrato_item.quantidade = request.POST.get(itens[i+3])
                contrato_item.remuneracao = request.POST.get(itens[i+5])
                contrato_item.valor_unitario = request.POST.get(itens[i+4])
                contrato_item.valor_total = request.POST.get(itens[i+6])
                contrato_item.status = request.POST.get(itens[i+8])

                mudanca.quantidade_novo = request.POST.get(itens[i+3])
                mudanca.remuneracao_novo = request.POST.get(itens[i+5])
                mudanca.valor_unitario_novo = request.POST.get(itens[i+4])
                mudanca.valor_total_novo = request.POST.get(itens[i+6])
                mudanca.status_novo = request.POST.get(itens[i+8])

            elif contrato.tipo_contrato in ('Produtos', 'Serviços'):
                contrato_item.quantidade = request.POST.get(itens[i+3])
                contrato_item.valor_unitario = request.POST.get(itens[i+4])
                contrato_item.valor_total = request.POST.get(itens[i+5])
                contrato_item.status = request.POST.get(itens[i+7])

                mudanca.quantidade_novo = contrato_item.quantidade
                mudanca.valor_unitario_novo = contrato_item.valor_unitario
                mudanca.valor_total_novo = contrato_item.valor_total
                mudanca.status_novo = contrato_item.status

        contrato_item.save()
        salvar_historico(request, contrato_item, edicao, 'administracao_contrato_item', modificacoes_contrato_item)

        mudanca.save()
        salvar_historico(request, mudanca, edicao, 'administracao_contrato_item_mudanca')
        
        item = contrato_item
        contrato = item.contrato
        if contrato.tipo_contrato == 'Postos de trabalho - Vigilância Armada': 
            postos = Contrato_posto_vigilante.objects.filter(item= item)
            quantidade_postos = postos.count()
            vagas_restantes = int(item.quantidade) - quantidade_postos  
        elif 'Postos de trabalho' in contrato.tipo_contrato: 
            servidores = Contrato_lotacao.objects.filter(item= item, status= 1)
            quantidade_servidores = servidores.count()
            valor = (str(item.quantidade).split('.'))[0]
            vagas_restantes = int(valor) - quantidade_servidores
        
        if contrato.tipo_contrato not in ('Produtos', 'Serviços'):
            item.qtd_vagas = vagas_restantes
            if item.qtd_vagas == 0:
                item.vagas = 0
            else:
                item.vagas = 1
            item.save()


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
    # posts = request.POST
    # c = 1
    # itens = []
    # for post in posts:
    #     if c > 1:
    #         itens.append(post)
    #     else:
    #         c += 1

    # for i in range(0, len(itens), 8):
    #     gestor = Contrato_gestor()
    #     gestor.contrato = contrato
    #     gestor.atribuicao = request.POST.get(itens[i])
    #     gestor.nome = request.POST.get(itens[i+1])
    #     gestor.doe = request.POST.get(itens[i+2])
    #     gestor.portaria = request.POST.get(itens[i+3])
    #     gestor.data_portaria = request.POST.get(itens[i+4])
    #     gestor.data_publicacao = request.POST.get(itens[i+5])
    #     gestor.data_inicio = request.POST.get(itens[i+6])
    #     gestor.data_termino = request.POST.get(itens[i+7])
    #     gestor.situacao = 'Ativo'
    #     gestor.save()
    #     salvar_historico(request, gestor, edicao, 'administracao_contrato_gestor')

    gestor_titular = request.POST.get('nome1')
    atribuicao_gestor_titular = request.POST.get('tipo1')
    doe_gestor_titular = request.POST.get('doe_gestor_titular')
    portaria_gestor_titular = request.POST.get('portaria_gestor_titular')
    data_portaria_gestor_titular = request.POST.get('data_portaria_gestor_titular')
    data_publicacao_gestor_titular = request.POST.get('data_publicacao_gestor_titular')
    data_inicio_gestor_titular = request.POST.get('data_inicio_gestor_titular')
    data_termino_gestor_titular = request.POST.get('data_termino_gestor_titular')
    gestor_substituto = request.POST.get('nome2')
    atribuicao_gestor_substituto = request.POST.get('tipo2')
    doe_gestor_substituto = request.POST.get('doe_gestor_substituto')
    portaria_gestor_substituto = request.POST.get('portaria_gestor_substituto')
    data_portaria_gestor_substituto = request.POST.get('data_portaria_gestor_substituto')
    data_publicacao_gestor_substituto = request.POST.get('data_publicacao_gestor_substituto')
    data_inicio_gestor_substituto = request.POST.get('data_inicio_gestor_substituto')
    data_termino_gestor_substituto = request.POST.get('data_termino_gestor_substituto')
    fiscal_titular = request.POST.get('nome3')
    atribuicao_fiscal_titular = request.POST.get('tipo3')
    doe_fiscal_titular = request.POST.get('doe_fiscal_titular')
    portaria_fiscal_titular = request.POST.get('portaria_fiscal_titular')
    data_portaria_fiscal_titular = request.POST.get('data_portaria_fiscal_titular')
    data_publicacao_fiscal_titular = request.POST.get('data_publicacao_fiscal_titular')
    data_inicio_fiscal_titular = request.POST.get('data_inicio_fiscal_titular')
    data_termino_fiscal_titular = request.POST.get('data_termino_fiscal_titular')
    fiscal_substituto = request.POST.get('nome4')
    atribuicao_fiscal_substituto = request.POST.get('tipo4')
    doe_fiscal_substituto = request.POST.get('doe_fiscal_substituto')
    portaria_fiscal_substituto = request.POST.get('portaria_fiscal_substituto')
    data_portaria_fiscal_substituto = request.POST.get('data_portaria_fiscal_substituto')
    data_publicacao_fiscal_substituto = request.POST.get('data_publicacao_fiscal_substituto')
    data_inicio_fiscal_substituto = request.POST.get('data_inicio_fiscal_substituto')
    data_termino_fiscal_substituto = request.POST.get('data_termino_fiscal_substituto')

    if not Contrato_gestor.objects.filter(contrato= contrato, gestor_titular= gestor_titular, gestor_substituto= gestor_substituto, fiscal_titular= fiscal_titular, fiscal_substituto= fiscal_substituto).exists():
        gestores = Contrato_gestor()
        gestores.contrato = contrato
        gestores.gestor_titular = gestor_titular
        gestores.atribuicao_gestor_titular = atribuicao_gestor_titular
        gestores.doe_gestor_titular = doe_gestor_titular
        gestores.portaria_gestor_titular = portaria_gestor_titular
        gestores.data_portaria_gestor_titular = data_portaria_gestor_titular
        gestores.data_publicacao_gestor_titular = data_publicacao_gestor_titular
        gestores.data_inicio_gestor_titular = data_inicio_gestor_titular
        gestores.data_termino_gestor_titular = data_termino_gestor_titular
        gestores.gestor_substituto = gestor_substituto
        gestores.atribuicao_gestor_substituto = atribuicao_gestor_substituto
        gestores.doe_gestor_substituto = doe_gestor_substituto
        gestores.portaria_gestor_substituto = portaria_gestor_substituto
        gestores.data_portaria_gestor_substituto = data_portaria_gestor_substituto
        gestores.data_publicacao_gestor_substituto = data_publicacao_gestor_substituto
        gestores.data_inicio_gestor_substituto = data_inicio_gestor_substituto
        gestores.data_termino_gestor_substituto = data_termino_gestor_substituto
        gestores.fiscal_titular = fiscal_titular
        gestores.atribuicao_fiscal_titular = atribuicao_fiscal_titular
        gestores.doe_fiscal_titular = doe_fiscal_titular
        gestores.portaria_fiscal_titular = portaria_fiscal_titular
        gestores.data_portaria_fiscal_titular = data_portaria_fiscal_titular
        gestores.data_publicacao_fiscal_titular = data_publicacao_fiscal_titular
        gestores.data_inicio_fiscal_titular = data_inicio_fiscal_titular
        gestores.data_termino_fiscal_titular = data_termino_fiscal_titular
        gestores.fiscal_substituto = fiscal_substituto
        gestores.atribuicao_fiscal_substituto = atribuicao_fiscal_substituto
        gestores.doe_fiscal_substituto = doe_fiscal_substituto
        gestores.portaria_fiscal_substituto = portaria_fiscal_substituto
        gestores.data_portaria_fiscal_substituto = data_portaria_fiscal_substituto
        gestores.data_publicacao_fiscal_substituto = data_publicacao_fiscal_substituto
        gestores.data_inicio_fiscal_substituto = data_inicio_fiscal_substituto
        gestores.data_termino_fiscal_substituto = data_termino_fiscal_substituto
        gestores.situacao = 'Ativo'
        gestores.save()
        salvar_historico(request, gestores, edicao, 'administracao_contrato_gestor')
    
        
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
    valor = request.POST.get('naturalidade')
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
    

def formulario_postos(request, item):
    edicao = False

    tipo_unidade = request.POST.get('fieldset-tipo-unidade')

    if tipo_unidade == 'adm':
        unidade_administrativa = request.POST.get('administrativa')
    else:
        endereco = request.POST.get('endereco')

    postos = Contrato_posto_vigilante()
    postos.item = item
    if tipo_unidade == 'adm':
        postos.unidade_administrativa = Unidade_administrativa.objects.get(id= unidade_administrativa)
    else:
        postos.endereco = Endereco.objects.get(id= endereco)
    postos.vagas_ocupadas = 0
    postos.status = 1
    postos.save()
    salvar_historico(request, postos, edicao, 'administracao_contrato_posto_vigilante')
    
    vagas = item.vagas
    item.vagas = vagas - 1
    # if vagas == 0:
    #     item.vagas = 1
    # else:
    #     item.vagas = 0
    item.save()
    

def formulario_documento(request, contrato):
    edicao = False

    descricao = request.POST.get('descricao')
    arquivo = request.FILES.get('arquivo')

    versao = Contrato_documento.objects.filter(contrato= contrato).count() + 1
    if versao > 1:
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
        documento.arquivo = handle_uploaded_file(arquivo, nome, 'Contratos/', contrato.numero_contrato)
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
    