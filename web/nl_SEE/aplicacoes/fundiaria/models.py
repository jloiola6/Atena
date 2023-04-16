from aplicacoes.administracao.models import Endereco, Unidade_administrativa
from django.db import models


class Fundiaria(models.Model):
    endereco = models.ForeignKey(Endereco, on_delete= models.CASCADE, null=True)
    unidade_adm = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null=True)
    regularizacao = models.CharField(max_length=50)
    area_imovel = models.CharField(max_length=20)
    area_utilizada = models.CharField(max_length=20)
    area_construida = models.CharField(max_length=20)
    perimetro = models.CharField(max_length=20)
    ppi = models.CharField(max_length=100)
    bci = models.CharField(max_length=100)
    decreto_criacao = models.CharField(max_length=100)
    portaria_autorizacao = models.CharField(max_length=100)
    conta_agua = models.CharField(max_length=100)
    matricula_imoveis = models.CharField(max_length=100)
    forma_ocupacao = models.CharField(max_length=100)
    convenio = models.CharField(max_length=100, null= True, blank= True)
    situacao = models.CharField(max_length=100)


class Extincao(models.Model):
    fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
    data_extincao = models.DateField(null= True, blank= True)
    data_paralizacao = models.DateField(null= True, blank= True)
    escola_guardia = models.CharField(max_length=100)
    decreto_extincao = models.CharField(max_length=100, null= True)


class Imagens(models.Model):
    fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
    arquivo = models.FileField()
    descricao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15, null= True)
    grupo = models.CharField(max_length=15, null= True)


    def path_arquivo(self):
        return 'media/' + str(self.arquivo)

    def nome_arquivo(self):
        arquivo = self.path_arquivo()
        return arquivo.split('/')[-1]

    def descricao_simples(self):
        if len(self.descricao) > 15:
            return self.descricao[0:15] + '...'
        return self.descricao


class Arquivo(models.Model):
    fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
    arquivo = models.FileField()
    descricao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, null= True)
    grupo = models.CharField(max_length=15, null= True)

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)

    def nome_arquivo(self):
        arquivo = self.path_arquivo()
        return arquivo.split('/')[-1]

    def descricao_simples(self):
        if len(self.descricao) > 15:
            return self.descricao[0:15] + '...'
        return self.descricao


class Energia(models.Model):
    fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
    energia_eletrica = models.CharField(max_length=100)





# class Decreto(models.Model):
#     fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
#     decreto = models.CharField(max_length=100)


# class Portaria(models.Model):
#     fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
#     decreto = models.CharField(max_length=100)


# class Verificados(models.Model):
#     fundiaria = models.ForeignKey(Fundiaria, on_delete= models.CASCADE)
#     status = models.IntegerField()
