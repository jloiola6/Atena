from django.contrib import admin
from .models import *

# Register your models here.


class UsuariosAdmin(admin.ModelAdmin):

    list_display = ('nome', 'login', 'cpf', 'email')
    search_fields = ['nome', 'login', 'cpf', 'email']

admin.site.register(Usuarios, UsuariosAdmin)


class LogsAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'entrada', 'saida')
    search_fields = ['usuario', 'entrada', 'saida']

admin.site.register(Logs, LogsAdmin)


class PermussoesAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'servico', 'consultar', 'editar', 'imprimir')
    search_fields = ['usuario', 'servico', 'consultar', 'editar', 'imprimir']

admin.site.register(Permissao, PermussoesAdmin)