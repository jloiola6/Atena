from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from aplicacoes.contas.views import *


app_name = 'contas'
urlpatterns = [
    path('', index, name='index'),

]