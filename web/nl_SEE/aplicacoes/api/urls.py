from django.urls import path

from aplicacoes.api.views import *

app_name = 'api'
urlpatterns = [
    path('escolas/', dados_escola, name='index'),
    path('escola/turma/', turma_escola, name='turma'),
    path('aluno/turma/', aluno_turma, name='aluno'),
    path('servidor/', servidor, name='servidor'),

    # Educação Conectada
    path('ec/aluno/turma/', aluno_turma_EC, name='ec-aluno')
]