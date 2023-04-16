from django.contrib import admin
from .models import *

# Register your models here.


# class DepartamentoAdmin(admin.ModelAdmin):

#     list_display = ('nome', 'hierarquia', 'tipo', 'municipio')
#     search_fields = ['nome', 'hierarquia', 'tipo', 'municipio']

# admin.site.register(Departamento, DepartamentoAdmin)


class EscolaAdmin(admin.ModelAdmin):

    list_display = ('cod_inep', 'cod_turmalina', 'nome_escola')
    search_fields = ['cod_inep', 'cod_turmalina', 'nome_escola']

admin.site.register(Escola, EscolaAdmin)


class EnderecoAdmin(admin.ModelAdmin):

    list_display = ('escola', 'municipio', 'regiao', 'zoneamento', 'tipo_localizacao')
    search_fields = ['escola', 'municipio', 'regiao', 'zoneamento', 'tipo_localizacao']

admin.site.register(Endereco, EnderecoAdmin)


class ContatoAdmin(admin.ModelAdmin):

    list_display = ('endereco', 'tipo_contato', 'contato')
    search_fields = ['endereco', 'tipo_contato', 'contato']

admin.site.register(Contato, ContatoAdmin)


class Organizacao_escolarAdmin(admin.ModelAdmin):

    list_display = ('escola', 'site', 'espacos_entorno', 'pedagogia_atualizada')
    search_fields = ['escola', 'site', 'espacos_entorno', 'pedagogia_atualizada']

admin.site.register(Organizacao_escolar, Organizacao_escolarAdmin)


# class TurmasAdmin(admin.ModelAdmin):

#     list_display = ('escola', 'nome', 'turno', 'etapa', 'total_alunos')
#     search_fields = ['escola', 'nome', 'turno', 'etapa', 'total_alunos']

# admin.site.register(Turmas, TurmasAdmin)


class DisciplinasAdmin(admin.ModelAdmin):

    list_display = ['nome']
    search_fields = ['nome']

admin.site.register(Disciplinas, DisciplinasAdmin)


class ContratoAdmin(admin.ModelAdmin):

    list_display = ['numero_contrato']
    search_fields = ['numero_contrato']

admin.site.register(Contrato_contrato, ContratoAdmin)


class Contrato_aditivoAdmin(admin.ModelAdmin):

    list_display = ['contrato']
    search_fields = ['contrato']

admin.site.register(Contrato_aditivo, Contrato_aditivoAdmin)


class Contrato_itemAdmin(admin.ModelAdmin):

    list_display = ['contrato']
    search_fields = ['contrato']

admin.site.register(Contrato_item, Contrato_itemAdmin)
