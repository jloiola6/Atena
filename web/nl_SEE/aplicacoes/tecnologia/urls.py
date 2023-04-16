from django.contrib import admin
from django.urls import path
from aplicacoes.tecnologia.views.vagas import *
from aplicacoes.tecnologia.views.main import *
from aplicacoes.tecnologia.views.link import *
from aplicacoes.tecnologia.views.contrato import *
from aplicacoes.core.views_gerais.contratos import *
from aplicacoes.tecnologia.views.chamados import *
from aplicacoes.tecnologia.views.educacao_conectada import *
from aplicacoes.tecnologia.views.auxilio_notebook import *


app_name = 'tecnologia'
urlpatterns = [
    path('', index, name='index'),

    #Link
    path('link_perfil', link_perfil, name='link-perfil'),
    path('links_tabela', links_tabela, name='links-tabela'),
    path('link_formulario', link_formulario, name='link-formulario'),
    path('inativar-link', inativar_link, name='inativar-link'),


    #Contrato
    path('contratos', contratos, name='contratos'),
    path('contrato-perfil', contrato_perfil, name='contrato-perfil'),
    path('item-perfil', item_perfil, name='item-perfil'),
    path('contrato-aditivo-formulario', contrato_aditivo_formulario, name='contrato-aditivo-formulario'),
    path('gestores-formulario', gestores_formulario, name='gestores-formulario'),
    path('fiscais-formulario', fiscais_formulario, name='fiscais-formulario'),
    path('responsavel-formulario', responsavel_formulario, name='responsavel-formulario'),
    path('contrato-aditivo-perfil', contrato_aditivo_perfil, name='contrato-aditivo-perfil'),
    path('fonte-formulario', fonte_formulario, name='fonte-formulario'),
    path('documento-formulario', documento_formulario, name='documento-formulario'),
    path('fonte-perfil', fonte_perfil, name='fonte-perfil'),
    path('empenho-formulario', empenho_formulario, name='empenho-formulario'),
    path('pre-empenho-formulario', pre_empenho_formulario, name='pre-empenho-formulario'),

    #Central de vagas
    path('central-de-vagas', central_vagas, name='vagas'),

    #Chamados
    path('chamados', chamados, name='chamados'),
    path('chamados-tecnico', chamados_tecnico, name='chamados-tecnico'),
    path('chamados-help', chamados_help, name='chamados-help'),
    path('chamados-adm', chamados_adm, name='chamados-adm'),
    path('chamado-formulario', chamado_formulario, name='chamado-formulario'),
    path('chamado-perfil', chamado_perfil, name='chamado-perfil'),
    path('chamados-adicionar', chamados_adicionar, name='chamados-adicionar'),

    #Educação conectada
    path('educacao-conectada', educacao_conectada, name='educacao-conectada'),
    path('tablets', tablets, name='tablets'),
    path('escolas', escolas, name='escolas'),
    path('escola-perfil/<int:id_escola>', escola_perfil, name='escola-perfil'),
    path('escola-anexos/<int:id_escola>', escola_anexos, name='escola-anexos'),
    path('turma-perfil/<int:id_turma>', turma_perfil, name='turma-perfil'),
    path('aluno-perfil/<int:id_aluno_turma>', aluno_perfil, name='aluno-perfil'),
    path('tablet-formulario/<int:id_turma>', tablet_formulario, name='tablet-formulario'),

    #Auxílio Notebook
    path('auxilio-notebook', main, name='auxilio-notebook'),
    path('tabela-auxilio', auxilio_notebook, name='tabela-auxilio'),
    path('tabela-notas', notas_notebook, name='tabela-notas'),
    path('devolucao-notebook', devolucao_notebook, name='devolucao-notebook'),
    path('servidor-perfil', servidor_perfil, name="servidor-perfil")
]