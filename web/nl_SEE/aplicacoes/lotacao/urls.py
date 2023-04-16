from aplicacoes.lotacao.views.contrato import *
from aplicacoes.lotacao.views.lotacao import *
from aplicacoes.lotacao.views.main import *
from aplicacoes.lotacao.views.servidor import *
from aplicacoes.lotacao.views.vdp import *
from aplicacoes.lotacao.views.folha import *
from aplicacoes.lotacao.views.registro import *
from aplicacoes.lotacao.views.qualidade import *
from aplicacoes.lotacao.views.autorizacao import *
from aplicacoes.lotacao.views.teste import *
from aplicacoes.lotacao.views.tecnico import *
# from aplicacoes.core.views_gerais.servidor import *
from django.contrib import admin
from django.urls import path

app_name = 'lotacao'

urlpatterns = [
    path('', index, name='index'),

    #Servidor
    path('servidores', servidores, name='servidores'),
    path('servidor-formulario', servidor_formulario, name='servidor-formulario'),
    path('servidor-perfil', servidor_perfil, name='servidor-perfil'),
    path('servidor-contatos', servidor_contatos, name='servidor-contatos'),
    path('servidor-banco', servidor_banco, name='servidor-banco'),
    path('servidor-endereco', servidor_endereco, name='servidor-endereco'),
    path('servidor-base', servidor_base, name='servidor-base'),
    path('servidor-consulta', servidor_consulta, name='servidor-consulta'),
    path('servidor-documento', documento_formulario, name='servidor-documento'),
    path('cadastro-escolaridade', escolaridade, name='cadastro-escolaridade'),
    path('gerenciador-documento', gerenciador_documento, name='gerenciador-documento'),

    #Contrato
    path('contratos', contratos, name='contratos'),
    path('contratos-filtros', contratos_filtros, name='contratos-filtros'),
    path('contrato-formulario', contrato_formulario, name='contrato-formulario'),
    # path('contrato-perfil', contrato_perfil, name='contrato-perfil'),
    path('contrato-perfil/<int:id_contrato>', contrato_perfil, name='contrato-perfil'),
    path('ocorrencia-formulario', ocorrencia_formulario, name='ocorrencia-formulario'),
    path('cargo-formulario', cargo_formulario, name='cargo-formulario'),
    path('complemento-formulario', complemento_formulario, name='complemento-formulario'),
    path('gratificacao-formulario', gratificacao_formulario, name='gratificacao-formulario'),
    path('finalizar-contrato', finalizar_contrato, name='finalizar-contrato'),
    path('aditivo-formulario', aditivo_formulario, name='aditivo-formulario'),
    path('vdp-formulario', vdp_formulario, name='vdp-formulario'),


    #Lotação
    path('lotacoes', lotacoes, name='lotacoes'),
    path('lotacao-formulario', lotacao_formulario, name='lotacao-formulario'),
    path('subconta-formulario', subconta_formulario, name='subconta-formulario'),
    path('turma-formulario', turma_formulario, name='turma-formulario'),
    path('aluno-formulario', aluno_formulario, name='aluno-formulario'),
    path('lotacoes-filtros', lotacoes_filtros, name='lotacoes-filtros'),


    #VDP
    path('vdp-tabela', vdp_tabela, name='vdp-tabela'),
    path('anos-vdp', anos_vdp, name='anos-vdp'),


    # Registro
    path('registro', registro, name='registro'),
    path('registro-lotacoes', registro_lotacoes, name='registro-lotacoes'),
    path('registro-contratos', registro_contratos, name='registro-contratos'),


    #Folha de Pagamento
    path('folha-pagamento', folha_pagamento, name='folha-pagamento'),

    # Qualidade de Vida
    path('qualidade', qualidade, name='qualidade'),
    path('aniversarios', aniversarios, name='aniversarios'),
    path('agendamentos', agendamentos, name='agendamentos'),
    path('formulario-espera', formulario_espera, name='formulario-espera'),
    path('lista-espera', lista_espera, name='lista-espera'),
    path('marcar-consulta/<int:id_agendamento>', marcar_consulta, name='marcar-consulta'),
    path('relatorios', relatorio, name='relatorios'),
    path('perfil-agendamento', perfil_agendamento, name='perfil-agendamento'),
    path('agendamento-formulario/<int:id_atendimento>', agendamento_formulario, name='agendamento-formulario'),
    path('atendimento-formulario', atendimento_formulario, name='atendimento-formulario'),
    path('atendimento/<int:id_atendimento>', atendimento, name='atendimento'),


    #Autorização de Lotação
    path('autorizacao-lotacao', autorizacao_lotacao, name='autorizacao-lotacao'),

    #Técnico
    path('tecnico', tecnico, name='tecnico'),
    path('autorizacao-verbas', autorizacao_verbas, name='autorizacao-verbas')
]
