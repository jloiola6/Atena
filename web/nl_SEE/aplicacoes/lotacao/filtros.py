# from django.core.paginator import Paginator
from itertools import chain
from logging.config import IDENTIFIER
from django.db.models import Q

from .models import *
from aplicacoes.core.models import *
from aplicacoes.administracao.models import Grade
from aplicacoes.lotacao.models import *

import re
from datetime import *

def filtro_vdp(request):
    vdp = Servidor_vdp.objects.all()
    ano = request.GET.get('ano')

    if ano == "2022":
        vdp = Servidor_vdp.objects.filter( ano_periodo = "2022")
    elif ano == "2023":
        vdp = Servidor_vdp.objects.filter( ano_periodo = "2023")

    digito = request.GET.get('digito')
    nome = request.GET.get('nome')

    if digito != None and digito != '':
        vdp = vdp.filter(contrato__digito= digito)

    elif nome != None and nome != '':
        if vdp.filter(contrato__servidor__nome__icontains= nome).count() > 0:
            vdp = vdp.filter(contrato__servidor__nome__icontains= nome)
        else:
            vdp = vdp.filter(contrato__servidor__nome__icontains= nome.upper())

    return vdp

def filtro_servidores(request):
    servidores = Servidor.objects.all().values('id', 'matricula', 'nome', 'cpf', 'situacao').order_by('nome')
    cpf = request.GET.get('cpf')
    matricula = request.GET.get('matricula')
    nome = request.GET.get('nome')

    #Filtro pelo CPF
    if cpf != None and cpf != '':
        cpf = re.sub('\D', '', cpf)
        servidores = servidores.filter(cpf= cpf)

    #Filtro pelo Nome
    elif matricula != None and matricula != '':
        servidores = servidores.filter(matricula= matricula)

    #Filtro pelo Nome
    elif nome != None and nome != '':
        if servidores.filter(nome__icontains= nome).count() > 0:
            servidores = servidores.filter(nome__icontains= nome)
        else:
            servidores = servidores.filter(nome__icontains= nome.upper())

    return servidores

# def filtro_lotacao(request, banco, name_unidade_adm, name_unidade_educacional, name_cargos, name_funcoes):
def filtro_lotacao(request):
    verificacao = False

    # Pesquisa na tabela lotação com lotações ativas
    lotacao = Servidor_lotacao.objects.filter(status= 1).values('id', 'unidade_escolar__municipio', 'unidade_adm__endereco__municipio', 'subconta__sub', 'contrato__tipo_contrato', 'data_inicio', 'contrato__digito', 'contrato__cargo__nome', 'contrato__servidor__matricula', 'contrato__servidor__cpf', 'contrato__servidor__nome','funcao','unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'unidade_escolar__escola__nome_escola', 'carga_horaria','contrato__municipio', 'contrato__servidor__id', 'unidade_escolar__regiao', 'unidade_escolar__escola__cod_inep', 'subconta__fonte', 'contrato__data_contrato', 'contrato__doe', 'tipo_lotacao', 'contrato').order_by('unidade_escolar__municipio', 'unidade_adm__endereco__municipio', 'unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'contrato__servidor__nome')

    # Pesquisa na tabela lotação com lotações ativas e que são tipo Cedido, Permuta, Sem lotação
    lotacao2 = Servidor_lotacao.objects.filter(status= 1, tipo_lotacao__in=['Cedido', 'Permuta', 'Sem Lotação']).values('id', 'unidade_escolar__municipio', 'unidade_adm__endereco__municipio', 'subconta__sub', 'contrato__tipo_contrato', 'data_inicio', 'contrato__digito', 'contrato__cargo__nome', 'contrato__servidor__matricula', 'contrato__servidor__cpf', 'contrato__servidor__nome','funcao','unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'unidade_escolar__escola__nome_escola', 'carga_horaria','contrato__municipio', 'contrato__servidor__id', 'unidade_escolar__regiao', 'unidade_escolar__escola__cod_inep', 'subconta__fonte', 'contrato__data_contrato', 'contrato__doe', 'tipo_lotacao', 'contrato').order_by('unidade_escolar__municipio', 'unidade_adm__endereco__municipio', 'unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'contrato__servidor__nome')

    # Capturando url do requisição
    get = request.build_absolute_uri()

    # Filtrando de acordo com os inputs da página e modal
    if '=on' not in get:
        data_final= request.GET.get('data-final')
        cpf = request.GET.get('cpf')
        data = request.GET.get('data')
        matricula = request.GET.get('matricula')
        nome = request.GET.get('nome')
        cargo = request.GET.get('cargo')
        funcao = request.GET.get('funcao')
        administrativa = request.GET.get('administrativa')
        educacional = request.GET.get('educacional')
        municipio = request.GET.get('municipio')
        regional = request.GET.get('regiao')
        subconta = request.GET.get('subconta')
        tipo_lotacao = request.GET.get('tipo')

        if cpf != None and cpf != '':
            cpf = re.sub('\D', '', cpf)
            lotacao = lotacao.filter(contrato__servidor__cpf= cpf)
            verificacao = True

        if matricula != None and matricula != '':
            lotacao = lotacao.filter(contrato__servidor__matricula= matricula)
            verificacao = True

        if nome != None and nome != '':
            lotacao = lotacao.filter(contrato__servidor__nome__icontains= nome)
            verificacao = True

        if cargo != None and cargo != '':
            lotacao = lotacao.filter(contrato__cargo__nome__icontains = cargo)
            verificacao = True

        if funcao != None and funcao != '':
            lotacao = lotacao.filter(funcao__icontains = funcao)
            verificacao = True

        if administrativa != None and administrativa != '':
            lotacao = lotacao.filter(unidade_adm__id= administrativa)
            verificacao = True

        if educacional != None and educacional != '':
            lotacao = lotacao.filter(unidade_escolar__escola__id= educacional)
            verificacao = True

        if municipio != None and municipio != '':
            lotacao = lotacao.filter(unidade_escolar__municipio__icontains = municipio)
            verificacao = True

        if regional != None and regional != '':
            lotacao = lotacao.filter(unidade_escolar__regiao__icontains = regional)
            verificacao = True

        if subconta != None and subconta != '':
            lotacao = lotacao.filter(subconta__id = subconta)
            verificacao = True

        if tipo_lotacao != None and tipo_lotacao != '':
            lotacao = lotacao.filter(tipo_lotacao__icontains = tipo_lotacao)
            verificacao = True

        if data != None and data  != '':
            lotacao = lotacao.filter(data_inicio__range=(data, data_final))
            verificacao = True
    else:
        # Filtrando de acordo com os dados vindo da url
        get = get.split('?')[1]

        id_regional = []
        for name in get.split('&'):
            if 'regional' in name:
                valor = name.split('regional-')[1]
                id = str(valor.split('=')[0]).replace('+', ' ')
                id_regional.append(id)
        if len(id_regional):
            for aux in range(len(id_regional)):
                id_regional[aux] = manipulacaoStr(id_regional[aux])
            lotacao = lotacao.filter(Q(unidade_adm__endereco__regiao__in= id_regional) | Q(unidade_escolar__regiao__in= id_regional))
            verificacao = True

        id_municipio = []
        for name in get.split('&'):
            if 'municipio' in name:
                valor = name.split('municipio-')[1]
                id = valor.split('=')[0].replace('+', ' ')
                id_municipio.append(id)
        if len(id_municipio):
            for aux in range(len(id_municipio)):
                id_municipio[aux] = manipulacaoStr(id_municipio[aux])
            lotacao = lotacao.filter(Q(unidade_adm__endereco__municipio__in= id_municipio) | Q(unidade_escolar__municipio__in= id_municipio))
            verificacao = True

        id_escolar = []
        for name in get.split('&'):
            if 'escolar' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_escolar.append(id)
        if len(id_escolar):
            lotacao = lotacao.filter(unidade_escolar__escola__id__in= id_escolar)
            verificacao = True

        id_adm = []
        for name in get.split('&'):
            if 'adm' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_adm.append(id)
        if len(id_adm):
            lotacao = lotacao.filter(unidade_adm__id__in= id_adm)
            verificacao = True

        id_cargos = []
        for name in get.split('&'):
            if 'cargo' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_cargos.append(id)
        if len(id_cargos):
            lotacao = lotacao.filter(contrato__cargo__id__in= id_cargos)
            verificacao = True

        id_subs = []
        for name in get.split('&'):
            if 'subconta' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_subs.append(id)
        if len(id_subs):
            lotacao = lotacao.filter(subconta__id__in= id_subs)
            verificacao = True

        id_funcao = []
        for name in get.split('&'):
            if 'funcao' in name:
                valor = name.split('funcao-')[1]
                id = valor.split('=')[0].replace('+', ' ')
                id_funcao.append(id)
        if len(id_funcao):
            for aux in range(len(id_funcao)):
                id_funcao[aux] = manipulacaoStr(id_funcao[aux])
            lotacao = lotacao.filter(funcao__in= id_funcao)
            verificacao = True

        id_disciplinas = []
        for name in get.split('&'):
            if 'disciplina' in name:
                valor = name.split('-')[1]
                id = valor.split('=')[0].replace('+', ' ')
                id_disciplinas.append(id)
        if len(id_disciplinas):
            for aux in range(len(id_disciplinas)):
                id_disciplinas[aux] = manipulacaoStr(id_disciplinas[aux])
            id_lotacoes = Grade.objects.filter(disciplina__nome__in= id_disciplinas).exclude(status= 0).values_list('professor', flat= True)
            lotacao = lotacao.filter(id__in= id_lotacoes)
            verificacao = True

        id_etapa = []
        for name in get.split('&'):
            if 'etapa' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_etapa.append(id)
        if len(id_etapa):
            id_lotacoes = Grade.objects.filter(turma__etapa__in= id_etapa).values_list('professor', flat= True)
            lotacao = lotacao.filter(id__in= id_lotacoes)
            verificacao = True

        id_tipos = []
        for name in get.split('&'):
            if 'tipo' in name:
                valor = name.split('tipo-')[1]
                id = valor.split('=')[0].replace('+', ' ')
                id_tipos.append(id)
        if len(id_tipos):
            for aux in range(len(id_tipos)):
                id_tipos[aux] = manipulacaoStr(id_tipos[aux])
            lotacao = lotacao.filter(tipo_lotacao__in= id_tipos)
            verificacao = True

    if not verificacao:
        lotacao = list(chain(lotacao.exclude(tipo_lotacao = 'Cedido').exclude(tipo_lotacao = 'Permuta').exclude(tipo_lotacao = 'Sem Lotação'), lotacao2))
    return lotacao

def manipulacaoStr(var1):
    var1 = var1.replace('%28', '(').replace('%29', ')').replace('%C3%A9', 'é').replace('%C3%A3', 'ã').replace('%C3%BA', 'ú').replace('%C3%87', 'Ç').replace('%C3%89', 'É').replace('%C3%83', 'Ã').replace('%C2%BA', '°').replace('%2F', '/').replace('%2C', ',').replace('%C3%A7', 'ç').replace('%C3%93', 'Ó').replace('%C3%A1', 'á').replace('%C3%9A', 'Ú').replace('%C3%B3', 'ó').replace('%C3%AD', 'í')

    return var1

def filtro_contrato(request):
    get = request.build_absolute_uri()
    if 'situacao=EXONERADO%2FRESCISO' in get:
        contratos = Servidor_contrato.objects.filter().order_by('servidor__nome')
    else:
        contratos = Servidor_contrato.objects.filter().exclude(situacao__in = ['EXONERADO/RESCISO', 'EXONERADO']).order_by('servidor__nome')
    lista = []
    lista2 = []
    if 'tipo-=on' in get:
        for i in contratos:
            if i.parecer == None or i.parecer == 'None' or i.parecer == '00' or i.parecer == '00000000000000000' or i.doe:
                lista.append(i.id)
        contratos = contratos.exclude(id__in = lista)
        contratos = contratos.exclude(situacao__in =  ['EXONERADO/RESCISO', 'EXONERADO'])
        contratos = contratos.exclude(parecer__in=['123', '12', '1', '0000', '00000', '0', 'x', '', ' ', '000000000000', 'READEQUACAO ATRAVES DE JURIDICO', '13291', '234324', '00217453236', '13139', '12504', '12521', '12549', 'EDITAL  024/SEPLAG/SEE/ESPECIAL DE 24 /05/2022', 'EDITAL  013/SEPLAG/SEE/ESPECIAL DE 23/05/2022', '13348', '378', '3', '13316', '12919', '13241', '2011-P 28/01/2022', 'CEC-1 - LC355/18 DIRETA'])
        contratos = contratos.filter(parecer__isnull = False)

        for i in contratos:
            lista2.append(i.parecer)
        print(lista2)
    if '=on' not in get:
        cpf = request.GET.get('cpf')
        matricula = request.GET.get('matricula')
        nome = request.GET.get('nome')
        cargo = request.GET.get('cargo')
        carga_horaria = request.GET.get('carga_horaria')
        tipo_contrato = request.GET.get('tipo_contrato')
        situacao = request.GET.get('situacao')
        municipio = request.GET.get('municipio')

        #Filtro pelo CPF
        if cpf != None and cpf != '':
            cpf = re.sub('\D', '', cpf)
            contratos = contratos.filter(servidor__cpf= cpf)

        #Filtro pelo matricula
        elif matricula != None and matricula != '':
            contratos = contratos.filter(servidor__matricula= matricula)

        #Filtro pelo Nome
        elif nome != None and nome != '':
            if contratos.filter(servidor__nome__icontains= nome).count() > 0:
                contratos = contratos.filter(servidor__nome__icontains= nome)
            else:
                contratos = contratos.filter(servidor__nome__icontains= nome.upper())

        if cargo != None and cargo != '':
            contratos = contratos.filter(cargo__nome= cargo)

        if carga_horaria != None and carga_horaria != '':
            contratos = contratos.filter(cargo__carga_horaria= carga_horaria)

        if tipo_contrato != None and tipo_contrato != '':
            if tipo_contrato == 'PARECER':
                for i in contratos:
                    if i.parecer == None or i.parecer == 'None' or i.parecer == '00' or i.parecer == '00000000000000000' or i.doe:
                        lista.append(i.id)
                contratos = contratos.filter(parecer__isnull = False).exclude(id__in = lista).exclude(parecer__in=['123', '12', '1', '0000', '00000', '0', 'x', '', ' ', '000000000000', 'READEQUACAO ATRAVES DE JURIDICO', '13291', '234324', '00217453236', '13139', '12504', '12521', '12549', 'EDITAL  024/SEPLAG/SEE/ESPECIAL DE 24 /05/2022', 'EDITAL  013/SEPLAG/SEE/ESPECIAL DE 23/05/2022', '13348', '378', '3', '13316', '12919', '13241', '2011-P 28/01/2022', 'CEC-1 - LC355/18 DIRETA'])
            else:
                contratos = contratos.filter(tipo_contrato= tipo_contrato)

        if situacao != None and situacao != '':
            contratos = contratos.filter(situacao= situacao)

        if municipio != None and municipio != '':
            contratos = contratos.filter(municipio= municipio)

    else:
        get = get.split('?')[1]

        id_cargos = []
        for name in get.split('&'):
            if 'cargo' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_cargos.append(id)
        if len(id_cargos):
            contratos = contratos.filter(cargo__id__in= id_cargos)

        # cargas = []
        # for name in get.split('&'):
        #     if 'carga' in name:
        #         valor = name.split('-')[1]
        #         id = valor.split('=')[0]
        #         cargas.append(id)
        # if len(cargas):
        #     contratos = contratos.filter(cargo__carga_horaria__in= cargas)

        tipos = []
        for name in get.split('&'):
            if 'tipo' in name:
                valor = name.split('-')[1]
                id = valor.split('=')[0].replace('%C3%81', 'Á').replace('%C3%83','Ã')
                tipos.append(id)
        if len(tipos):
            if id == 'PARECER':
                for i in contratos:
                    if i.parecer == None or i.parecer == 'None' or i.parecer == '00' or i.parecer == '00000000000000000' or i.doe:
                        lista.append(i.id)
                contratos = contratos.filter(parecer__isnull = False).exclude(id__in = lista).exclude(parecer__in=['123', '12', '1', '0000', '00000', '0', 'x', '', ' ', '000000000000', 'READEQUACAO ATRAVES DE JURIDICO', '13291', '234324', '00217453236', '13139', '12504', '12521', '12549', 'EDITAL  024/SEPLAG/SEE/ESPECIAL DE 24 /05/2022', 'EDITAL  013/SEPLAG/SEE/ESPECIAL DE 23/05/2022', '13348', '378', '3', '13316', '12919', '13241', '2011-P 28/01/2022', 'CEC-1 - LC355/18 DIRETA'])
            else:
                contratos = contratos.filter(cargo__tipo__in= tipos)

        id_disciplina = []
        for name in get.split('&'):
            if 'disciplina_convocacao' in name:
                valor = name.split('-')[1]
                id = int(valor.split('=')[0])
                id_disciplina.append(id)
        if len(id_disciplina):
            contratos = contratos.filter(disciplina_convocacao__id__in= id_disciplina)

        diario_homologacao = []
        for name in get.split('&'):
            if 'diario_homologacao' in name:
                valor = name.split('-')[1]
                id = valor.split('=')[0]
                diario_homologacao.append(id)
        if len(diario_homologacao):
            contratos = contratos.filter(diario_homologacao__in= diario_homologacao)

        situacoes = []
        for name in get.split('&'):
            if 'situacao' in name:
                valor = name.split('-')[1]
                id = valor.split('=')[0].replace('+', ' ').replace('%C3%8D','Í').replace("%2F", '/')
                # if id == 'None':
                #     id = None
                situacoes.append(id)
        if len(situacoes):
            contratos = contratos.filter(situacao__in= situacoes)

        municipios = []
        for name in get.split('&'):
            if 'municipio' in name:
                valor = name.split('-')[1]
                id = valor.split('=')[0].replace('+', ' ').replace('%C3%A2', 'â').replace('%C3%A3', 'ã').replace('%C3%B3', 'ó').replace('%C3%A9', 'é').replace('%C3%A1', 'á')
                municipios.append(id)
        if len(municipios):
            contratos = contratos.filter(municipio__in= municipios)

    return contratos

def filtro_registro(request):
    lotacao = Servidor_lotacao.objects.filter().values('id', 'contrato__servidor__nome', 'unidade_adm__endereco__municipio', 'unidade_escolar__municipio', 'unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'numero_memorando').order_by('-id')

    tecnico = request.GET.get('tecnico')
    municipio = request.GET.get('municipio')
    data = request.GET.get('data')
    data_final = request.GET.get('data-final')

    if tecnico != None and tecnico != '':
        registros_id = Historico.objects.filter(tabela= 'lotacao_servidor_lotacao', log__usuario__id= tecnico).values_list('objeto', flat= True)
        lotacao = lotacao.filter(id__in= registros_id)

    if municipio != None and municipio != '':
        lotacao = lotacao.filter(Q(unidade_adm__endereco__municipio= municipio) | Q(unidade_escolar__municipio= municipio))

    if data != None and data != '' and data_final != None and data_final != '':
        lotacao = lotacao.filter(data_memorando__range=(data, data_final))

    return lotacao

def filtro_registro_contrato(request):

    contrato = Servidor_contrato.objects.filter().values('id', 'servidor__nome', 'municipio', 'numero_contrato', 'cargo__nome').order_by('-id')
    tecnico = request.GET.get('tecnico')
    # print(tecnico)
    municipio = request.GET.get('municipio')
    # data = request.GET.get('data')
    # data= data.split('-')
    # data= data[2]+'-'+data[1]+'-'+data[0]

    data = request.GET.get('data')
    if data != None and data != '':
        data= data.split('-')
        data= data[2]+'/'+data[1]+'/'+data[0]

    if municipio != None and municipio != '':
        contrato = contrato.filter(municipio= municipio)

    if tecnico != None and tecnico != '':
        registros_id = Historico.objects.filter(tabela= 'lotacao_servidor_contrato', log__usuario__id= tecnico).values_list('objeto', flat= True)
        contrato = contrato.filter(id__in= registros_id)

    if data != None and data != '':
        contrato_id = Historico.objects.filter(tabela= 'lotacao_servidor_contrato', data__contains=(data)).values_list('objeto', flat= True)
        contrato = contrato.filter(id__in= contrato_id)
    return contrato

def filtro_agendamento(request):
    data1 = date.today()
    if '?' not in request.build_absolute_uri() or len(str(request.build_absolute_uri()).split('?')[-1]) == 6 or len(str(request.build_absolute_uri()).split('?')[-1]) == 7:
        agendamento = Agendamento.objects.filter(data__gte = data1, status = 0).order_by('data', 'hora_atendimento')

    elif 'servidor=&servico=&data=' == request.build_absolute_uri().split('?')[-1]:
        agendamento = Agendamento.objects.filter(data__gte = data1, status = 0).order_by('data', 'hora_atendimento')

    else:
        agendamento = Agendamento.objects.all().order_by('data', 'hora_atendimento')
    atendente = request.GET.get('atendente')
    servidor = request.GET.get('servidor')
    servico = request.GET.get('servico')
    data = request.GET.get('data')
    status_ausente = request.GET.get('status-ausente')
    status_concluido = request.GET.get('status-concluido')
    status_cancelado = request.GET.get('status-cancelado')
    status_pendente = request.GET.get('status-pendente')
    status = [status_ausente, status_concluido, status_pendente, status_cancelado]

    if servidor != None and servidor.strip() != '':
        agendamento = agendamento.filter(servidor__id= servidor)

    if servico != None and servico.strip() != '':
        agendamento = agendamento.filter(atendimento__servico= servico)

    if data != None and data != '':
        agendamento = agendamento.filter(data__contains= (data))

    if status != [None, None, None, None] and status != '':
        agendamento = agendamento.filter(status__in= status)

    if atendente != None and atendente != '':
        agendamento = agendamento.filter(atendimento__atendente__nome= atendente)


    return agendamento

def filtro_autorizacao(request):
    get = request.build_absolute_uri()
    lotacoes = Servidor_lotacao.objects.filter(status= 2).values('id', 'data_memorando', 'data_inicio', 'data_termino', 'tipo_lotacao', 'orgao_cedido', 'contrato__cargo__nome', 'numero_memorando','carga_horaria', 'contrato__doe', 'contrato__cargo__nome', 'contrato__servidor__matricula', 'contrato__digito', 'contrato__servidor__nome', 'funcao', 'unidade_escolar__municipio', 'unidade_escolar__escola__nome_escola', 'unidade_escolar__escola__cod_turmalina', 'unidade_adm__nome', 'unidade_escolar', 'unidade_adm_id', 'unidade_adm__sigla', 'contrato__municipio', 'unidade_adm__endereco__municipio', 'subconta__fonte', 'observacoes', 'turno_manha', 'turno_tarde', 'turno_noite', 'subconta__sub', 'ano_referencia', 'orgao_origem').exclude(tipo_lotacao__in=['Complementação Salarial', 'Aula Complementar','Dedicação Exclusiva'])

    if '=on' not in get:
        cpf = request.GET.get('cpf')
        matricula = request.GET.get('matricula')
        nome = request.GET.get('nome')
        unidade_escolar = request.GET.get('unidade-escolar')
        unidade_adm = request.GET.get('unidade-adm')
        municipio = request.GET.get('municipio')
        tecnico = request.GET.get('tecnico')
        #Filtro pelo CPF
        if cpf != None and cpf != '':
            cpf = re.sub('\D', '', cpf)
            lotacoes = lotacoes.filter(contrato__servidor__cpf= cpf)

        #Filtro pelo matricula
        if matricula != None and matricula != '':
            lotacoes = lotacoes.filter(contrato__servidor__matricula= matricula)

        #Filtro pelo Nome
        if nome != None and nome != '':
            if lotacoes.filter(contrato__servidor__nome__icontains= nome).count() > 0:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome)
            else:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome.upper())

        #Filtros Avançados
        if unidade_escolar != None and unidade_escolar != '':
            lotacoes = lotacoes.filter(unidade_escolar__escola__nome_escola = unidade_escolar)

        if unidade_adm != None and unidade_adm != '':
            lotacoes = lotacoes.filter(unidade_adm__nome = unidade_adm)

        if municipio != None and municipio != '':
            lotacoes = lotacoes.filter(Q(unidade_adm__endereco__municipio = municipio) | Q(unidade_escolar__municipio = municipio))

        if tecnico != None and tecnico != '':
            ids_tecnico = Lotacao_assinatura.objects.filter(tecnico = tecnico).values_list('lotacao_id')
            lotacoes = lotacoes.filter(id__in = ids_tecnico)
            # lotacoes = lotacoes.filter(contrato__municipio = tecnico)

    return lotacoes

def filtro_tecnico(request, lotacoes_historico):
    get = request.build_absolute_uri()
    lotacoes = Servidor_lotacao.objects.filter(id__in= lotacoes_historico).order_by('-status')

    if '=on' not in get:
        cpf = request.GET.get('cpf')
        matricula = request.GET.get('matricula')
        nome = request.GET.get('nome')

        #Filtro pelo CPF
        if cpf != None and cpf != '':
            cpf = re.sub('\D', '', cpf)
            lotacoes = lotacoes.filter(contrato__servidor__cpf= cpf)

        #Filtro pelo matricula
        elif matricula != None and matricula != '':
            lotacoes = lotacoes.filter(contrato__servidor__matricula= matricula)

        #Filtro pelo Nome
        elif nome != None and nome != '':
            if lotacoes.filter(contrato__servidor__nome__icontains= nome).count() > 0:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome)
            else:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome.upper())

    return lotacoes

def filtro_folha(request):
    servidores = Servidor_contrato.objects.filter(situacao = 'EM EXERCÍCIO').values('id', 'digito', 'tipo_contrato', 'municipio', 'cargo_id', 'cargo__vencimento', 'cargo__nome', 'cargo__carga_horaria', 'cargo__classe', 'cargo__tipo', 'servidor__id', 'servidor__nome', 'servidor__matricula', 'servidor__cpf').order_by('servidor__nome')

    return servidores

def filtro_autorizacao_verbas(request):
    get = request.build_absolute_uri()
    lotacoes = Servidor_lotacao.objects.filter(tipo_lotacao__in=['Complementação Salarial', 'Aula Complementar','Dedicação Exclusiva'],status= 2).values('id', 'data_memorando', 'data_inicio', 'data_termino', 'tipo_lotacao', 'contrato__cargo__nome', 'numero_memorando','carga_horaria', 'contrato__doe', 'contrato__cargo__nome', 'contrato__servidor__matricula', 'contrato__digito', 'contrato__servidor__nome', 'funcao', 'unidade_escolar__municipio', 'unidade_escolar__escola__nome_escola', 'unidade_escolar__escola__cod_turmalina', 'unidade_adm__nome', 'unidade_escolar', 'unidade_adm_id', 'unidade_adm__sigla', 'contrato__municipio', 'unidade_adm__endereco__municipio', 'subconta__fonte', 'observacoes', 'turno_manha', 'turno_tarde', 'turno_noite', 'subconta__sub')

    if '=on' not in get:
        cpf = request.GET.get('cpf')
        matricula = request.GET.get('matricula')
        nome = request.GET.get('nome')
        unidade_escolar = request.GET.get('unidade-escolar')
        unidade_adm = request.GET.get('unidade-adm')
        municipio = request.GET.get('municipio')
        tecnico = request.GET.get('tecnico')
        #Filtro pelo CPF
        if cpf != None and cpf != '':
            cpf = re.sub('\D', '', cpf)
            lotacoes = lotacoes.filter(contrato__servidor__cpf= cpf)

        #Filtro pelo matricula
        if matricula != None and matricula != '':
            lotacoes = lotacoes.filter(contrato__servidor__matricula= matricula)

        #Filtro pelo Nome
        if nome != None and nome != '':
            if lotacoes.filter(contrato__servidor__nome__icontains= nome).count() > 0:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome)
            else:
                lotacoes = lotacoes.filter(contrato__servidor__nome__icontains= nome.upper())

        #Filtros Avançados
        if unidade_escolar != None and unidade_escolar != '':
            lotacoes = lotacoes.filter(unidade_escolar__escola__nome_escola = unidade_escolar)

        if unidade_adm != None and unidade_adm != '':
            lotacoes = lotacoes.filter(unidade_adm__nome = unidade_adm)

        if municipio != None and municipio != '':
            lotacoes = lotacoes.filter(Q(unidade_adm__endereco__municipio = municipio) | Q(unidade_escolar__municipio = municipio))

        if tecnico != None and tecnico != '':
            ids_tecnico = Lotacao_assinatura.objects.filter(tecnico = tecnico).values_list('lotacao_id')
            lotacoes = lotacoes.filter(id__in = ids_tecnico)
            # lotacoes = lotacoes.filter(contrato__municipio = tecnico)

    return lotacoes

def filtro_lista_espera(request):
    
    agenda = Agendamento.objects.filter(status = 4).values('id', 'servidor__nome', 'atendimento__servico__nome', 'atendimento__atendente__nome', 'contato', 'atendimento__id', 'atendimento__servico__id', 'servidor__id')

    if request.GET.get('servidor'):
        agenda = agenda.filter(servidor__id = request.GET.get('servidor'))
    
    if request.GET.get('servico'):
        agenda = agenda.filter(atendimento__servico__id = request.GET.get('servico'))
    
    return agenda
