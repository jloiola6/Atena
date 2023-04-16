from http import server
from django.core.paginator import Paginator
from itertools import chain
import re

from .models import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import *
from aplicacoes.terceirizacao.models import *


def filtro_servidores(request):
    id_servidores = Contrato_lotacao.objects.values_list('servidor_id', flat=True).distinct()
    servidores = Servidor.objects.filter(id__in = id_servidores).order_by('nome')

    cpf = request.GET.get('cpf')
    nome = request.GET.get('nome')

    #Filtro pelo CPF
    if cpf != None and cpf != '':
        cpf = re.sub('\D', '', cpf)
        servidores = servidores.filter(cpf= cpf)
    #Filtro pelo Nome
    elif nome != None and nome != '':
        nome = nome.upper()
        if servidores.filter(nome__contains= nome).count() > 0:
            servidores = servidores.filter(nome__icontains= nome)
        else:
            servidores = servidores.filter(nome__icontains= nome.upper())

    return servidores

def filtro_lotacoes(request):
    lotacoes = Contrato_lotacao.objects.filter(status= 1).order_by('servidor__nome')
    cpf = request.GET.get('cpf')
    funcao = request.GET.get('funcao')
    nome = request.GET.get('nome')
    administrativa = request.GET.get('administrativa')
    empresa = request.GET.get('empresa')
    numero_contrato = request.GET.get('numero_contrato')
    educacional = request.GET.get('educacional')

    id_contratos = []
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 78).values('contrato'):
            id_contratos.append(id['contrato'])
    itens = Contrato_item.objects.filter(vagas= 1, contrato__id__in= id_contratos)

    servidor_Contrato = request.GET.get('numero_contrato')
    empresa = request.GET.get('empresa')
    municipio = request.GET.get('municipio')

    if numero_contrato != None and numero_contrato != '':
        lotacoes = lotacoes.filter(item__contrato__numero_contrato__contains= numero_contrato)

    #Filtro pelo CPF
    if cpf != None and cpf != '':
        cpf = re.sub('\D', '', cpf)
        lotacoes = lotacoes.filter(servidor__cpf= cpf)

    if funcao != None and funcao != '':
        lotacoes = lotacoes.filter(item__descricao__icontains = funcao )

    #Filtro pelo Nome
    if nome != None and nome != '':
        nome = nome.upper()
        lotacoes = lotacoes.filter(servidor__nome__contains= nome)

    if administrativa != None and administrativa != '':
        lotacoes = lotacoes.filter(unidade_administrativa= administrativa)

    if educacional != None and educacional != '':
        lotacoes = lotacoes.filter(endereco= educacional)

    if empresa != None and empresa != '':
        id_contratos = []
        for contrato in Contrato_contrato.objects.filter(empresa__id= empresa).values('id'):
            if contrato not in id_contratos:
                id_contratos.append(contrato['id'])

        id_itens = []
        for item in Contrato_item.objects.filter(contrato__in= id_contratos).values('id'):
            if item not in id_itens:
                id_itens.append(item['id'])

        lotacoes = lotacoes.filter(item__in= id_itens)

    if municipio != None and municipio != '':
        lotacoes = lotacoes.filter(endereco__municipio = municipio)

    return lotacoes

def filtro_servidores_unidade(request):
    id_unidade = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    id_unidades = []
    id_unidades.append(unidade.id)

    if unidade.categoria.id == 2:
        departamentos = Unidade_administrativa.objects.filter(categoria = 3, hierarquia= unidade.id)
        divisoes = Unidade_administrativa.objects.filter(categoria= 4)
        nucleos = Unidade_administrativa.objects.filter(categoria= 5)

        for departamento in departamentos:
            id_unidades.append(departamento.id)

            for divisao in divisoes:
                if divisao.hierarquia == departamento.id:
                    id_unidades.append(divisao.id)

                    for nucleo in nucleos:
                        if nucleo.hierarquia == divisao.id:
                            id_unidades.append(nucleo.id)

    elif unidade.categoria.id == 3:
        divisoes = Unidade_administrativa.objects.filter(categoria= 4, hierarquia= unidade.id)
        nucleos = Unidade_administrativa.objects.filter(categoria= 5)

        for divisao in divisoes:
            id_unidades.append(divisao.id)

            for nucleo in nucleos:
                if nucleo.hierarquia == divisao.id:
                    id_unidades.append(nucleo.id)

    elif unidade.categoria.id == 4:
        nucleos = Unidade_administrativa.objects.filter(hierarquia= unidade.id)

        for nucleo in nucleos:
            id_unidades.append(nucleo.id)

    lotacoes = Servidor_lotacao.objects.filter(unidade_adm__in= id_unidades, status= 1)
    terceirizados = Contrato_lotacao.objects.filter(unidade_administrativa__in= id_unidades, status= 1)

    cpf = request.GET.get('cpf')
    matricula = (request.GET.get('matricula'))
    nome = request.GET.get('nome')

    if cpf != None and cpf != '':
        cpf = re.sub('\D', '', cpf)
        lotacoes = lotacoes.filter(contrato__servidor__cpf= cpf)
        terceirizados = terceirizados.filter(servidor__cpf= cpf)

    elif matricula != None and matricula != '':
        lotacoes = lotacoes.filter(contrato__servidor__matricula= matricula)
        terceirizados = terceirizados.filter(servidor__matricula= matricula)

    elif nome != None and nome != '':
        nome = nome.upper()
        lotacoes = lotacoes.filter(contrato__servidor__nome__contains= nome)
        terceirizados = terceirizados.filter(servidor__nome__contains= nome)


    qr_servidores = list(chain(lotacoes, terceirizados))

    servidores = []
    for servidor in qr_servidores:
        try:
            if servidor.unidade_administrativa:
                servidores.append((servidor.servidor.nome, servidor.unidade_administrativa, servidor.item.descricao, 'Terceirizado'))
            else:
                servidores.append((servidor.servidor.nome, servidor.endereco, servidor.item.descricao, 'Terceirizado'))
        except:
            if servidor.unidade_escolar:
                servidores.append((servidor.contrato.servidor, servidor.unidade_escolar, servidor.contrato.cargo.nome, 'SEE'))
            else:
                servidores.append((servidor.contrato.servidor, servidor.unidade_adm, servidor.contrato.cargo.nome, 'SEE'))

    return servidores

def filtro_vagas(request):
    id_contratos = []
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 78).values('contrato'):
        id_contratos.append(id['contrato'])
    itens = Contrato_item.objects.filter(vagas= 1, contrato__id__in= id_contratos).order_by('-qtd_vagas')

    numero_contrato = request.GET.get('numero_contrato')
    empresa = request.GET.get('empresa')

    if numero_contrato != None and numero_contrato != '':
        itens = itens.filter(contrato__numero_contrato__contains= numero_contrato)

    if empresa != None and empresa != '':
        itens = itens.filter(contrato__empresa__id= empresa)

    return itens

def filtro_registro_lotacoes(request):
    pass