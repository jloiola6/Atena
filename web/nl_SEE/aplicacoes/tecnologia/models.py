from ast import Pass
from functools import total_ordering
from pyexpat import model
from re import T
from statistics import mode
from venv import create
from django.db import models

from aplicacoes.administracao.models import Endereco, Contrato_item, Unidade_administrativa, Aluno_turma
from aplicacoes.usuario.models import Logs, Usuarios
from aplicacoes.lotacao.models import Servidor


class Link(models.Model):
    item = models.ForeignKey(Contrato_item, on_delete= models.CASCADE, null= True)
    unidade_educacional = models.ForeignKey(Endereco, on_delete= models.CASCADE, null= True)
    departamento = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null= True)
    tipo = models.CharField(max_length=30, null= True, choices=(('UNIDADE EDUCACIONAL','UNIDADE EDUCACIONAL'),('DEPARTAMENTO SEE','DEPARTAMETO SEE')))
    fornecedor = models.CharField(max_length=30, null= True, choices=(('SEE','SEE'), ('MEC', 'MEC')))
    operadora = models.CharField(max_length=15, null= True, choices=(('OI','Oi'), ('VIVO', 'Vivo'), ('CLARO', 'Claro'), ('SEM FRONTEIRAS', 'SEM FRONTEIRAS')))
    tipo_banda = models.CharField(max_length=30, null= True, choices=(('ADSL','ADSL'), ('ADSL EMPRESARIAL', 'ADSL EMPRESARIAL'), ('CIRCUITO DE DADOS', 'CIRCUITO DE DADOS'), ('CIRCUITO DE DADOS - SATÉLITE', 'CIRCUITO DE DADOS - SATÉLITE'), ('GESAC', 'GESAC')))
    status = models.CharField(max_length=10, null= True, choices=(('ATIVO','ATIVO'), ('INATIVO', 'INATIVO')))
    iplan = models.CharField(max_length=25, blank=True, null=True)
    ipwan = models.CharField(max_length=25, blank=True, null=True)
    circuito = models.CharField(max_length=40, blank=True, null=True)
    velocidade = models.CharField(max_length=40, blank=True, null=True)
    observacao = models.CharField(max_length=500, blank=True, null=True)
    data_ativo = models.DateField(null=True)
    data_alteracao = models.DateField(null=True)
    data_inativo = models.DateField(null=True)
    motivo = models.CharField(max_length=300, blank=True, null=True)
    user_inativou = models.CharField(max_length=30, blank=True, null=True)
    fonte = models.CharField(max_length=10, blank=True, null=True)
    autenticacao = models.CharField(max_length=25, blank=True, null=True)



class Firewall(models.Model):
    link = models.ForeignKey(Link, on_delete= models.CASCADE)
    ip_firewall = models.CharField(max_length=50, blank=True, null=True)


class Solicitacao(models.Model):
    unidade_administrativa = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null = True)
    endereco_escola = models.ForeignKey(Endereco, on_delete= models.CASCADE, null = True)
    tecnico_atribuido = models.ForeignKey(Servidor, on_delete= models.CASCADE, null = True)
    # tecnico_atribuido = models.IntegerField(null= True)
    user_solicitante = models.IntegerField(blank=True, null=True)
    user_finalizador = models.CharField(max_length=100, blank=True, null=True)
    user_criador = models.ForeignKey(Usuarios, on_delete= models.CASCADE)
    prioridade = models.CharField(max_length=15)
    tipo_chamado = models.CharField(max_length=100)
    tipo_unidade = models.CharField(max_length=30)
    data_abertura = models.DateTimeField()
    data_finalizacao = models.DateTimeField(null=True)
    tempo_total = models.IntegerField(blank=True, null=True)
    situacao = models.CharField(max_length=50, blank=True, null=True)
    descricao = models.CharField(max_length=1000, blank=True, null=True)
    contato = models.CharField(max_length=60)

    def tempo_total_horas(self):
        return self.tempo_total / 60


class Solicitacao_chamado(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)
    servico = models.CharField(max_length=100)
    descricao_chamado = models.CharField(max_length=1000, blank=True, null=True)
    sub_chamado = models.IntegerField()


class Solicitacao_tecnico(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete= models.CASCADE)
    user_tecnico = models.ForeignKey(Usuarios, on_delete= models.CASCADE)
    data_inicio = models.DateTimeField()
    motivo = models.CharField(max_length=500, blank=True, null=True)
    situacao = models.CharField(max_length=50, blank=True, null=True)
    data_fim = models.DateTimeField(null= True)
    total = models.IntegerField(null= True)


class Solicitacao_equipamento(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete= models.CASCADE)
    numero_documento = models.CharField(max_length=60, blank=True, null=True)
    equipamento = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    descricao = models.CharField(max_length=500, blank=True, null=True)


class Solicitacao_retirada(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete= models.CASCADE)
    horario_retirada = models.DateTimeField()
    equipamento = models.CharField(max_length=100)
    num_serie = models.CharField(max_length=100, blank=True, null=True)
    patrimonio = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.CharField(max_length=500, blank=True, null=True)


class Ec_tablet(models.Model):
    endereco_escola = models.ForeignKey(Endereco, on_delete= models.CASCADE, null = True)
    aluno_turma = models.ForeignKey(Aluno_turma, on_delete= models.CASCADE, null = True)
    serial_tablet = models.CharField(max_length=100)
    imei_tablet = models.CharField(max_length=100)
    serial_chip = models.CharField(max_length=100)
    cad_unico = models.IntegerField()

    status = models.IntegerField()
    # DESCRIÇÃO DOS STATUS
    """
    0: Entrega pendente
    1: Entregue a escola
    2: Finalizado
    """



class Auxilio_notebook(models.Model):
    gestor = models.ForeignKey(Servidor, on_delete= models.CASCADE, null = True)
    auxilio = models.IntegerField()
    notaFiscal = models.IntegerField(null = True)
    arquivo = models.FileField()
    data = models.DateField(null = True)
    data_exportacao= models.DateTimeField(null = True)
    descricao_notebook = models.CharField(max_length=300)
    motivo_devolucao = models.CharField(max_length=300)
    caixa_notebook = models.IntegerField(null = True)
    nota_notebook = models.IntegerField(null = True)
    notebook = models.IntegerField(null = True)
    carregador = models.IntegerField(null = True)

    def __str__(self):
        return self.auxilio.usuario.nome

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)


class Tipos_solicitacao(models.Model):
    tipo = models.CharField(max_length=100)
    acao = models.CharField(max_length=100)