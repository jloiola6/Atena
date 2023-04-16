import re

from aplicacoes.administracao.models import *
from aplicacoes.atena.models import Cidade
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.terceirizacao.models import *

from aplicacoes.core.uploads import *


def formulario_contrato_lotacao(request, edicao, servidor):
    tipo_unidade = request.POST.get('fieldset-tipo-unidade')
    tipo_contrato = request.POST.get('fieldset-tipo-contrato')
    if tipo_contrato == 'vigilancia':
        id_posto = request.POST.get('posto_trabalho')
        posto = Contrato_posto_vigilante.objects.get(id= id_posto)
        item = posto.item

        if posto.funcionario1 == None:
            posto.funcionario1 = servidor.nome
        else:
            posto.funcionario2 = servidor.nome


        if posto.endereco != None:
            endereco = posto.endereco
            unidade_administrativa = None
        else:
            unidade_administrativa = posto.unidade_administrativa
            endereco = None
        
    else:
        id_item = request.POST.get('item')
        item = Contrato_item.objects.get(id= id_item)

        if tipo_unidade == 'adm':
            id_adm = request.POST.get('administrativa')
            unidade_administrativa = Unidade_administrativa.objects.get(id= id_adm)
            endereco = None
        else:
            id_endereco = request.POST.get('endereco')
            endereco = Endereco.objects.get(id= id_endereco)
            unidade_administrativa = None

    inicio = request.POST.get('inicio')
    carga_horaria = request.POST.get('carga_horaria')

    if not Contrato_lotacao.objects.filter(item= item, servidor= servidor, status= 1).exists():
        lotacao = Contrato_lotacao()
        modificacoes_lotacao = None

        if tipo_contrato == 'vigilancia':
            lotacao.posto = posto

        lotacao.servidor = servidor
        lotacao.item = item
        lotacao.endereco = endereco
        lotacao.unidade_administrativa = unidade_administrativa
        lotacao.data_inicio = inicio
        lotacao.data_termino = item.contrato.data_termino
        lotacao.status = 1
        lotacao.carga_horaria = carga_horaria
        lotacao.save()

        vagas = item.qtd_vagas - 1
        item.qtd_vagas = vagas
        if vagas == 0:
            item.vagas = 0
        else:
            item.vagas = 1

        item.save()
        
        if tipo_contrato == 'vigilancia':
            vagas_posto = posto.vagas_ocupadas + 1
            posto.vagas_ocupadas = vagas_posto
            posto.save()

        salvar_historico(request, lotacao, edicao, 'terceirizacao_contrato_lotacao', modificacoes_lotacao)
    

def contrato_finalizar(request, lotacao):
    edicao = False

    item = lotacao.item
    vagas = item.qtd_vagas + 1
    item.qtd_vagas = vagas    
    item.vagas = 1
    item.save()

    data_finalizacao = request.POST.get('data_finalizacao')
    motivo = request.POST.get('motivo')

    lotacao.motivo = motivo
    lotacao.data_termino = data_finalizacao
    lotacao.status = 0
    lotacao.save()

    if lotacao.posto != None:
        posto = lotacao.posto
        if posto.funcionario1 == lotacao.servidor.nome:
            posto.funcionario1 = None
        else:
            posto.funcionario2 = None

        vagas_ocupadas = posto.vagas_ocupadas - 1
        posto.vagas_ocupadas = vagas_ocupadas
        posto.save()

    salvar_historico(request, lotacao, edicao, 'terceirizacao_contrato_lotacao')


def formulario_ocorrencia_terceirizacao(request, contrato):
    edicao = False

    tipo_ocorrencia = request.POST.get('tipo_ocorrencia')
    data_inicio = request.POST.get('data_inicio')
    data_final = request.POST.get('data_final')
    subtituto = request.POST.get('substituto')
    # documento = request.POST.get('documento')
    if not Servidor_ocorrencia_funcional.objects.filter(contrato= contrato, tipo_ocorrencia= tipo_ocorrencia, data_inicio= data_inicio, data_termino= data_final ).exists():
        ocorrencia = Servidor_ocorrencia_funcional()
        ocorrencia.substituto = subtituto
        ocorrencia.contrato = contrato
        ocorrencia.tipo_ocorrencia = tipo_ocorrencia
        ocorrencia.data_inicio = data_inicio
        ocorrencia.data_termino = data_final
        ocorrencia.status = 1
        # ocorrencia.documento = documento
        ocorrencia.save()
        salvar_historico(request, ocorrencia, edicao, 'tercerizacao_servidor_ocorrencia_funcional')
    