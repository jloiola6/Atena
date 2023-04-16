from django.db import models
from django.forms import IntegerField

from aplicacoes.administracao.models import Escola
from aplicacoes.lotacao.models import Servidor


# Create your models here.
class Consorcio(models.Model):
    nome_consorcio = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    status = models.IntegerField()


class Coex(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    cnpj = models.CharField(max_length=18)
    nome_empresarial = models.CharField(max_length=150, null=True)
    data_inativo = models.DateField(null=True)
    motivo = models.CharField(max_length=300, blank=True, null=True)
    user_inativou = models.CharField(max_length=30, blank=True, null=True)
    status = models.IntegerField()


class Arquivo(models.Model):
    coex = models.ForeignKey(Coex, on_delete= models.CASCADE)
    arquivo = models.FileField()
    categoria = models.CharField(max_length=100)
    descricao = models.CharField(max_length=250)
    status = models.IntegerField()

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)

    def descricao_simples(self):
        if len(self.descricao) > 70:
            return self.descricao[0:70] + '...'
        return self.descricao


class Escola_consorcio(models.Model):
    consorcio = models.ForeignKey(Consorcio, on_delete= models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    status = models.IntegerField()


class Equipe_comite(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE, null= True)
    coex = models.ForeignKey(Coex, on_delete= models.CASCADE, null= True)
    consorcio = models.ForeignKey(Consorcio, on_delete= models.CASCADE, null= True)
    cargo = models.CharField(max_length=50)
    nome = models.CharField(max_length=150, null=True)


class Arquivo_consorcio(models.Model):
    consorcio = models.ForeignKey(Consorcio, on_delete= models.CASCADE)
    arquivo = models.FileField()
    categoria = models.CharField(max_length=100)
    descricao = models.CharField(max_length=250)
    status = models.IntegerField()

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)

    def descricao_simples(self):
        if len(self.descricao) > 70:
            return self.descricao[0:70] + '...'
        return self.descricao
