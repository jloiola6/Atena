from django.contrib import admin
from django.urls import path

from aplicacoes.administracao.views.main import *
from aplicacoes.administracao.views.unidade_educacional import *
from aplicacoes.administracao.views.unidade_administrativa import *
from aplicacoes.administracao.views.contratos import *
from aplicacoes.core.views_gerais.contratos import *
from aplicacoes.administracao.views.organograma import *
from aplicacoes.administracao.views.infraestrutura import *
from aplicacoes.administracao.views.inventario import *
from aplicacoes.administracao.views.servidores import *
from aplicacoes.administracao.views.matrizes import *
from aplicacoes.administracao.views.alunos import *

app_name = 'administracao'
urlpatterns = [
    #main.py
    path('', index, name='index'),

    # UNIDADES EDUCACIONAIS
    path('unidades', unidades_educacionais, name='unidades_educacionais'),
    path('unidade-anexos/<int:inep>', unidade_anexos, name='unidade-anexos'),
    path('unidade_perfil', unidade_perfil, name='unidade-perfil'),
    path('unidade_formulario', unidade_formulario, name='unidade-formulario'),
    path('editar_dados', editar_dados, name='editar-dados'),
    path('editar_endereco', editar_endereco, name='editar-endereco'),
    path('unidade_contatos', unidade_contatos, name='unidade-contatos'),
    path('unidade_historico', unidade_historico, name='unidade-historico'),
    path('turma_formulario', turma_formulario, name='turma-formulario'),
    path('grade_formulario', grade_formulario, name='grade-formulario'),
    path('organizacao_formulario', organizacao_formulario, name='organizacao-formulario'),
    path('organizacao_perfil', organizacao_perfil, name='organizacao-perfil'),
    # path('turma_perfil', turma_perfil, name='turma-perfil'),
    path('turma-perfil/<int:id_turma>', turma_perfil, name='turma-perfil'),
    path('deletar_grade', deletar_grade, name='deletar-grade'),
    path('unidade_anexo', unidade_anexo, name='unidade-anexo'),
    path('aluno_formulario', aluno_formulario, name='aluno-formulario'),
    # path('aluno_perfil', aluno_perfil, name='aluno-perfil'),
    path('vincular-professor-formulario', vincular_professor_formulario, name='vincular-professor-formulario'),
    path('unidade-consulta', unidade_consulta, name='unidade-consulta'),
    path('unidade-matriz/<int:id_endereco>', unidade_matriz, name='unidade-matriz'),
    path('unidade-ouvidoria', ouvidoria_unidade, name='unidade-ouvidoria'),

    #unidades_administrativas.py
    path('unidades_administrativas', unidades_administrativas, name='unidades-administrativas'),
    path('servidores_lotados', servidores_lotados, name='servidores-lotados'),
    path('editar-endereco-adm', editar_endereco_adm, name='editar-endereco-adm'),

    # contratos.py
    path('contratos', contratos, name='contratos'),
    path('contrato-formulario', contrato_formulario, name='contrato-formulario'),
    # path('contrato-limpeza-formulario', contrato_limpeza_formulario, name='contrato-limpeza-formulario'),
    # path('contrato-produto-formulario', contrato_produto_formulario, name='contrato-produto-formulario'),
    # path('contrato-servico-formulario', contrato_servico_formulario, name='contrato-servico-formulario'),
    # path('contrato-trabalho-formulario', contrato_trabalho_formulario, name='contrato-trabalho-formulario'),
    # path('contrato-vigilante-formulario', contrato_vigilante_formulario, name='contrato-vigilante-formulario'),
    path('empresa-formulario', empresa_formulario, name='empresa-formulario'),
    path('contrato-aditivo-formulario', contrato_aditivo_formulario, name='contrato-aditivo-formulario'),
    path('gestores-formulario', gestores_formulario, name='gestores-formulario'),
    path('fiscais-formulario', fiscais_formulario, name='fiscais-formulario'),
    path('contrato-perfil', contrato_perfil, name='contrato-perfil'),
    path('item-perfil', item_perfil, name='item-perfil'),
    path('contrato-aditivo-perfil', contrato_aditivo_perfil, name='contrato-aditivo-perfil'),
    path('responsavel-formulario', responsavel_formulario, name='responsavel-formulario'),
    path('fonte-formulario', fonte_formulario, name='fonte-formulario'),
    path('postos-formulario', postos_formulario, name='postos-formulario'),
    # path('vigilantes-formulario', vigilantes_formulario, name='vigilantes-formulario'),
    path('documento-formulario', documento_formulario, name='documento-formulario'),
    path('fonte-perfil', fonte_perfil, name='fonte-perfil'),
    path('empenho-formulario', empenho_formulario, name='empenho-formulario'),


    #infraestrutura.py
    path('infraestrutura_formulario', infraestrutura_formulario, name='infraestrutura-formulario'),
    path('infraestrutura-perfil/<int:id_endereco>', infraestrutura_perfil, name='infraestrutura-perfil'),
    path('dependencia-formulario/<int:id_endereco>', dependencia_formulario, name='dependencia-formulario'),
    # path('dependencia', dependencia_perfil, name='dependencia'),

    # INVENTÁRIO
    path('controle-inventario', controle_inventario, name='controle-inventario'),
    # path('inventario', inventario_perfil, name='inventario-perfil'),
    # path('inventario_formulario', inventario_formulario, name='inventario-formulario'),
    path('item-formulario/<int:id_dependencia>/<int:id_tipo>', item_formulario, name='item-formulario'),
    path('inventario-perfil/<int:id_infraestrutura>', inventario_perfil, name='inventario-perfil'),
    # path('inventario_cadastro', inventario_perfil, name='inventario'),

    # Servidores.py
    # path('servidores', servidores, name='servidores'),
    path('professor_perfil', professor_perfil, name='professor-perfil'),

    #organograma.py VAI VIRAR UNIDADE ADMINISTRATIVA
    path('organograma', organograma, name='organograma'),
    path('diretoria', diretoria, name='diretoria'),
    path('departamento', departamento, name='departamento'),
    path('divisao', divisao, name='divisao'),
    path('nucleo', nucleo, name='nucleo'),
    path('centro', centro, name='centro'),
    # path('organograma_formulario', organograma_formulario, name='organograma-formulario'),
    path('departamento_formulario', departamento_formulario, name='departamento-formulario'),
    path('divisao_formulario', divisao_formulario, name='divisao-formulario'),
    path('nucleo_formulario', nucleo_formulario, name='nucleo-formulario'),
    path('polo_centro_formulario', polo_centro_formulario, name='polo-centro-formulario'),

    # MATRIZES
    path('matrizes', matrizes, name='matrizes'),
    path('matriz/<int:id_matriz>', matriz, name='matriz'),
    path('matriz-formulario', matriz_formulario, name='matriz-formulario'),

    # ALUNOS
    path('alunos', alunos, name='alunos'),
    path('aluno-perfil/<int:id_aluno>', aluno_perfil, name='aluno-perfil'),
]
