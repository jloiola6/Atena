from aplicacoes.administracao.models import Endereco, Unidade_administrativa
from django.db import models

from aplicacoes.administracao.models import Contrato_contrato, Disciplinas


class Cargo(models.Model):
    nome = models.CharField(max_length= 150)
    classe = models.CharField(max_length= 15)
    carga_horaria = models.CharField(max_length= 3)
    nivel = models.CharField(max_length=35)
    tipo = models.CharField(max_length=15, choices=(('EFETIVO','EFETIVO'),('TEMPORÁRIO','TEMPORÁRIO'), ('COMISSÃO', 'COMISSÃO')))
    atribuicao = models.CharField(max_length=200)
    situacao = models.CharField(max_length=15, choices=(('ATIVO','ATIVO'),('EXTINTO','EXTINTO')))
    vencimento = models.FloatField(max_length=50, null=True)

    def __str__(self):
        return self.nome


class Servidor(models.Model):
    matricula = models.CharField(max_length=15, null= True)
    nome = models.CharField(max_length=100, null= True)
    nome_social = models.CharField(max_length=100, null=True, blank= True)
    data_nascimento = models.DateField(null= True)
    cpf = models.CharField(max_length=11, null= True)
    rg = models.CharField(max_length=11, null= True)
    sexo = models.CharField(max_length=50, null= True)
    uf = models.CharField(max_length=4, null=True, blank= True)
    nacionalidade = models.CharField(max_length=50, null= True)
    naturalidade = models.CharField(max_length=50, null= True)
    situacao = models.CharField(max_length=50, null= True)
    pis = models.CharField(max_length=30, null= True)
    titulo_eleitor = models.CharField(max_length=30, null= True)

    def __str__(self):
        return self.nome.upper()

    def nome_simples(self):
        nome = self.nome.upper().split()
        nome = f'{nome[0]} {nome[1]}'
        return nome

    def cpf_oculto(self):
        return f'{self.cpf[0:3]}******-{self.cpf[9:13]}'


class Servidor_endereco(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    uf = models.CharField(max_length=4, null=True, blank= True)
    municipio = models.CharField(max_length=50, null=True, blank= True)
    regiao = models.CharField(max_length=50, null=True, blank= True)
    cep = models.CharField(max_length=10, null=True, blank= True)
    rua = models.CharField(max_length=100, null=True, blank= True)
    numero = models.CharField(max_length=50, null=True, blank= True)
    bairro = models.CharField(max_length=50, null=True, blank= True)
    complemento = models.CharField(max_length=100, null= True, blank= True)
    tipo_localizacao = models.CharField(max_length=50, null= True, blank= True)

    def __str__(self):
        return self.servidor.nome


class Servidor_contato(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    tipo_contato = models.CharField(max_length=1, choices=(('T','Telefone'),('C','Celular'), ('E', 'E-mail')), null=True, blank= True)
    contato = models.CharField(max_length=50, null=True, blank= True)

    def __str__(self):
        return self.servidor.nome


class Servidor_banco(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    instituicao = models.CharField(max_length=30, choices=(('BANCO DO BRASIL','BANCO DO BRASIL'),('BRADESCO','BRADESCO'), ('CAIXA ECONÔMICA FEDERAL', 'CAIXA ECONÔMICA FEDERAL'), ('SANTANDER', 'SANTANDER')), null=True, blank= True)
    tipo_conta = models.CharField(max_length=20, choices=(('CONTA-CORRENTE','CONTA-CORRENTE'),('CONTA-SALÀRIO','CONTA-SALÀRIO')), null=True, blank= True)
    agencia = models.CharField(max_length= 30, null=True, blank= True)
    conta = models.CharField(max_length= 40, null=True, blank= True)

    def __str__(self):
        return self.conta


class Servidor_contrato(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE, null= True, default= None)
    cargo = models.ForeignKey(Cargo, on_delete= models.CASCADE, null= True, default= None)
    numero_contrato = models.CharField(max_length=20, null= True)
    doe = models.CharField(max_length=50, null= True)
    parecer = models.CharField(max_length=50, null= True)
    data_convocacao = models.DateField(null= True)
    digito = models.CharField(max_length=10, null= True)
    tipo_contrato = models.CharField(max_length=60, null= True)
    data_contrato = models.DateField(null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    municipio = models.CharField(max_length=50, null= True)
    situacao = models.CharField(max_length=50, null= True)
    saldo = models.CharField(max_length=15, null= True)

    diario_homologacao = models.CharField(max_length=8, null= True)
    disciplina_convocacao = models.ForeignKey(Disciplinas, on_delete= models.CASCADE, null= True, default= None)
    data_cancelamento = models.DateField(null= True)
    motivo_cancelamento = models.CharField(max_length=200, null= True)
    ano_referencia = models.CharField(max_length=4, null=True)

    def __str__(self):
        return self.servidor.nome

    def convocacao(self):
        return str(self.data_contrato)

    def contratacao(self):
        return str(self.data_convocacao)

    def inicio(self):
        return str(self.data_inicio)

    def termino(self):
        return str(self.data_termino)


class Servidor_contrato_formacao(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True, default= None)
    tipo = models.CharField(max_length=20, null= True)
    formacao = models.CharField(max_length=50, null= True)


class Funcao(models.Model):
    nome = models.CharField(max_length=100, null= True)
    tipo = models.CharField(max_length=50, null= True, choices=(('Unidade Escolar','Unidade Escolar'),('Unidade Administrativa','Unidade Administrativa')))


class Servidor_subconta(models.Model):
    sub = models.CharField(max_length=11, null= True)
    fonte = models.CharField(max_length=50, null= True)
    situacao = models.CharField(max_length=50, null= True)
    descricao = models.CharField(max_length=200, null= True)


class Servidor_lotacao(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    unidade_escolar = models.ForeignKey(Endereco, on_delete= models.CASCADE, null= True)
    unidade_adm = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null= True)
    subconta = models.ForeignKey(Servidor_subconta, on_delete= models.CASCADE, null= True)
    numero_memorando = models.CharField(max_length= 20, null= True)
    numero_sei = models.CharField(max_length= 50, null= True)
    funcao = models.CharField(max_length= 100, null= True)
    orgao_cedido = models.CharField(max_length= 150, null= True)
    tipo_lotacao = models.CharField(max_length= 30, null= True)
    orgao_origem = models.CharField(max_length= 15, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    carga_horaria = models.CharField(max_length= 10, null= True)
    
    status = models.IntegerField(null= True)
    

    motivo = models.CharField(max_length= 500, blank= True, null= True)
    observacoes = models.CharField(max_length= 500, blank= True, null= True)
    turno_manha = models.IntegerField(null= True)
    turno_tarde = models.IntegerField(null= True)
    turno_noite = models.IntegerField(null= True)
    data_memorando = models.DateTimeField(null= True)
    ano_referencia = models.CharField(max_length= 4, null= True)
    portaria = models.CharField(max_length= 200, null= True)
    destituicao = models.CharField(max_length= 200, null= True)
    doe_portaria = models.CharField(max_length= 200, null= True)
    doe_destituicao = models.CharField(max_length= 200, null= True)


    def __str__(self):
        return self.contrato.servidor.nome


class Servidor_ocorrencia_funcional(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    tipo_ocorrencia = models.CharField(max_length=50, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    data_falecimento = models.DateField(null= True)
    data_expedicao = models.DateField(null= True)
    portaria = models.CharField(max_length=200, null= True)
    parecer = models.CharField(max_length=200, null= True)
    cid = models.CharField(max_length=200, null= True)
    sei = models.CharField(max_length=200, null= True)
    pad = models.CharField(max_length=200, null= True)
    doe = models.CharField(max_length=200, null= True)
    decreto = models.CharField(max_length=200, null= True)
    ano_exercicio = models.CharField(max_length=200, null= True)
    laudo_requisicao = models.CharField(max_length=200, null= True)
    sentenca = models.CharField(max_length=200, null= True)
    folha = models.CharField(max_length=200, null= True)
    livro = models.CharField(max_length=200, null= True)
    termo = models.CharField(max_length=200, null= True)
    registro_obito = models.CharField(max_length=200, null= True)
    observacao = models.CharField(max_length=500, null= True)
    ano_readequacao = models.CharField(max_length=200, null= True)
    status = models.IntegerField()


class Servidor_hora_complementar(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    carga_horaria = models.CharField(max_length=50, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    status = models.IntegerField()


class Servidor_gratificacao(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    porcentagem = models.CharField(max_length=50, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    status = models.IntegerField()


class Servidor_documento(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    documento = models.FileField()
    descricao = models.CharField(max_length=100, null= True)
    categoria = models.CharField(max_length=30, null= True)

    def path_arquivo(self):
        return 'static/media/' + str(self.documento)

    def descricao_simples(self):
        if len(self.descricao) > 50:
            return self.descricao[0:50] + '...'
        return self.descricao


class Atualizacao_cadastral(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    ultima_atualizacao = models.DateTimeField()
    log = models.IntegerField()


class Instituicoes(models.Model):
    nome = models.CharField(max_length=250)
    sigla = models.CharField(max_length=25)
    uf = models.CharField(max_length=10)

    class Meta:
        db_table = 'aux_instituicoes'


class Cursos_graduacao(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'aux_cursos_graduacao'


class Escolas(models.Model):
    nome = models.CharField(max_length=250)

    class Meta:
        db_table = 'aux_escolas'


class Lotacao_assinatura(models.Model):
    lotacao = models.ForeignKey(Servidor_lotacao, on_delete= models.CASCADE)
    gestor = models.CharField(max_length=60, null= True)
    cargo_gestor = models.CharField(max_length=100, null= True)
    lotacao_gestor = models.CharField(max_length=100, null= True)
    tecnico = models.CharField(max_length=60, null= True)
    funcao_tecnico = models.CharField(max_length=100, null= True)
    sigla = models.CharField(max_length=20, null= True)
    rua = models.CharField(max_length=100, null= True)
    numero = models.CharField(max_length=50, null= True)
    bairro = models.CharField(max_length=50, null= True)
    cep = models.CharField(max_length=10, null= True)
    municipio = models.CharField(max_length=50, null= True)
    uf = models.CharField(max_length=4, null= True)
    telefone = models.CharField(max_length=50, null= True)
    email = models.CharField(max_length=100, null= True)


class Servidor_contrato_aditivo(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    data_inicio = models.DateField(null= True)
    data_termino = models.DateField(null= True)
    status = models.IntegerField()


class Servidor_escolaridade(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    formacao= models.CharField(max_length=60, null= True)
    escola= models.CharField(max_length=100, null= True)
    data_conclusao= models.DateField(null= True)
    curso= models.CharField(max_length=100, null= True)
    instituicao= models.CharField(max_length=100, null= True)
    situacao= models.CharField(max_length=60, null= True)


class Servidor_vdp(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE, null= True)
    ano_periodo = models.CharField(max_length= 4)
    ano_verificacao = models.CharField(max_length= 4)
    valor_liquido = models.FloatField()
    valor_bruto = models.FloatField()
    status = models.IntegerField()
    tipo = models.CharField(max_length= 30)
    situacao = models.CharField(max_length= 30)


class Cargo_vencimento(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete= models.CASCADE)
    ref = models.CharField(max_length= 50)
    valor = models.FloatField()

    def __str__(self):
        return self.cargo.nome


# TABELAS PARA O SERVIÇO DA QUALIDADE DE VIDA
class Servico(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    servico = models.ForeignKey(Servico, on_delete= models.CASCADE)
    atendente = models.ForeignKey(Servidor, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.servico.nome} - {self.atendente}'

class Atendimento_dia(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete= models.CASCADE)
    dia = models.IntegerField()
    hora = models.TimeField()

    def __str__(self):
        return f'{self.dia} - {self.hora}'

class Agendamento(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    atendimento = models.ForeignKey(Atendimento, on_delete= models.CASCADE)
    data = models.DateField(null=True)
    hora_atendimento = models.TimeField(null= True)
    contato = models.CharField(max_length=50, null=True)

    status = models.IntegerField()

    # 0 -> Pendente
    # 1 -> Concluidos
    # 2 -> Cancelados
    # 3 -> Não Compareceu
    # 4 -> Lista de espera

    atividade = models.CharField(max_length=10, null= False)

    def __str__(self) -> str:
        return f'{self.data} - {self.hora_atendimento}'

# TABELAS PARA O SERVIÇO DE AUTORIZAÇÃO DE LOTAÇÃO
class Autorizacao_lotacao(models.Model):
    autorizador = models.ForeignKey(Servidor, on_delete= models.CASCADE)
    lotacao = models.ForeignKey(Servidor_lotacao, on_delete= models.CASCADE)
    status = models.IntegerField()
    data = models.DateField()
    motivo = models.CharField(max_length=300, null=True)


class Contrato_cancelamento(models.Model):
    contrato = models.ForeignKey(Servidor_contrato, on_delete= models.CASCADE)
    documento = models.FileField()

    def path_arquivo(self):
        return 'static/media/' + str(self.documento)
