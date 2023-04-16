from django.contrib import admin
from django.urls import path

from aplicacoes.usuario.views import *


app_name = 'usuario'
urlpatterns = [
    path('', index, name='index'),
    path('pre_cadastrados', pre_cadastrados, name='pre-cadastrados'),
    path('login', login, name='login'),
    path('usuario_formulario', usuario_formulario, name='usuario-formulario'),
    path('usuario_perfil', usuario_perfil, name='usuario-perfil'),
    path('usuario_permissoes', usuario_permissoes, name='usuario-permissoes'),
    path('editar_permissao', editar_permissao, name='editar-permissao'),
    path('exluir_permissao', exluir_permissao, name='excluir-permissao'),

]