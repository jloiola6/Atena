from django.urls import path

# from aplicacoes.atena.views import *
from aplicacoes.atena.views.simaed import *
from aplicacoes.atena.views.testes import *

app_name = 'atena'
urlpatterns = [
    path('', index, name='index'),
    path('teste-escolas-etapas', teste_escolas_etapas, name='teste-escolas-etapas'),
    path('teste', teste, name='teste'),
    path('aditivo', aditivo, name='aditivo'),
    path('front', front, name='front'),
    path('testes', testes, name='testes'),

    # SIMAED
    path('simaed', simaed, name='simaed'),
    path('importacao/<int:id_importacao>', importacao, name='importacao'),
    path('escola/<int:id_importacao>/<int:inep>', escola, name='escola'),
]