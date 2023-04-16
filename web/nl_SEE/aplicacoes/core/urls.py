from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from aplicacoes.core.views import *
# from aplicacoes.core.views_gerais.servidor import *


app_name = 'core'
urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout, name='logout'),
    path('manutencao/', manutencao, name='manutencao'),
    path('meu-perfil', perfil, name='perfil'),
    path('editar-dados', editar_dados, name='editar-dados'),
    path('servidor-endereco', servidor_endereco, name='servidor-endereco'),
    path('servidor-contatos', servidor_contatos, name='servidor-contatos'),
    path('servidor-banco', servidor_banco, name='servidor-banco'),
    path('servidor-documento', documento_formulario, name='servidor-documento'),
    path('historico-chamados', historico_chamados, name='historico-chamados'),
    path('servidor-galeria',servidor_galeria, name='servidor-galeria'),

    # Dados cadastrais
    path('dados-cadastrais', dados_cadastrais, name='dados-cadastrais'),
    path('cadastro-escolaridade', cadastro_escolaridade, name='cadastro-escolaridade'),

    #Saiba Mais
    path('saiba-mais', saiba_mais, name='saiba-mais'),
    path('suporte', suporte, name='suporte'),
]