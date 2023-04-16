from datetime import datetime
from pytz import timezone

from .models import Historico
from aplicacoes.usuario.models import Logs
from aplicacoes.terceirizacao.models import *
from aplicacoes.core.models import *
from aplicacoes.administracao.models import *

import hashlib
from datetime import datetime


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}

    return modified

def salvar_historico(request, objeto, edicao, tabela, modificacoes=None, excluir= None):
    data = datetime.now().astimezone(timezone('America/Rio_Branco'))
    data = data.strftime("%d/%m/%Y %H:%M:%S")

    historico = Historico()
    historico.tabela = tabela
    usuario = request.session['username']


    historico.log = log = Logs.objects.filter(usuario__login= usuario).last()
    historico.objeto = objeto.id
    historico.data = data
    if edicao:
        if excluir == True:
            historico.acao = 'R'
            historico.modificacao = modificacoes
        else:
            historico.acao = 'E'
            historico.modificacao = modificacoes
    else:
        historico.acao = 'A'

    historico.save()

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
        contrato_aditivo.data_inicio = data_final
        contrato_aditivo.data_termino = data_aditivo
    else:
        contrato_aditivo.data_inicio = data_aditivo
        contrato_aditivo.data_termino = data_final

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

def alterar_senha(request, usuario):
    password = request.POST.get("nova-senha")
    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    usuario.senha = password
    usuario.save()

    request.session['atualizar-senha'] = False

def verificar_lotacao(request):
    lotacao_id = request.POST.get('lotacao')
    tipo_unidade = request.POST.get('tipo-unidade')
    tipo_situacao = request.POST.get('confirma-situacao')
    unidade_adm = request.POST.get('unidade-adm')
    unidade_escolar = request.POST.get('unidade-escolar')
    terceirizado = request.POST.get('terceirizado')
    unidade_administrativa= Unidade_administrativa.objects.get(id= unidade_adm)
    unidade_educacional= Escola.objects.get(id= unidade_escolar)
    data= datetime.now()

    lotacao= Confirmacao_lotacao()

    lotacao.data_atualizacao= data
    if terceirizado != '' and terceirizado != None:
        lotacao.terceirizado = Contrato_lotacao.objects.get(id = lotacao_id)
        lotacao.lotacao = None
    else:
        lotacao.lotacao = Servidor_lotacao.objects.get(id= lotacao_id)
        lotacao.terceirizado = None
    if tipo_situacao == "correta":
        lotacao.alteracao_lotacao=0
    else:
        lotacao.alteracao_lotacao=1

        if tipo_unidade == "escolar":
            lotacao.unidade_escolar= unidade_educacional

        if tipo_unidade == "adm":
            lotacao.unidade_adm= unidade_administrativa



    lotacao.save()