# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from aplicacoes.administracao.models import Endereco, Unidade_administrativa, Escola
from aplicacoes.lotacao.models import Servidor, Servidor_lotacao
from aplicacoes.usuario.models import Logs, Usuarios
from aplicacoes.terceirizacao.models import Contrato_lotacao
# #Models de Histórico
class Historico(models.Model):
    log = models.ForeignKey(Logs, on_delete= models.CASCADE)
    tabela = models.CharField(max_length=100)
    objeto = models.IntegerField()
    data = models.CharField(max_length=20)
    acao = models.CharField(max_length=1, choices=(('A', 'Adição'), ('E','Edição')))
    modificacao = models.CharField(max_length= 1000, null= True)

    def __str__(self) -> str:
        return str(self.log)


class Confirmacao_lotacao(models.Model):
    lotacao = models.ForeignKey(Servidor_lotacao, on_delete=models.CASCADE, null = True)
    terceirizado = models.ForeignKey(Contrato_lotacao, on_delete=models.CASCADE, null = True)
    alteracao_lotacao= models.IntegerField()
    unidade_escolar = models.ForeignKey(Escola, on_delete= models.CASCADE, null= True)
    unidade_adm = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null= True)
    data_atualizacao= models.DateTimeField(null= True)