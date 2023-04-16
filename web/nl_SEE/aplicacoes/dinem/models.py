from django.db import models

from aplicacoes.administracao.models import Endereco, Escola, Contato, Turmas, Grade, Aluno
from aplicacoes.usuario.models import Permissao, Gestor_Escolar


# Create your models here.
# class Aluno(models.Model):
#     nome = models.CharField(max_length=100)
#     nascimento = models.CharField(max_length=30)
#     cpf = models.CharField(max_length=15)
#     sexo = models.CharField(max_length=1)
#     turma = models.ForeignKey(Turmas, on_delete= models.CASCADE, blank= True, null= True)
#     nome_turma = models.CharField(max_length=100)
#     inep = models.CharField(max_length=100)

#     nome_pai = models.CharField(max_length=100)
#     nome_mae = models.CharField(max_length=100)
#     nacionalidade = models.CharField(max_length=50)
#     uf = models.CharField(max_length=5)
#     naturalidade = models.CharField(max_length=50)

#     def __str__(self):
#         return self.nome

class RelatorioFinal(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete= models.CASCADE)
    turma = models.ForeignKey(Turmas, on_delete= models.CASCADE, null= True)
    etapa = models.CharField(max_length=30)
    portugues = models.CharField(max_length=4)
    arte = models.CharField(max_length=4)
    ingles = models.CharField(max_length=4)
    ed_fisica = models.CharField(max_length=4)
    matematica = models.CharField(max_length=4)
    fisica = models.CharField(max_length=4)
    quimica = models.CharField(max_length=4)
    biologia = models.CharField(max_length=4)
    historia = models.CharField(max_length=4)
    geografia = models.CharField(max_length=4)
    filosofia = models.CharField(max_length=4)
    sociologia = models.CharField(max_length=4)
    espanhol = models.CharField(max_length=4)
    projeto_vida = models.CharField(max_length=4)
    lt_ch = models.CharField(max_length=4)
    mt_cn = models.CharField(max_length=4)
    investigacao = models.CharField(max_length=4)
    criativos = models.CharField(max_length=4)
    sociocultural = models.CharField(max_length=4)
    empreendedorismo = models.CharField(max_length=4)
    area_conhecimento = models.CharField(max_length=50)
    resultado = models.CharField(max_length=30)
    eletiva = models.CharField(max_length=4)
    estudo_orientado = models.CharField(max_length=4)
    praticas_experimentais = models.CharField(max_length=4)
    oficina_linguagens = models.CharField(max_length=4)
    oficina_matematica = models.CharField(max_length=4)
    oficina_natureza = models.CharField(max_length=4)
    oficina_humanas = models.CharField(max_length=4)
    ciencias_natureza = models.CharField(max_length=4)
    ciencias_humanas = models.CharField(max_length=4)
    matematica_tecnologias = models.CharField(max_length=4)
    linguagens_tecnologias = models.CharField(max_length=4)
    formacao_tecnica = models.CharField(max_length=4)
    pos_medio = models.CharField(max_length=4)
    protagonismo = models.CharField(max_length=4)


class Escola_Dinem(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)

    def __str__(self):
        return self.escola.nome_escola