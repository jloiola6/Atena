from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nome = models.CharField(max_length=70)
    login = models.CharField(max_length=50)
    cpf  = models.CharField(max_length=15)
    senha = models.CharField(max_length=40)
    email = models.CharField(max_length=60)
    status = models.CharField(max_length=10, choices=(('Ativo','Ativo'), ('Inativo','Inativo')))
    servidor = models.IntegerField(null=True) #Bruno Style

    def __str__(self):
        return self.nome


class Aplicacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    aplicacao = models.ForeignKey(Aplicacao, on_delete= models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.aplicacao} - {self.nome}'


class Permissao(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete= models.CASCADE, null= True)
    usuario_pendente = models.CharField(max_length=100, null= True, blank= True)
    servico = models.ForeignKey(Servico, on_delete= models.CASCADE)
    consultar = models.IntegerField()
    editar = models.IntegerField()
    imprimir = models.IntegerField()

    def __str__(self):
        return f'{self.servico.aplicacao.nome} - {self.servico.nome}'


class Gestor_Escolar(models.Model):
    permissao = models.ForeignKey(Permissao, on_delete= models.CASCADE, null= True)
    inep = models.CharField(max_length= 30)

    def __str__(self):
        return self.inep


class Logs(models.Model):
    entrada = models.CharField(max_length=80)
    saida = models.CharField(max_length=80, null= True)
    usuario = models.ForeignKey(Usuarios, on_delete= models.CASCADE)
    ip = models.CharField(max_length=50)
