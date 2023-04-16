from aplicacoes.atena.models import *
from aplicacoes.usuario.models import Gestor_Escolar, Logs, Permissao, Usuarios

from datetime import date

ANO_ATUAL = str(date.today().year)

# TABELAS PARA UNIDADE ADMINISTRATIVA
class Unidade_administrativa_categoria(models.Model):
    nome = models.CharField(max_length=100)


class Unidade_administrativa_endereco(models.Model):
    uf = models.CharField(max_length=2, default= 'AC')
    municipio = models.CharField(max_length=50)
    regiao = models.CharField(max_length=50)
    # zoneamento = models.CharField(max_length=50, null= True, blank= True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    complemento = models.CharField(max_length=100, null= True)
    # google_map = models.CharField(max_length=500,null= True)


class Unidade_administrativa(models.Model):
    categoria = models.ForeignKey(Unidade_administrativa_categoria, on_delete= models.CASCADE)
    endereco = models.ForeignKey(Unidade_administrativa_endereco, on_delete= models.CASCADE, null=True)
    hierarquia = models.IntegerField(null= True)
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


# TABELAS PARA ESCOLA
class Detalhes_escola(models.Model):
    simaed = models.IntegerField(null=True)
    energia_eletrica = models.IntegerField(null=True)
    internet = models.IntegerField(null=True)


class Escola(models.Model):
    # coex = models.ForeignKey(Coex, on_delete= models.CASCADE, null= True)
    # consorcio = models.ForeignKey(Consorcio, on_delete= models.CASCADE, null= True)
    cod_inep = models.CharField(max_length=15, blank=True)
    cod_turmalina = models.CharField(max_length=30, blank=True, null=True)
    nome_escola = models.CharField(max_length=80)
    dependencia_adm = models.CharField(max_length=10, choices=(('Federal', 'Federal'), ('Estadual', 'Estadual'), ('Municipal', 'Municipal'), ('Privado', 'Privado')), default= 'Estadual')
    tipificacao = models.CharField(max_length=1, null= True, blank=True, choices=(('A','A'), ('B','B'), ('C','C'), ('D','D'), ('E','E')))
    total_alunos = models.IntegerField(null=True)
    detalhes = models.ForeignKey(Detalhes_escola, on_delete= models.CASCADE, null= True)

    def __str__(self):
        return self.nome_escola

    def municipio(self):
        try:
            return Endereco.objects.get(escola= self, tipo= 'S').municipio
        except:
            return None

    def regional(self):
        try:
            return Endereco.objects.get(escola= self, tipo= 'S').regiao
        except:
            return None

    def zona(self):
        try:
            return Endereco.objects.get(escola= self, tipo= 'S').tipo_localizacao
        except:
            return None


class Escola_vinculo(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    orgao = models.CharField(max_length=60, null= True, blank=True, choices=(('Secretaria de Educação/Ministério da Educação','Secretaria de Educação/Ministério da Educação'), ('Secretaria de Segurança Publica/Forças Armadas/Militar','Secretaria de Segurança Publica/Forças Armadas/Militar'), ('Secretaria da Saúde/Ministério da Saúde','Secretaria da Saúde/Ministério da Saúde'), ('Outro órgão administrativo','Outro órgão administrativo')))

# TABELAS PARA INFRAESTRUTURA
class Infraestrutura_geral(models.Model):
    agua_potavel = models.CharField(max_length=20, null= True)


class Infraestrutura_local_funcionamento(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    local = models.CharField(max_length=100)


class Infraestrutura_abastecimento_agua(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_fonte_energia(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_rede_esgoto(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_destinacao_lixo(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_tratamento_lixo(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_tipo_dependencia(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


class Infraestrutura_dependencia_tipo(models.Model):
    tipo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo


class Infraestrutura_dependencia(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.ForeignKey(Infraestrutura_tipo_dependencia, on_delete= models.CASCADE, null= True)
    tipo_dependencia = models.ForeignKey(Infraestrutura_dependencia_tipo, on_delete= models.CASCADE, null= True)
    descricao = models.CharField(max_length=50)
    capacidade_pessoas = models.CharField(max_length=3)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao


class Infraestrutura_recurso_acessibilidade(models.Model):
    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=100)


# TABELAS PARA INVENTÁRIO FINALMENTEEEEEEEEEEE
class Inventario_item_categoria(models.Model):
    nome = models.CharField(max_length= 100)


class Inventario_item_tipo(models.Model):
    categoria = models.ForeignKey(Inventario_item_categoria, on_delete= models.CASCADE)
    nome = models.CharField(max_length= 100)


class Inventario_item(models.Model):
    dependencia = models.ForeignKey(Infraestrutura_dependencia, on_delete= models.CASCADE)
    tipo = models.ForeignKey(Inventario_item_tipo, on_delete= models.CASCADE)
    patrimonio = models.CharField(max_length=30, null= True)
    quantidade = models.IntegerField(null= True)


class Inventario_item_detalhes(models.Model):
    item = models.ForeignKey(Inventario_item, on_delete= models.CASCADE)
    campo = models.CharField(max_length= 100)
    valor = models.CharField(max_length= 100)


class Endereco(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    uf = models.CharField(max_length=2, default= 'AC')
    municipio = models.CharField(max_length=50)
    regiao = models.CharField(max_length=50)
    zoneamento = models.CharField(max_length=50, null= True, blank= True)
    cep = models.CharField(max_length=10)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    complemento = models.CharField(max_length=100, null= True)
    tipo_localizacao = models.CharField(max_length=50, null= True)
    latitude = models.CharField(max_length=50, null= True)
    longitude = models.CharField(max_length=50, null= True)
    tipo = models.CharField(max_length=1, null= True, choices=(('A','Anexo'),('S','Sede')))
    localizacao_diferenciada = models.CharField(max_length=30, null= True, choices=(('Terra Indigena','Terra Indigena'),('Quilombo','Quilombo'), ('Area de Assentamento', 'Area de Assentamento ')))
    google_map = models.CharField(max_length=500,null= True)
    numero_anexo = models.IntegerField(null= True)

    infraestrutura = models.ForeignKey(Infraestrutura_geral, on_delete= models.CASCADE, null= True)

    def __str__(self):
        return f'{self.escola.nome_escola} - {self.get_tipo()}'

    def get_tipo(self):
        tipo = 'Sede'

        if self.tipo == 'A':
            return f'Anexo - {self.numero_anexo}'

        return tipo

class Contato(models.Model):

    endereco = models.ForeignKey(Endereco, on_delete= models.CASCADE)
    tipo_contato = models.CharField(max_length=1, choices=(('T','Telefone'),('C','Celular'), ('E', 'E-mail')))
    contato = models.CharField(max_length=50)
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.endereco.escola.nome_escola


class Organizacao_escolar(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    site = models.CharField(max_length=50, null= True, blank= True)
    espacos_entorno = models.CharField(max_length=3, choices=(('Sim','Sim'),('Não','Não')), null= True, blank= True)
    espacos_escola_comunidade = models.CharField(max_length=3, choices=(('Sim','Sim'),('Não','Não')), null= True, blank= True)
    pedagogia_atualizada = models.CharField(max_length=50, choices=(('Sim','Sim'),('Não','Não'), ('A escola não possui projeto/proposta pedagógica', 'A escola não possui projeto/proposta pedagógica')), null= True, blank= True)
    educacao_indigena = models.CharField(max_length=3, choices=(('Sim','Sim'),('Não','Não')), null= True, blank= True)
    # lingua_ministrada = models.CharField(max_length=50, null= True, blank= True)
    processo_seletivo = models.CharField(max_length=3, choices=(('Sim','Sim'),('Não','Não')), null= True, blank= True)


class Modalidade(models.Model): #Nova Tabela
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Etapa(models.Model): #Nova Tabela
    modalidade = models.ForeignKey(Modalidade, on_delete= models.CASCADE)
    nome = models.CharField(max_length=100)
    modalidade_nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# TABELA PARA AS DISCIPLINAS
class Disciplinas(models.Model):
    nome = models.CharField(max_length= 75)

    def __str__(self):
        return self.nome

# TABELAS PARA MATRIZ
class Matriz(models.Model):
    etapa = models.ForeignKey(Etapa, on_delete= models.CASCADE)
    nome = models.CharField(max_length=100)


class Matriz_disciplina(models.Model):
    matriz = models.ForeignKey(Matriz, on_delete= models.CASCADE)
    disciplina = models.ForeignKey(Disciplinas, on_delete= models.CASCADE)
    carga_horaria = models.CharField(max_length= 3)


# TABELA PARA TURMAS
class Turmas(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE, null= True)
    endereco = models.ForeignKey(Endereco, on_delete= models.CASCADE)
    nome = models.CharField(max_length=150)
    turno = models.CharField(max_length=15, choices=(('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'),('Noturno','Noturno'), ('Integral', 'Integral')))
    etapa = models.ForeignKey(Etapa, on_delete= models.CASCADE, null= True, blank= True)
    ano_serie = models.CharField(max_length=50)
    total_alunos = models.CharField(max_length= 3)
    ano_letivo = models.CharField(max_length= 4)

    matriz = models.ForeignKey(Matriz, on_delete= models.CASCADE, null= True)

    importacao = models.CharField(max_length=50, null= True)

    def __str__(self):
        return f'{self.nome} {self.turno} - {self.ano_letivo}'

    def qtd_alunos(self):
        if self.ano_letivo == ANO_ATUAL:
            return Aluno_turma.objects.filter(turma= self, status= 1).count()
        else:
            return Aluno_turma.objects.filter(turma= self).count()


    def nome_simples(self):
        if len(self.nome) > 10:
            return f'{self.nome[0:10]}...'
        else:
            return self.nome


class Modalidade_escola(models.Model): #Nova Tabela
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete= models.CASCADE)


class Etapa_escola(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete= models.CASCADE)

    def __str__(self):
        return self.etapa.nome


class Grade(models.Model):
    turma = models.ForeignKey(Turmas, on_delete= models.CASCADE)
    disciplina = models.ForeignKey(Disciplinas, on_delete= models.CASCADE, null= True)
    rota = models.CharField(max_length= 50, null= True)
    carga_horaria = models.CharField(max_length= 3)
    ano = models.CharField(max_length= 5)

    # ID REFERENTE À LOTAÇÃO DO PROFESSOR
    professor = models.IntegerField(null= True)
    status = models.IntegerField()


class Organizacao_reserva_cota(models.Model):
    organizacao_escolar = models.ForeignKey(Organizacao_escolar, on_delete= models.CASCADE)
    tipo_cota = models.CharField(max_length=90, choices=(('Autodeclarado preto, pardo ou indígena (PPI)','Autodeclarado preto, pardo ou indígena (PPI)'),('Condição de renda','Condição de renda'), ('Oriundo da escola pública', 'Oriundo da escola pública'), ('Pessoa com deficiência (PCD)', 'Pessoa com deficiência (PCD)'), ('Outros grupos', 'Outros grupos')), blank= True, null= True)


class Organizacao_formas_organizacao(models.Model):
    organizacao_escolar = models.ForeignKey(Organizacao_escolar, on_delete= models.CASCADE)
    tipo_organizacao = models.CharField(max_length=100, choices=(('Sério/Ano (séries anuais)','Sério/Ano (séries anuais)'),('Períodos semestrais','Períodos semestrais'), ('Ciclo(s) do ensino fundamental', 'Ciclo(s) do ensino fundamental'), ('Grupos não seriados com base na idade ou competência (art. 23 LDB)', 'Grupos não seriados com base na idade ou competência (art. 23 LDB)'), ('Módulos', 'Módulos'), ('Alternacia regular de períodos de estudo', 'Alternacia regular de períodos de estudo')))


class Organizacao_instrumento_educativo(models.Model):
    organizacao_escolar = models.ForeignKey(Organizacao_escolar, on_delete= models.CASCADE)
    instrumento = models.CharField(max_length=90, choices=(('Acervo Multimídia','Acervo Multimídia'),('Instrumentos musicais','Instrumentos musicais'), ('Materiais pedagógicos para educação escolar indígena', 'Materiais pedagógicos para educação escolar indígena'), ('Brinquedos para a educação infantil', 'Brinquedos para a educação infantil'), ('Jogos Educativos', 'Jogos Educativos'), ('Materiais pedagógicos para educação das relações etnico-raciais', 'Materiais pedagógicos para educação das relações etnico-raciais'), ('Conjunto de materiais científicos', 'Conjunto de materiais científicos'), ('Materiais para atividades culturais e artísticas', 'Materiais para atividades culturais e artísticas'), ('Materiais pedagógicos para educação do campo', 'Materiais pedagógicos para educação do campo'), ('Equipamento para ampliação de som','Equipamento para ampliação de som'), ('Materiais para práticas desportiva e recreação', 'Materiais para práticas desportiva e recreação')), blank= True, null= True)


class Organizacao_colegiados_escola(models.Model):
    organizacao_escolar = models.ForeignKey(Organizacao_escolar, on_delete= models.CASCADE)
    orgao_colegiado = models.CharField(max_length=50, choices=(('Associação de pais','Associação de pais'),('Associação de pais e mestres','Associação de pais e mestres'), ('Conselho escolar', 'Conselho escolar'), ('Gremio estudantil', 'Gremio estudantil'), ('Outros', 'Outros')), null= True, blank= True)


class Detalhes_Indigena(models.Model):
    escola = models.ForeignKey(Escola, on_delete= models.CASCADE, null= True, blank= True)
    inep = models.CharField(max_length=30, null= True, blank= True)
    localizacao = models.CharField(max_length=100)
    aldeia = models.CharField(max_length=50)
    etnia = models.CharField(max_length=50)


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100)
    nascimento = models.CharField(max_length=30)
    cpf = models.CharField(max_length=15)
    sexo = models.CharField(max_length=1)

    cod_inep = models.CharField(max_length=50)
    nome_pai = models.CharField(max_length=100)
    nome_mae = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50, null= True)
    uf = models.CharField(max_length=5, null= True)
    naturalidade = models.CharField(max_length=50, null= True)
    cor = models.CharField(max_length=25)
    endereco = models.CharField(max_length=350)
    transporte = models.IntegerField()
    bolsa_familia = models.IntegerField()
    deficiencia = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    celular = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    nome_responsavel = models.CharField(max_length=100)
    responsavel_telefone = models.CharField(max_length=100)
    ra = models.CharField(max_length=50)
    data_matricula = models.CharField(max_length=50)
    data_encerramento = models.CharField(max_length=50)
    situacao = models.CharField(max_length=50)
    importacao = models.CharField(max_length=50, null= True)

    def __str__(self):
        return self.nome

class Professor_aluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete= models.CASCADE)
    status = models.IntegerField()

    # ID REFERENTE À LOTAÇÃO DO PROFESSOR
    professor = models.IntegerField()

#TABELAS PARA CONTRATO
class Contrato_empresa(models.Model):
    nome = models.CharField(max_length=200)
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=50, blank=True)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    bairro = models.CharField(max_length=70)
    cep = models.CharField(max_length=10)
    municipio = models.CharField(max_length=50)
    uf = models.CharField(max_length=3)
    telefone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Contrato_contrato(models.Model):
    tipo_contrato = models.CharField(max_length=60, null= True)
    numero_contrato = models.CharField(max_length=30, null= True)
    empresa = models.ForeignKey(Contrato_empresa, on_delete= models.CASCADE)
    objeto = models.CharField(max_length=800, null= True)
    data_inicio = models.DateField(null= True, blank= True)
    data_termino = models.DateField(null= True, blank= True)
    data_aditivo = models.DateField(null= True, blank= True)
    valor_total_aditivo = models.CharField(max_length=30, null= True, blank= True)
    valor_total = models.CharField(max_length=30, null= True)
    valor_global = models.CharField(max_length=30, null= True)
    meses_vigencia = models.CharField(max_length=3, null= True)
    numero_sei = models.CharField(max_length=30, null= True)
    documento_sei = models.CharField(max_length=30, null= True)
    situacao = models.CharField(max_length=30, null= True)
    empenho = models.CharField(max_length=30, null= True, blank= True)
    fonte_recurso = models.CharField(max_length= 30, null= True)

    def __str__(self):
        return self.numero_contrato


class Vinculacao_contrato(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    unidade_administrativa = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE)


class Fonte_contrato(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    fonte_recurso = models.CharField(max_length= 30, null= True)

    def __str__(self):
        return self.fonte_recurso


class Contrato_aditivo(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    tipo = models.CharField(max_length=30)
    data_inicio = models.DateField(null= True, blank= True)
    data_termino = models.DateField(null= True, blank= True)
    valor_total = models.CharField(max_length=30, null= True)
    valor_global = models.CharField(max_length=30, null= True)
    meses_vigencia = models.CharField(max_length=3, null= True)
    diferenca = models.CharField(max_length=30, null= True)


class Contrato_item(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    numero_item = models.CharField(max_length=3)
    numero_lote = models.CharField(max_length=3, blank= True, null= True)
    metragem_contratada = models.CharField(max_length=14, blank= True, null= True)
    metragem_mensal = models.CharField(max_length=7, blank= True, null= True)
    descricao = models.CharField(max_length=300)
    quantidade = models.CharField(max_length=9)
    valor_unitario = models.CharField(max_length=30)
    remuneracao = models.CharField(max_length=30, null= True)
    valor_total = models.CharField(max_length=30)
    qtd_vagas = models.IntegerField(null= True)
    status = models.IntegerField()
    vagas = models.IntegerField(null= True)

    def descricao_simples(self):
        if len(self.descricao) > 100:
            return f'{self.descricao[0:99]}...'
        else:
            return self.descricao

    def metragem_total(self):
        self.metragem = int(self.metragem_mensal)

        return "{0:,}".format(self.metragem).replace(',', '.')

    def metragem_disponivel(self):
        if '.' in self.quantidade:
            self.valor = str(self.quantidade).split('.')
            self.novo_valor = str(self.qtd_vagas) + '.' + self.valor[1]
            self.vagas_restantes = float(self.novo_valor) * int(self.metragem_contratada)
            self.vagas_restantes = ("{0:,}".format(self.vagas_restantes).replace(',', '.'))[:-2]
        else:
            self.vagas_restantes = int(self.qtd_vagas * int(self.metragem_contratada))
            self.vagas_restantes = "{0:,}".format(self.vagas_restantes).replace(',', '.')

        return self.vagas_restantes


class Contrato_posto_vigilante(models.Model):
    item = models.ForeignKey(Contrato_item, on_delete= models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete= models.CASCADE, null= True)
    unidade_administrativa = models.ForeignKey(Unidade_administrativa, on_delete= models.CASCADE, null= True)
    vagas_ocupadas = models.IntegerField()
    funcionario1 = models.CharField(max_length=80, null= True)
    funcionario2 = models.CharField(max_length=80, null= True)
    funcionario3 = models.CharField(max_length=80, null= True)
    status = models.IntegerField()


class Contrato_item_mudanca(models.Model):
    contrato_aditivo = models.ForeignKey(Contrato_aditivo, on_delete= models.CASCADE)
    numero_item = models.CharField(max_length=3)
    numero_lote = models.CharField(max_length=3, blank= True, null= True)
    metragem_contratada_antigo = models.CharField(max_length=4, blank= True, null= True)
    metragem_mensal_antigo = models.CharField(max_length=7, blank= True, null= True)
    descricao = models.CharField(max_length=300)
    quantidade_antigo = models.CharField(max_length=9)
    valor_unitario_antigo = models.CharField(max_length=30)
    valor_total_antigo = models.CharField(max_length=30)
    remuneracao_antigo = models.CharField(max_length=30, null= True)
    status_antigo = models.IntegerField(null= True)

    metragem_contratada_novo = models.CharField(max_length=4, blank= True, null= True)
    metragem_mensal_novo = models.CharField(max_length=7, blank= True, null= True)
    quantidade_novo = models.CharField(max_length=9, null= True)
    valor_unitario_novo = models.CharField(max_length=30, null= True)
    valor_total_novo = models.CharField(max_length=30, null= True)
    remuneracao_novo = models.CharField(max_length=30, null= True)
    status_novo = models.IntegerField(null= True)


class Contrato_gestor(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    gestor_titular = models.CharField(max_length=200)
    atribuicao_gestor_titular = models.CharField(max_length=30)
    doe_gestor_titular = models.CharField(max_length=30)
    portaria_gestor_titular = models.CharField(max_length=30)
    data_portaria_gestor_titular = models.DateField()
    data_publicacao_gestor_titular = models.DateField()
    data_inicio_gestor_titular = models.DateField()
    data_termino_gestor_titular = models.DateField()
    gestor_substituto = models.CharField(max_length=200)
    atribuicao_gestor_substituto = models.CharField(max_length=30)
    doe_gestor_substituto = models.CharField(max_length=30)
    portaria_gestor_substituto = models.CharField(max_length=30)
    data_portaria_gestor_substituto = models.DateField()
    data_publicacao_gestor_substituto = models.DateField()
    data_inicio_gestor_substituto = models.DateField()
    data_termino_gestor_substituto = models.DateField()
    fiscal_titular = models.CharField(max_length=200)
    atribuicao_fiscal_titular = models.CharField(max_length=30)
    doe_fiscal_titular = models.CharField(max_length=30)
    portaria_fiscal_titular = models.CharField(max_length=30)
    data_portaria_fiscal_titular = models.DateField()
    data_publicacao_fiscal_titular = models.DateField()
    data_inicio_fiscal_titular = models.DateField()
    data_termino_fiscal_titular = models.DateField()
    fiscal_substituto = models.CharField(max_length=200)
    atribuicao_fiscal_substituto = models.CharField(max_length=30)
    doe_fiscal_substituto = models.CharField(max_length=30)
    portaria_fiscal_substituto = models.CharField(max_length=30)
    data_portaria_fiscal_substituto = models.DateField()
    data_publicacao_fiscal_substituto = models.DateField()
    data_inicio_fiscal_substituto = models.DateField()
    data_termino_fiscal_substituto = models.DateField()
    situacao = models.CharField(max_length=30)


class Contrato_responsavel(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    nome = models.CharField(max_length=200, null= True)
    cpf = models.CharField(max_length=20, null= True)
    rg = models.CharField(max_length=15, null= True)
    orgao = models.CharField(max_length=30, null= True)
    rua = models.CharField(max_length=100, null= True)
    numero = models.CharField(max_length=10, null= True)
    bairro = models.CharField(max_length=70, null= True)
    cep = models.CharField(max_length=20, null= True)
    municipio = models.CharField(max_length=50, null= True)
    uf = models.CharField(max_length=3, null= True)


class Contrato_documento(models.Model):
    contrato = models.ForeignKey(Contrato_contrato, on_delete= models.CASCADE)
    arquivo = models.FileField()
    descricao = models.CharField(max_length=300, null=True)

    def path_arquivo(self):
        return 'static/media/' + str(self.arquivo)


class Contrato_empenho(models.Model):
    fonte = models.ForeignKey(Fonte_contrato, on_delete= models.CASCADE)
    documento = models.ForeignKey(Contrato_documento, on_delete= models.CASCADE, null= True)
    tipo = models.CharField(max_length=60, null= True)
    num_empenho = models.CharField(max_length=25, null= True)
    data_emissao = models.DateField(null=True)
    cod_orcamento = models.CharField(max_length=40, null= True)
    cod_despesa = models.CharField(max_length=20, null= True)
    valor = models.CharField(max_length=30, null= True)

# TABELA PARA ENTURMAÇÃO DE UM ALUNO
class Aluno_turma(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete= models.CASCADE)
    turma = models.ForeignKey(Turmas, on_delete= models.CASCADE)
    status = models.IntegerField()

    importacao = models.CharField(max_length=50, null= True)

    def __str__(self):
        status = 'Inativa'

        if self.status:
            status = 'Ativa'
        return f'{self.turma.endereco.escola} - {self.turma} - {status}'

    def get_status(self):
        status = 'Inativa'

        if self.status:
            return 'Ativa'

        return status


class Grade_professor_adm(models.Model):
    disciplina = models.ForeignKey(Disciplinas, on_delete= models.CASCADE, null= True)
    professor = models.IntegerField(null= True)
    status = models.IntegerField()
