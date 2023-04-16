from itertools import chain

from .models import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import *
from aplicacoes.terceirizacao.models import Contrato_lotacao

import re


# def filtro_unidades(request, enderecos, municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes):
def filtro_unidades(request, user):
    escola_coex = Coex.objects.values_list('escola__id', flat = True)
    enderecos = Endereco.objects.filter(tipo='S', escola__id__in = escola_coex).values('escola__id','escola__cod_inep', 'escola__nome_escola', 'municipio', 'regiao', 'tipo_localizacao').order_by('escola__nome_escola')

    login = ('ana.marina', 'erick.nascimento', 'fabio.santos', 'franklin.farias', 'joaopedro.passos', 'joaoteixeira.netto', 'josecarlos.souza', 'tharlis.seixas')
    if user not in login:
        enderecos = enderecos.exclude(id__in = [669, 723, 724, 722])

    inep = request.GET.get('cod_inep')
    nome = request.GET.get('nome_unidade')
    cnpj = request.GET.get('cnpj')
    comite = request.GET.get('comite')
    situacao = request.GET.get('situacao')


    #Filtro pelo INEP
    if inep != None and inep != '':
        enderecos = enderecos.filter(escola__cod_inep= int(inep))
    
    #Filtro pelo Nome
    if nome != None and nome != '':
        enderecos = enderecos.filter(escola__nome_escola__icontains= nome)
    
    #Filtro pelo cnpj
    if cnpj != None and cnpj != '':
        escola_id = Coex.objects.filter(cnpj= cnpj).values_list('escola__id', flat= True)
        enderecos = enderecos.filter(id__in= escola_id)

    if comite != None and comite != '':
        escola_id = Coex.objects.filter(nome_empresarial= comite).values_list('escola__id', flat= True)
        enderecos = enderecos.filter(id__in= escola_id)

    if situacao != None and situacao != '':
        escola_id = Coex.objects.filter(status= situacao).values_list('escola__id', flat= True)
        enderecos = enderecos.filter(id__in= escola_id)

    return enderecos
