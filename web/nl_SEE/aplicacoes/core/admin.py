from django.contrib import admin
from .models import *

# Register your models here.

class HistoricoAdmin(admin.ModelAdmin):

    list_display = ('log', 'tabela', 'objeto', 'data', 'acao')
    search_fields = ['log', 'tabela', 'objeto', 'data', 'acao']

admin.site.register(Historico, HistoricoAdmin)