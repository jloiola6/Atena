from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from aplicacoes.coex.views.main import *

from aplicacoes.coex.views.comite import *
from aplicacoes.coex.views.consorcio import *


app_name = 'coex'
urlpatterns = [
    path('', index, name='index'),

#Comitê
    path('comite', unidades_educacionais, name='comite'),
    path('comite-perfil', comite_perfil, name='comite-perfil'),
    path('equipe-formulario', equipe_formulario, name='equipe-formulario'),
    path('documento-formulario', documento_formulario, name='documento-formulario'),
    path('comite-formulario', comite_formulario, name='comite-formulario'),
    path('gerenciador-documentos', gerenciador_documentos, name='gerenciador-documentos'),
    path('contato-formulario', editar_contatos, name='contato-formulario'),
    path('endereco-formulario', editar_endereco, name='endereco-formulario'),
    path('servidor-perfil', servidor_perfil, name='servidor-perfil'),
    path('servidor-base', servidor_base, name='servidor-base'),
    path('servidor-endereco', servidor_endereco, name='servidor-endereco'),
    path('servidor-contato', servidor_contato, name='servidor-contato'),
    path('inativar-comite', inativar_comite, name='inativar-comite'),


#Corsórcio
    path('consorcio', consorcio, name='consorcio'),
    path('consorcio-formulario', consorcio_formulario, name='consorcio-formulario'),
    path('consorcio-perfil', consorcio_perfil, name='consorcio-perfil'),
    path('vincular-escola', vincular_escola, name='vincular-escola'),
    path('desvincular-escola', desvincular_escola, name='desvincular-escola'),
    path('documento-consorcio', formulario_documento_consorcio, name='documento-consorcio'),
    path('gerenciador-documentos-consorcio', gerenciador_documentos_consorcio, name='gerenciador-documentos-consorcio'),

]