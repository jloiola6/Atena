from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from aplicacoes.fundiaria.views import *


app_name = 'fundiaria'
urlpatterns = [
    path('', index, name='index'),
    path('unidades-educacionais', unidades_educacionais, name='unidades-educacionais'),
    path('unidades-adm', unidades_adm, name='unidades-adm'),
    path('fundiaria-perfil', fundiaria_perfil, name='fundiaria-perfil'),
    # path('fundiaria-perfil-adm', fundiaria_perfil_adm, name='fundiaria-perfil-adm'),


#infraestrutura.py
    path('infraestrutura_formulario', infraestrutura_formulario, name='infraestrutura-formulario'),
    path('documento-formulario', documento_formulario, name='documento-formulario'),
    path('imagem-formulario', imagem_formulario, name='imagem-formulario'),
    path('extincao-formulario', extincao_formulario, name='extincao-formulario'),
    path('galeria-imagem', galeria_imagem, name='galeria-imagem'),
    path('gerenciador-documentos', gerenciador_documentos, name='gerenciador-documentos'),
    path('editar-dados', editar_dados, name='editar_dados'),
    path('editar-endereco', editar_endereco, name='editar_endereco'),
    path('editar-contatos', editar_contatos, name='editar-contatos'),
] 