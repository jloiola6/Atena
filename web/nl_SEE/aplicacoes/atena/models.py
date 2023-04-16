from django.db import models

# from aplicacoes.administracao.models import *

# Create your models here.
class Detalhes(models.Model):
    situacao = models.CharField(max_length=10, choices=(('Ativo','Ativo'),('Desativado','Desativado')))
    atualizar_simaed = models.IntegerField()


class Estado(models.Model):
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=2)

    class Meta:
        db_table = 'aux_estado'


class Cidade(models.Model):
    estado = models.ForeignKey(Estado, on_delete= models.CASCADE)
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'aux_cidade'


class Importacao_simaed(models.Model):
    data_hora = models.DateTimeField()
    status = models.IntegerField()
    arquivo = models.FileField()
    enturmacoes = models.IntegerField(default= 0)
    novas_enturmacoes = models.IntegerField(default= 0)

    def __str__(self):
        return f'#{self.id} Importação'
    
    def get_arquivo(self):
        return str(self.arquivo).split('/')[-1] 

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)


class Aux_simaed(models.Model):
    municipio = models.CharField(max_length=200, null=True, blank=True)
    escola = models.CharField(max_length=200, null=True, blank=True)
    inep_escola = models.CharField(max_length=200, null=True, blank=True)
    nome_aluno = models.CharField(max_length=200, null=True, blank=True)
    inep_aluno = models.CharField(max_length=200, null=True, blank=True)
    nascimento = models.CharField(max_length=200, null=True, blank=True)
    nome_pai = models.CharField(max_length=200, null=True, blank=True)
    nome_mae = models.CharField(max_length=200, null=True, blank=True)
    sexo = models.CharField(max_length=200, null=True, blank=True)
    cor = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.CharField(max_length=400, null=True, blank=True)
    transporte = models.CharField(max_length=200, null=True, blank=True)
    nome_social = models.CharField(max_length=200, null=True, blank=True)
    possui_deficiencia = models.CharField(max_length=200, null=True, blank=True)
    deficiencia = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    celular = models.CharField(max_length=200, null=True, blank=True)
    email_aluno = models.CharField(max_length=200, null=True, blank=True)
    nome_responsavel = models.CharField(max_length=200, null=True, blank=True)
    numero_responsavel = models.CharField(max_length=200, null=True, blank=True)
    cpf_responsavel = models.CharField(max_length=200, null=True, blank=True)
    cpf_aluno = models.CharField(max_length=200, null=True, blank=True)
    bolsa_familia = models.CharField(max_length=200, null=True, blank=True)
    cns = models.CharField(max_length=200, null=True, blank=True)
    ra = models.CharField(max_length=200, null=True, blank=True)

    nivel = models.CharField(max_length=200, null=True, blank=True)
    etapa = models.CharField(max_length=200, null=True, blank=True)
    turno = models.CharField(max_length=200, null=True, blank=True)
    turma = models.CharField(max_length=200, null=True, blank=True)
    periodo_letivo = models.CharField(max_length=200, null=True, blank=True)

    data_matricula = models.CharField(max_length=200, null=True, blank=True)
    situacao_matricula = models.CharField(max_length=200, null=True, blank=True)
    ano_referencia = models.CharField(max_length=200, null=True, blank=True)
    exclusivo_aee = models.CharField(max_length=200, null=True, blank=True)

    importacao_simaed = models.ForeignKey(Importacao_simaed, on_delete=models.CASCADE)