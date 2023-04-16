from django.contrib import admin
from django.urls import path

from aplicacoes.dinem.views import *

# Historico Alunos
from aplicacoes.dinem.relatorios.relatorio_aluno_integral_2022 import *
from aplicacoes.dinem.relatorios.relatorio_aluno_parcial_2022 import *
from aplicacoes.dinem.relatorios.relatorio_aluno_tecnico_2022 import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.relatorio_aluno_integral_2serie import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.relatorio_aluno_parcial_2serie import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.relatorio_aluno_profissionalizante import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_1_serie.relatorio_aluno_integral_1serie import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_1_serie.relatorio_aluno_parcial_1serie import *

# Relatorio Turmas
from aplicacoes.dinem.relatorios.relatorio_turma import *
from aplicacoes.dinem.relatorios.relatorio_aluno import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_1_serie.turma_integral_1serie import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_1_serie.turma_parcial_1serie import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_1_serie.turma_profissionalizante_1serie_2022 import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.turma_integral_2serie_2022_novo import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.turma_parcial_2serie_2022_novo import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_2_serie.turma_profissionalizante_2serie_2022 import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_3_serie.turma_integral_terceiro_2022_novo import *
from aplicacoes.dinem.relatorios.ano_letivo_2022.turma_3_serie.turma_parcial_terceiro_2022_novo import *


app_name = 'dinem'
urlpatterns = [
    path('', index, name='index'),
    path('unidade-anexos/<int:inep>', unidade_anexos, name='unidade-anexos'),
    path('unidade_perfil', unidade_perfil, name='unidade-perfil'),
    path('unidade-turmas/<int:id_endereco>', unidade_turmas, name='unidade-turmas'),
    path('turma_perfil/<int:id_turma>', turma_perfil, name='turma-perfil'),
    path('relatorio_turma', relatorio_turma, name='relatorio-turma'),
    path('relatorio_aluno/<int:id_aluno_turma>', relatorio_aluno, name='relatorio-aluno'),
    path('aluno_perfil/<int:id_aluno_turma>', aluno_perfil, name='aluno-perfil'),
    path('aluno_boletim/<int:id_aluno_turma>/<str:etapa>', aluno_boletim, name='aluno-boletim'),
    path('aluno_formulario/<int:id_aluno_turma>', aluno_formulario, name='aluno-formulario'),

    # Relatorios alunos
    path ('dados_aluno_integral/<int:id_aluno_turma>', dados_aluno_integral, name='dados_aluno_integral'),
    path ('dados_aluno_parcial/<int:id_aluno_turma>', dados_aluno_parcial, name='dados_aluno_parcial'),
    path ('dados_aluno_tecnico/<int:id_aluno_turma>', dados_aluno_tecnico, name='dados_aluno_tecnico'),
    path ('dados_aluno_integral_2serie/<int:id_aluno_turma>', dados_aluno_integral_2serie, name='dados_aluno_integral_2serie'),
    path ('dados_aluno_parcial_2serie/<int:id_aluno_turma>', dados_aluno_parcial_2serie, name='dados_aluno_parcial_2serie'),
    path ('dados_aluno_tecnico_2serie/<int:id_aluno_turma>', dados_aluno_tecnico_2serie, name='dados_aluno_tecnico_2serie'),
    path ('dados_aluno_integral_1serie/<int:id_aluno_turma>', dados_aluno_integral_1serie, name='dados_aluno_integral_1serie'),
    path ('dados_aluno_parcial_1serie/<int:id_aluno_turma>', dados_aluno_parcial_1serie, name='dados_aluno_parcial_1serie'),

    # Relatorios turmas
    path ('turma_parcial_terceiro', turma_parcial_terceiro, name='turma_parcial_terceiro'),
    path ('turma_integral_terceiro', turma_integral_terceiro, name='turma_integral_terceiro'),
    path ('turma_integral_2serie', turma_integral_2serie, name='turma_integral_2serie'),
    path ('turma_parcial_2serie', turma_parcial_2serie, name='turma_parcial_2serie'),
    path ('turma_profissionalizante_2serie', turma_profissionalizante_2serie, name='turma_profissionalizante_2serie'),
    path ('turma_integral_1serie', turma_integral_1serie, name='turma_integral_1serie'),
    path ('turma_parcial_1serie', turma_parcial_1serie, name='turma_parcial_1serie'),
    path ('turma_profissionalizante_1serie', turma_profissionalizante_1serie, name='turma_profissionalizante_1serie'),
]