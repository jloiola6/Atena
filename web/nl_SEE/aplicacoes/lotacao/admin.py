from django.contrib import admin
from .models import *

# Register your models here.


class FuncaoAdmin(admin.ModelAdmin):

    list_display = ('nome', 'tipo')
    search_fields = ['nome', 'tipo']

admin.site.register(Funcao, FuncaoAdmin)