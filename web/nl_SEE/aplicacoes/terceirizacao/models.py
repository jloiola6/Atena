from django.db import models

from aplicacoes.administracao.models import *
from aplicacoes.lotacao.models import Servidor

# Create your models here.

class Contrato_lotacao(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    item = models.ForeignKey(Contrato_item, on_delete= models.CASCADE)
    posto = models.ForeignKey(Contrato_posto_vigilante, on_delete= models.CASCADE, null=True)
    endereco = models.ForeignKey(Endereco, on_delete= models.CASCADE, null= True)
    unidade_administrativa = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null= True)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.CharField(max_length=6, blank=True, null=True)
    motivo = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField()


class Servidor_ocorrencia_funcional(models.Model):
    contrato = models.ForeignKey(Contrato_lotacao, on_delete= models.CASCADE, null= True)
    tipo_ocorrencia = models.CharField(max_length=50, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    documento = models.CharField(max_length=200, null= True)
    substituto = models.CharField(max_length=80, null = True)
    status = models.IntegerField()