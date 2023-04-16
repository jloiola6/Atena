from django.db import models


class Servidor_curriculo(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    nome_curso = models.CharField(max_length= 150)
    instituicao_ensino = models.CharField(max_length= 150)
    ano_conclusao = models.CharField(max_length= 150)
    tipo_formacao = models.CharField(max_length= 150)


class Servidor_documento(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    tipo = models.CharField(max_length= 150)
    data_emissao = models.DateField()
    numero = models.CharField(max_length= 150)
    complemento = models.CharField(max_length= 150)


class Servidor_familiar(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    grau_parentesco = models.CharField(max_length= 150)
    nome_familiar = models.CharField(max_length= 150)
    data_nascimento = models.DateField()
    cpf_familiar = models.CharField(max_length= 150)


class Servidor_ocorrencia(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    contrato = models.CharField(max_length= 150)
    tipo = models.CharField(max_length= 150)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    documento = models.CharField(max_length= 200)


class Servidor_contrato(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    doe = models.CharField(max_length= 150)
    parecer = models.CharField(max_length= 150)
    data_convocacao = models.DateField()
    digito = models.DateField()
    tipo = models.CharField(max_length= 150)
    cargo = models.CharField(max_length= 150)
    data_contrato = models.DateField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    municipio = models.CharField(max_length= 150)
    situacao = models.CharField(max_length= 150)


class Servidor_contrato_aditivo(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    digito = models.CharField(max_length= 150)
    id_contrato = models.CharField(max_length= 150)
    data_inicio = models.DateField()
    data_fim = models.DateField()


class Servidor_coordenador_lotacao(models.Model):
    nome = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    funcao = models.CharField(max_length= 150)
    local = models.CharField(max_length= 150)
    id_municipio = models.DateField()


class Servidor_lotacao(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    id_contrato = models.CharField(max_length= 150)
    digito = models.CharField(max_length= 150)
    unidiade_lotacao = models.CharField(max_length= 250)
    numero_memorando = models.CharField(max_length= 150)
    funcao = models.CharField(max_length= 150)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.CharField(max_length= 150)
    subconta = models.CharField(max_length= 150)
    observacao = models.CharField(max_length= 300)
    status = models.IntegerField()


class Servidor_lotacao_turma(models.Model):
    matricula = models.CharField(max_length= 150)
    cpf = models.CharField(max_length= 150)
    digito = models.CharField(max_length= 150)
    id_lotacao = models.CharField(max_length= 150)
    disciplina = models.CharField(max_length= 250)
    turno = models.CharField(max_length= 150)
    turma = models.CharField(max_length= 150)
    quantidade = models.CharField(max_length= 150)