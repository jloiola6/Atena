from django.contrib import admin
from django.urls import path

from aplicacoes.terceirizacao.views.main import index
from aplicacoes.terceirizacao.views.central_vagas import *
from aplicacoes.core.views_gerais.contratos import *
from aplicacoes.terceirizacao.views.contrato import *
from aplicacoes.terceirizacao.views.lotacao import *
from aplicacoes.terceirizacao.views.servidor import *
from aplicacoes.terceirizacao.views.registros import *

app_name = 'terceirizacao'

urlpatterns = [
    path('', index, name='index'),

    #Servidor
    path('servidores', servidores, name='servidores'),
    path('servidor-formulario', servidor_formulario, name='servidor-formulario'),
    path('servidor-consulta', servidor_consulta, name='servidor-consulta'),
    path('servidor-perfil', servidor_perfil, name='servidor-perfil'),
    path('servidores_lotados', servidores_lotados, name='servidores-lotados'),
    path('servidor-contatos', servidor_contatos, name='servidor-contatos'),
    path('servidor_contrato_perfil', servidor_contrato_perfil, name='servidor-contrato-perfil'),
    path('servidor-banco', servidor_banco, name='servidor-banco'),
    path('servidor-endereco', servidor_endereco, name='servidor-endereco'),
    path('servidor-base', servidor_base, name='servidor-base'),
    path('cadastro-escolaridade', escolaridade, name='cadastro-escolaridade'),

    #Contrato
    path('contratos', contratos, name='contratos'),
    path('contrato-formulario', contrato_formulario, name='contrato-formulario'),
    path('contrato-perfil', contrato_perfil, name='contrato-perfil'),
    path('item-perfil', item_perfil, name='item-perfil'),
    path('contrato-aditivo-formulario', contrato_aditivo_formulario, name='contrato-aditivo-formulario'),
    path('gestores-formulario', gestores_formulario, name='gestores-formulario'),
    path('fiscais-formulario', fiscais_formulario, name='fiscais-formulario'),
    path('responsavel-formulario', responsavel_formulario, name='responsavel-formulario'),
    path('contrato-aditivo-perfil', contrato_aditivo_perfil, name='contrato-aditivo-perfil'),
    path('fonte-formulario', fonte_formulario, name='fonte-formulario'),
    path('finalizar-contrato', finalizar_contrato, name='finalizar-contrato'),
    path('postos-formulario', postos_formulario, name='postos-formulario'),
    path('ocorrencia-formulario-terceirizacao', ocorrencia_formulario_terceirizacao, name='ocorrencia-formulario-terceirizacao'),
    path('documento-formulario', documento_formulario, name='documento-formulario'),
    path('fonte-perfil', fonte_perfil, name='fonte-perfil'),
    path('empenho-formulario', empenho_formulario, name='empenho-formulario'),

    # #Lotação
    path('lotacoes', lotacoes, name='lotacoes'),
    path('lotacao-perfil', lotacao_perfil, name='lotacao-perfil'),

#   # #Central de Vagas
    path('central-de-vagas', central_vagas, name='vagas'),

    # Registro
    path('registro', registro_lotacoes, name='registro'),
]
