from datetime import date
from aplicacoes.atena.models import Cidade
from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.core.views import handle_uploaded_file
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import *


def memorando():
    data_dia = str(date.today()).split("-")
    ultimo = ((Servidor_contrato.objects.all().last()).numero_contrato).split('/')
    if ultimo[1] == data_dia[0]:
        valor = int(ultimo[0])+1
        valor = f"{valor}/{data_dia[0]}"
    else:
        valor = f"1/{data_dia[0]}"
    return valor

def formulario_contrato(request, edicao, servidor):

    #Capturando dados
    numero_contrato = memorando()
    tipo = request.POST.get('tipo')
    if tipo != 'PERMUTA' and tipo != 'CEDIDO' and tipo != 'ESTAGIÁRIO':
        doe = request.POST.get('doe')
        parecer = request.POST.get('parecer')
        if 'digito-pendente' not in request.POST and request.POST.get('digito') == '' or 'digito-pendente' in request.POST:
            digito = 'Pendente'
        else:
            digito = request.POST.get('digito')
        convocacao = request.POST.get('convocacao')
        if convocacao == '':
            convocacao = None
        contratacao = request.POST.get('contratacao')
        if contratacao == '':
            contratacao = None
    cargo = request.POST.get('cargo')
    inicio = request.POST.get('inicio')
    termino = request.POST.get('termino')
    municipio = request.POST.get('municipio')
    situacao = request.POST.get('situacao')

    if tipo != 'ESTAGIÁRIO':
        cargo = Cargo.objects.get(id= cargo)
        municipio = Cidade.objects.get(id= municipio)

    if edicao:
        id_contrato = request.GET.get('id_contrato')
        contrato = Servidor_contrato.objects.filter(id= id_contrato)

        if tipo == 'ESTAGIÁRIO':
            inputs_contrato = {'numero_contrato': numero_contrato, 'tipo_contrato': tipo,  'data_inicio': inicio, 'data_termino': termino, 'situacao': situacao}
        elif tipo == 'PERMUTA' or tipo == 'CEDIDO':
            inputs_contrato = {'numero_contrato': numero_contrato, 'tipo_contrato': tipo, 'cargo': cargo.nome,  'data_inicio': inicio, 'data_termino': termino, 'municipio': municipio, 'situacao': situacao}
        else:
            inputs_contrato = {'numero_contrato': numero_contrato, 'doe': doe, 'parecer': parecer, 'digito': digito, 'tipo_contrato': tipo, 'cargo': cargo.nome, 'data_convocacao': convocacao,  'data_contrato': contratacao,  'data_inicio': inicio, 'data_termino': termino, 'municipio': municipio, 'situacao': situacao}

        modificacoes_contrato = dict_compare(contrato.values()[0], inputs_contrato)
        contrato = contrato[0]
    else:
        contrato = Servidor_contrato()
        modificacoes_contrato = None

    if tipo == 'EFETIVO' or tipo == 'TEMPORÁRIO' or tipo == 'CONTRATAÇÃO DIRETA' or tipo == 'COMISSÃO':
        if edicao:
            contrato.digito = digito
            contrato.servidor = servidor
            contrato.numero_contrato = numero_contrato
            contrato.tipo_contrato = tipo
            contrato.cargo = cargo
            contrato.municipio = municipio.nome
            contrato.doe = doe
            contrato.parecer = parecer
            contrato.data_convocacao = convocacao
            contrato.data_contrato = contratacao
            contrato.data_inicio = inicio
            if tipo != 'EFETIVO':
                contrato.data_termino = termino
            contrato.situacao = situacao
            contrato.saldo = cargo.carga_horaria

            if 'PROFESSOR' in cargo.nome:
                diario_homologacao = request.POST.get('diario-homologacao')
                id_disciplina = request.POST.get('disciplina-convocacao')

                if id_disciplina:
                    disciplina_convocacao = Disciplinas.objects.get(id= id_disciplina)
                else:
                    disciplina_convocacao = None

                contrato.diario_homologacao = diario_homologacao
                contrato.disciplina_convocacao = disciplina_convocacao

            contrato.ano_referencia = str(date.today().year)
            contrato.save()
            salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato', modificacoes_contrato)
        else:
            if not Servidor_contrato.objects.filter(servidor= servidor, digito= digito).exists():

                contrato.servidor = servidor
                contrato.numero_contrato = numero_contrato
                contrato.tipo_contrato = tipo
                contrato.cargo = cargo
                contrato.municipio = municipio.nome
                contrato.digito = digito
                contrato.doe = doe
                contrato.parecer = parecer
                contrato.data_convocacao = convocacao
                contrato.data_contrato = contratacao
                contrato.data_inicio = inicio
                if tipo != 'EFETIVO':
                    contrato.data_termino = termino
                contrato.situacao = situacao
                contrato.saldo = cargo.carga_horaria

                if 'PROFESSOR' in cargo.nome:
                    diario_homologacao = request.POST.get('diario-homologacao')
                    id_disciplina = request.POST.get('disciplina-convocacao')

                    if id_disciplina:
                        disciplina_convocacao = Disciplinas.objects.get(id= id_disciplina)
                    else:
                        disciplina_convocacao = None

                    contrato.diario_homologacao = diario_homologacao
                    contrato.disciplina_convocacao = disciplina_convocacao

                contrato.ano_referencia = str(date.today().year)
                contrato.save()
                salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato', modificacoes_contrato)
            else:
                contrato = None

    elif tipo == 'PERMUTA' or tipo == 'CEDIDO':
        contrato.servidor = servidor
        contrato.numero_contrato = numero_contrato
        contrato.tipo_contrato = tipo
        contrato.cargo = cargo
        contrato.municipio = municipio.nome
        contrato.data_inicio = inicio
        contrato.data_termino = termino
        contrato.situacao = situacao
        contrato.saldo = cargo.carga_horaria

        contrato.ano_referencia = str(date.today().year)
        contrato.save()
        salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato', modificacoes_contrato)

    else:
        contrato.numero_contrato = numero_contrato
        contrato.servidor = servidor
        contrato.tipo_contrato = tipo
        contrato.data_inicio = inicio
        contrato.data_termino = termino
        contrato.situacao = situacao
        contrato.ano_referencia = str(date.today().year)
        contrato.save()
        salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato', modificacoes_contrato)

    return contrato

def formulario_contrato_antiga(request, edicao, servidor):
    #Capturando dados
    numero_contrato = memorando()
    tipo = request.POST.get('tipo')
    if tipo != 'PERMUTA' and tipo != 'CEDIDO':
        doe = request.POST.get('doe')
        parecer = request.POST.get('parecer')
        digito = request.POST.get('digito')
        convocacao = request.POST.get('convocacao')
        if convocacao == '':
            convocacao = None
        contratacao = request.POST.get('contratacao')
        if contratacao == '':
            contratacao = None
    cargo = request.POST.get('cargo')
    inicio = request.POST.get('inicio')
    termino = request.POST.get('termino')
    municipio = request.POST.get('municipio')
    situacao = request.POST.get('situacao')

    if tipo != 'ESTAGIÁRIO':
        cargo = Cargo.objects.get(id= cargo)
        municipio = Cidade.objects.get(id= municipio)

    if edicao:
        id_contrato = request.GET.get('id_contrato')
        contrato = Servidor_contrato.objects.filter(id= id_contrato)

        if tipo == 'ESTAGIÁRIO':
            inputs_contrato = {'numero_contrato': numero_contrato, 'tipo_contrato': tipo,  'data_inicio': inicio, 'data_termino': termino, 'situacao': situacao}
        elif tipo == 'PERMUTA' or tipo == 'CEDIDO':
            inputs_contrato = {'numero_contrato': numero_contrato, 'tipo_contrato': tipo, 'cargo': cargo.nome,  'data_inicio': inicio, 'data_termino': termino, 'municipio': municipio, 'situacao': situacao}
        else:
            inputs_contrato = {'numero_contrato': numero_contrato, 'doe': doe, 'parecer': parecer, 'digito': digito, 'tipo_contrato': tipo, 'cargo': cargo.nome, 'data_convocacao': convocacao,  'data_contrato': contratacao,  'data_inicio': inicio, 'data_termino': termino, 'municipio': municipio, 'situacao': situacao}

        modificacoes_contrato = dict_compare(contrato.values()[0], inputs_contrato)
        contrato = contrato[0]
    else:
        contrato = Servidor_contrato()
        modificacoes_contrato = None

    if tipo != 'ESTAGIÁRIO':
        contrato.servidor = servidor
        contrato.numero_contrato = numero_contrato
        if tipo != 'PERMUTA' and tipo != 'CEDIDO':
            contrato.doe = doe
            contrato.parecer = parecer
            contrato.digito = digito
            contrato.data_convocacao = convocacao
            contrato.data_contrato = contratacao
        contrato.tipo_contrato = tipo
        if tipo != 'EFETIVO':
            contrato.data_termino = termino
        contrato.cargo = cargo
        contrato.data_inicio = inicio
        contrato.municipio = municipio.nome
        contrato.situacao = situacao
        contrato.saldo = cargo.carga_horaria

        if 'PROFESSOR' in cargo.nome and tipo != 'PERMUTA' and tipo != 'CEDIDO':
            diario_homologacao = request.POST.get('diario-homologacao')
            id_disciplina = request.POST.get('disciplina-convocacao')

            if id_disciplina:
                disciplina_convocacao = Disciplinas.objects.get(id= id_disciplina)
            else:
                disciplina_convocacao = None

            contrato.disciplina_convocacao = disciplina_convocacao
            contrato.diario_homologacao = diario_homologacao

        contrato.ano_referencia = '2023'
        contrato.save()

    else:
        contrato.numero_contrato = numero_contrato
        contrato.servidor = servidor
        contrato.tipo_contrato = tipo
        contrato.data_inicio = inicio
        contrato.data_termino = termino
        contrato.situacao = situacao
        contrato.ano_referencia = '2023'
        contrato.save()

    salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato', modificacoes_contrato)

    return contrato

def formulario_ocorrencia(request, contrato, edicao, id_ocorrencia):
    #Variaveis para receber valor do Front
    data_inicio = None
    data_final = None
    portaria = None
    doe = None
    cid = None
    pad = None
    sei = None
    decreto = None
    data_falecimento = None
    ano_exercicio = None
    laudo_requisicao = None
    folha = None
    livro = None
    termo = None
    registro_obito = None
    data_expedicao = None
    sentenca = None
    ano_readequacao = None
    parecer = None
    observacao = None

    tipo_ocorrencia = request.POST.get('tipo_ocorrencia')
    observacao = request.POST.get('observacao')

    if tipo_ocorrencia == 'AFASTAMENTO PARA ACOMPANHAR O CÔNJUGE':
        data_inicio = request.POST.get('conjuge-data-inicio')
        data_final = request.POST.get('conjuge-data-final')
        portaria = request.POST.get('conjuge-portaria')
        inputs_banco = {'data_inicio': data_inicio, 'data_termino': data_final, 'portaria': portaria}

    elif tipo_ocorrencia == 'AFASTAMENTO PARA ESTUDO FORA DO ESTADO (COM ÔNUS)': 
        portaria = request.POST.get('estudo-portaria')
        data_inicio = request.POST.get('estudo-data-inicio')
        inputs_banco = {'portaria': portaria, 'data_inicio': data_inicio }

    elif tipo_ocorrencia == 'APOSENTADORIA':
        portaria = request.POST.get('aposentadoria-portaria')
        doe = request.POST.get('aposentadoria-doe')
        data_inicio = request.POST.get('aposentadoria-data-inicio')
        inputs_banco = {'portaria': portaria, 'doe': doe ,'data_inicio': data_inicio }

    elif tipo_ocorrencia == 'ATESTADO MEDICO':
        cid = request.POST.get('atestado-medico-cid')
        data_inicio = request.POST.get('atestado-medico-data-inicio')
        data_final = request.POST.get('atestado-medico-data-final')
        inputs_banco = {'cid':cid, 'data_inicio': data_inicio , 'data_inicio': data_final }

    elif tipo_ocorrencia == 'AUXÍLIO DOENÇA':
        data_inicio = request.POST.get('auxilio-doenca-data-inicio')
        data_final = request.POST.get('auxilio-doenca-data-final')
        sei = request.POST.get('auxilio-doenca-sei')
        inputs_banco = {'sei':sei, 'data_inicio': data_inicio , 'data_inicio': data_final }

    elif tipo_ocorrencia == 'CESSÃO COM ÔNUS':
        decreto = request.POST.get('cessao-com-onus-decreto')
        doe = request.POST.get('cessao-com-onus-doe')
        data_inicio = request.POST.get('cessao-com-onus-data-inicio')
        data_final = request.POST.get('cessao-com-onus-data-final')
        inputs_banco = {'decreto':decreto, 'doe':doe ,'data_inicio': data_inicio , 'data_inicio': data_final}

    elif tipo_ocorrencia == 'CESSÃO SEM ÔNUS':
        decreto = request.POST.get('cessao-sem-onus-decreto')
        doe = request.POST.get('cessao-sem-onus-doe')
        data_inicio = request.POST.get('cessao-sem-onus-data-inicio')
        data_final = request.POST.get('cessao-sem-onus-data-final')
        inputs_banco = {'decreto':decreto, 'doe':doe ,'data_inicio': data_inicio , 'data_inicio': data_final}
    
    elif tipo_ocorrencia == 'DEMISSÃO':
        pad = request.POST.get('demissao-pad')
        data_inicio = request.POST.get('demissao-data-inicio')
        inputs_banco = {'pad':pad, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'EXONERAÇÃO':
        decreto = request.POST.get('exoneracao-decreto')
        doe = request.POST.get('exoneracao-doe')
        data_inicio = request.POST.get('exoneracao-data-inicio')
        inputs_banco = {'decreto':decreto, 'doe':doe ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'EXONERAÇÃO A PEDIDO':
        decreto = request.POST.get('exoneracao-pedido-decreto')
        doe = request.POST.get('exoneracao-doe')
        data_inicio = request.POST.get('exoneracao-data-inicio')
        inputs_banco = {'decreto':decreto, 'doe':doe ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'FALECIMENTO':
        data_falecimento = request.POST.get('falecimento-data-falecimento')
        registro_obito = request.POST.get('falecimento-registro-obito')
        inputs_banco = {'data_falecimento': data_falecimento, 'registro_obito':registro_obito}

    elif tipo_ocorrencia == 'FÉRIAS':
        ano_exercicio = request.POST.get('ferias-ano-exercicio')
        data_inicio = request.POST.get('ferias-data-inicio')
        data_final = request.POST.get('ferias-data-final')
        inputs_banco = {'decreto':decreto, 'doe':doe ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LAUDO MÉDICO DEFINITIVO DE FUNÇÃO':
        laudo_requisicao = request.POST.get('laudo-definitivo-laudo')
        sei = request.POST.get('laudo-definitivo-sei')
        data_inicio = request.POST.get('laudo-definitivo-data-inicio')
        inputs_banco = {'laudo_requisicao':laudo_requisicao, 'sei':sei ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA ACOMPANHANTE':
        laudo_requisicao = request.POST.get('acompanhante-laudo')
        sei = request.POST.get('acompanhante-sei')
        data_inicio = request.POST.get('acompanhante-data-inicio')
        inputs_banco = {'laudo_requisicao':laudo_requisicao, 'sei':sei ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA ADOÇÃO':
        portaria = request.POST.get('adocao-portaria')
        parecer = request.POST.get('adocao-parecer')
        sei = request.POST.get('adocao-sei')
        data_inicio = request.POST.get('adocao-data-inicio')
        data_final = request.POST.get('adocao-data-final')
        inputs_banco = {'portaria':portaria,'parecer': parecer, 'sei':sei , 'data_inicio': data_inicio, 'data_final':data_final}

    elif tipo_ocorrencia == 'LICENÇA CASAMENTO':
        folha = request.POST.get('casamento-folha')
        livro = request.POST.get('casamento-livro')
        termo = request.POST.get('casamento-termo')
        data_expedicao = request.POST.get('casamento-expedicao')
        data_inicio = request.POST.get('casamento-data-inicio')
        data_final = request.POST.get('casamento-data-final')
        inputs_banco = {'laudo_requisicao':laudo_requisicao, 'sei':sei ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA MATERNIDADE':
        sei = request.POST.get('maternidade-sei')
        data_inicio = request.POST.get('maternidade-data-inicio')
        data_final = request.POST.get('maternidade-data-final')
        inputs_banco = {'sei':sei ,'data_inicio': data_inicio, 'data_final':data_final}

    elif tipo_ocorrencia == 'LICENÇA PARA ATIVIDADE POLITICA':
        parecer = request.POST.get('politica-parecer')
        portaria = request.POST.get('politica-portaria')
        data_inicio = request.POST.get('politica-data-inicio')
        inputs_banco = {'parecer':parecer , 'portaria':portaria ,'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PARA DESEMPENHO DE MANDATO CLASSISTA':
        data_inicio = request.POST.get('classista-data-inicio')
        data_final = request.POST.get('classista-data-final')
        inputs_banco = {'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PARA EXERCÍCIO DE MANDATO ELETIVO':
        data_inicio = request.POST.get('eletivo-data-inicio')
        data_final = request.POST.get('eletivo-data-final')
        inputs_banco = {'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PARA INTERESSE PARTICULAR (SEM ÔNUS)':
        parecer = request.POST.get('interesse-particular-parecer')
        sei = request.POST.get('interesse-particular-sei')
        data_inicio = request.POST.get('interesse-particular-data-inicio')
        data_final = request.POST.get('interesse-particular-data-final')
        inputs_banco = {'parecer':parecer,'sei':sei, 'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PARA MANDATO ELEITORAL':
        data_inicio = request.POST.get('mandato-data-inicio')
        data_final = request.POST.get('mandato-data-final')
        inputs_banco = {'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PARA TRATAMENTO DE SAÚDE':
        sei = request.POST.get('tratamento-saude-sei')
        laudo_requisicao = request.POST.get('tratamento-saude-laudo')
        data_inicio = request.POST.get('tratamento-saude-data-inicio')
        data_final = request.POST.get('tratamento-saude-data-final')
        inputs_banco = {'sei':sei,'laudo_requisacao':laudo_requisicao, 'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PATERNIDADE':
        sei = request.POST.get('paternidade-sei')
        data_inicio = request.POST.get('paternidade-data-inicio')
        data_final = request.POST.get('paternidade-data-final')
        inputs_banco = {'sei':sei, 'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'LICENÇA PRÊMIO':
        portaria = request.POST.get('premio-portaria')
        data_inicio = request.POST.get('premio-data-inicio')
        data_final = request.POST.get('premio-data-final')
        inputs_banco = {'portaria':portaria, 'data_final':data_final, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'READEQUAÇÃO - LEI NALUH':
        parecer = request.POST.get('readequacao-parecer')
        sei = request.POST.get('readequacao-sei')
        ano_readequacao = request.POST.get('readequacao-ano')
        inputs_banco = {'parecer':parecer,'sei':sei, 'ano_readequacao': ano_readequacao}

    elif tipo_ocorrencia == 'RECLUSÃO':
        portaria = request.POST.get('reclusao-portaria')
        sentenca = request.POST.get('reclusao-sentenca')
        data_inicio = request.POST.get('reclusao-data-inicio')
        inputs_banco = {'portaria':portaria,'sentenca':sentenca, 'data_inicio': data_inicio}

    elif tipo_ocorrencia == 'REDUÇÃO DE CARGA HORÁRIA':
        laudo_requisicao = request.POST.get('reducao-laudo')
        parecer = request.POST.get('reducao-parecer')
        sei = request.POST.get('reducao-sei')
        inputs_banco = {'laudo_requisicao':laudo_requisicao,'parecer':parecer, 'sei': sei}

    elif tipo_ocorrencia == 'LAUDO MÉDICO TEMPORÁRIO':
        laudo_requisicao = request.POST.get('laudo-temporario-laudo')
        sei = request.POST.get('laudo-temporario-sei')
        data_inicio = request.POST.get('laudo-temporario-data-inicio')
        data_final = request.POST.get('laudo-temporario-data-final')
        inputs_banco = {'laudo_requisicao':laudo_requisicao,'sei': sei, 'data_inicio': data_inicio, 'data_final':data_final }

    if edicao:
        #Edição de Ocorrencia Funcional 
        inputs_banco['observacao'] = observacao
        
        #Criação do objeto do banco para atualização
        edicao_ocorrecia = Servidor_ocorrencia_funcional.objects.filter(id=id_ocorrencia)

        #Objeto de identificação de alteração
        modificacoes_banco = dict_compare(edicao_ocorrecia.values()[0], inputs_banco)

        edicao_ocorrecia = edicao_ocorrecia[0]

        #Campos de Edição para atualização
        edicao_ocorrecia.tipo_ocorrencia = tipo_ocorrencia
        edicao_ocorrecia.data_inicio = data_inicio
        edicao_ocorrecia.data_termino = data_final
        edicao_ocorrecia.data_falecimento = data_falecimento
        edicao_ocorrecia.data_expedicao = data_expedicao
        edicao_ocorrecia.portaria = portaria
        edicao_ocorrecia.parecer = parecer
        edicao_ocorrecia.cid = cid
        edicao_ocorrecia.sei = sei
        edicao_ocorrecia.pad = pad
        edicao_ocorrecia.doe = doe
        edicao_ocorrecia.decreto = decreto 
        edicao_ocorrecia.ano_exercicio = ano_exercicio
        edicao_ocorrecia.laudo_requisicao = laudo_requisicao 
        edicao_ocorrecia.sentenca = sentenca
        edicao_ocorrecia.folha = folha
        edicao_ocorrecia.livro = livro
        edicao_ocorrecia.termo = termo
        edicao_ocorrecia.registro_obito = registro_obito
        edicao_ocorrecia.observacao = observacao
        edicao_ocorrecia.ano_readequacao = ano_readequacao

        edicao_ocorrecia.save()

        #Salvar historico 
        salvar_historico(request, edicao_ocorrecia, edicao, 'lotacao_servidor_ocorrencia_funcional', modificacoes_banco)
    else:
        #criação de Ocorrencia Funcional 
        ocorrencia = Servidor_ocorrencia_funcional()
        ocorrencia.contrato = contrato
        ocorrencia.tipo_ocorrencia = tipo_ocorrencia
        ocorrencia.data_inicio = data_inicio
        ocorrencia.data_termino = data_final
        ocorrencia.data_falecimento = data_falecimento
        ocorrencia.data_expedicao = data_expedicao
        ocorrencia.portaria = portaria
        ocorrencia.parecer = parecer
        ocorrencia.cid = cid
        ocorrencia.sei = sei
        ocorrencia.pad = pad
        ocorrencia.doe = doe
        ocorrencia.decreto = decreto
        ocorrencia.ano_exercicio = ano_exercicio
        ocorrencia.laudo_requisicao = laudo_requisicao
        ocorrencia.folha = folha
        ocorrencia.livro = livro
        ocorrencia.termo = termo
        ocorrencia.observacao = observacao
        ocorrencia.ano_readequacao = ano_readequacao
        ocorrencia.status = 1
        ocorrencia.save()

        salvar_historico(request, ocorrencia, edicao, 'lotacao_servidor_ocorrencia_funcional')

        if 'LICENÇA' in tipo_ocorrencia:
            situacao = 'LICENCIADO'
        elif 'AFASTAMENTO' in tipo_ocorrencia:
            situacao = 'AFASTADO'
        elif 'EXONERAÇÃO' in tipo_ocorrencia:
            situacao = 'EXONERADO/RESCISO'
        elif 'DEMISSÃO' in tipo_ocorrencia:
            situacao = 'EXONERADO/RESCISO'
        elif 'FALECIMENTO' in tipo_ocorrencia:
            situacao = 'FALECIDO'
        elif 'APOSENTADORIA' in tipo_ocorrencia:
            situacao = 'APOSENTADO'
        elif 'CESSÃO' in tipo_ocorrencia:
            situacao = 'CEDIDO'
        else:
            situacao = 'EM EXERCÍCIO'

        contrato.situacao = situacao
        contrato.save()
        salvar_historico(request, contrato, edicao, 'lotacao_servidor_contrato')
        
def formulario_cargo(request):
    edicao= False

    nome = request.POST.get('nome')
    classe = request.POST.get('classe')
    carga_horaria = request.POST.get('carga_horaria')
    nivel = request.POST.get('nivel')
    tipo = request.POST.get('tipo')
    atribuicao = request.POST.get('atribuicao')
    situacao = request.POST.get('situacao')

    cargo = Cargo()
    cargo.nome = nome
    cargo.classe = classe.upper()
    cargo.carga_horaria = carga_horaria
    cargo.saldo = carga_horaria
    cargo.nivel = nivel
    cargo.tipo = tipo
    cargo.atribuicao = atribuicao
    cargo.situacao = situacao
    cargo.save()
    salvar_historico(request, cargo, edicao, 'lotacao_cargo')

def formulario_complemento_hora(request, contrato):
    edicao = False

    carga_horaria = request.POST.get('carga_horaria')
    data_inicio = request.POST.get('data_inicio')
    data_final = request.POST.get('data_final')

    complemento = Servidor_hora_complementar()

    complemento.contrato = contrato
    complemento.carga_horaria = carga_horaria
    complemento.data_inicio = data_inicio
    complemento.data_termino = data_final
    complemento.status = 1
    complemento.save()
    salvar_historico(request, complemento, edicao, 'lotacao_servidor_complemento_funcional')

    carga_cargo = int(contrato.cargo.carga_horaria)
    saldo_atual = int(contrato.saldo)
    contrato.saldo = saldo_atual + int(carga_horaria)
    contrato.save()

def formulario_gratificacao(request, contrato):
    edicao = False

    porcentagem = request.POST.get('porcentagem')
    data_inicio = request.POST.get('data_inicio')
    data_final = request.POST.get('data_final')

    gratificacao = Servidor_gratificacao()

    gratificacao.contrato = contrato
    gratificacao.porcentagem = porcentagem
    gratificacao.data_inicio = data_inicio
    gratificacao.data_termino = data_final
    gratificacao.status = 1
    gratificacao.save()
    salvar_historico(request, gratificacao, edicao, 'lotacao_servidor_gratificacao')

def contrato_finalizar(request, id_contrato, lotacao):
    edicao = False

    data_finalizacao = request.POST.get('data_finalizacao')
    motivo = request.POST.get('motivo')
    if lotacao.funcao in ['Diretor(a) Escolar', 'Coordenador(a) Administrativo de Escolas', 'Coordenador(a) de Ensino Escolar', 'Secretário(a) Escolar']:
        destituicao = request.POST.get('portaria-destituicao')
        doe_destituicao = request.POST.get('doe-portaria-destituicao')
    if id_contrato:
        lotacao = Servidor_lotacao.objects.filter(contrato= id_contrato).last()
    elif lotacao.funcao == "Professor(a)" and lotacao.unidade_adm:
        professor_adm= Grade_professor_adm.objects.get(professor= lotacao.id, status=1)
        professor_adm.status = 0
        professor_adm.save()
    else:
        lotacao = lotacao

        for grade in Grade.objects.filter(professor= lotacao.id):
            grade.status = 0
            grade.save()

        for item in Professor_aluno.objects.filter(professor= lotacao.id):
            item.status = 0
            item.save()

    lotacao.motivo = motivo
    lotacao.data_termino = data_finalizacao
    if lotacao.funcao in ['Diretor(a) Escolar', 'Coordenador(a) Administrativo de Escolas', 'Coordenador(a) de Ensino Escolar', 'Secretário(a) Escolar']:
        lotacao.doe_destituicao = doe_destituicao
        lotacao.destituicao = destituicao
    lotacao.status = 0
    lotacao.save()
    salvar_historico(request, lotacao, edicao, 'lotacao_servidor_contrato')

def lotacao_excluir(request, id_lotacao):
    assinatura = Lotacao_assinatura.objects.filter(lotacao = id_lotacao)
    if assinatura != None:
        assinatura.delete()
    grade = Grade.objects.filter(professor = id_lotacao)
    if grade != None:
        grade.delete()
    professor_aluno = Professor_aluno.objects.filter(professor = id_lotacao)
    if professor_aluno != None:
        professor_aluno.delete()
    professor_adm = Grade_professor_adm.objects.filter(professor = id_lotacao)
    if professor_adm != None:
        professor_adm.delete()
    servidor_lotacao = Servidor_lotacao.objects.filter(id = id_lotacao)
    if servidor_lotacao != None:
        servidor_lotacao.delete()

def formulario_aditivo(request, contrato):
    edicao = False

    data_inicio = request.POST.get('data_inicio')
    data_final = request.POST.get('data_final')

    aditivo = Servidor_contrato_aditivo()
    aditivo.contrato = contrato
    aditivo.data_inicio = data_inicio
    aditivo.data_termino = data_final
    aditivo.status = 1
    aditivo.save()
    salvar_historico(request, aditivo, edicao, 'lotacao_servidor_gratificacao')

def formulario_vdp(request, contrato):
    edicao = False

    ano_periodo = request.POST.get('ano_periodo')
    ano_verificacao = request.POST.get('ano_verificacao')
    valor_bruto = request.POST.get('valor_bruto')
    valor_liquido = request.POST.get('valor_liquido')

    valor_bruto = (valor_bruto.replace('R$', '').strip().replace('.', '').replace(',', '.'))
    valor_liquido = (valor_liquido.replace('R$', '').strip().replace('.', '').replace(',', '.'))

    vdp = Servidor_vdp()
    vdp.contrato = contrato
    vdp.ano_periodo = ano_periodo
    vdp.ano_verificacao = ano_verificacao
    vdp.valor_bruto = valor_bruto
    vdp.valor_liquido = valor_liquido
    vdp.status = 1
    vdp.save()
    salvar_historico(request, vdp, edicao, 'lotacao_servidor_vdp')

def cancelamento_contrato(request, contrato):
    edicao = False
    termo = request.FILES.get('termo')

    versao = Contrato_cancelamento.objects.filter(contrato_id= contrato).count() + 1
    if versao > 1:
        nome = f'Documento({versao}).' + str(termo).split('.')[-1]
    else:
        nome = 'Documento.' + str(termo).split('.')[-1]

    if not Contrato_cancelamento.objects.filter(contrato= contrato).exists():
        cancelamento = Contrato_cancelamento()
        cancelamento.contrato = contrato
        cancelamento.documento = handle_uploaded_file(termo, nome, 'Contrato', '/Cancelamento')
        cancelamento.save()
        salvar_historico(request, cancelamento, edicao, 'lotacao_contrato_cancelamento')

        situacao = Servidor_contrato.objects.get(id= contrato.id)
        situacao.situacao = 'EXONERADO/RESCISO'
        situacao.save()
        salvar_historico(request, cancelamento, True, 'lotacao_servidor_contrato')

def excluir_contrato(request, id_contrato):
    contrato = Servidor_contrato.objects.get(id= id_contrato)
    contrato.delete()

def excluir_contrato_aditivo(request, id_aditivo):
    aditivo = Servidor_contrato_aditivo.objects.get(id= id_aditivo)
    aditivo.delete()
