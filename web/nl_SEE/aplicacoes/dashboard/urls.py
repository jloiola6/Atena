from django.contrib import admin
from django.urls import path

from aplicacoes.dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    path('', index, name='index'),
] 
