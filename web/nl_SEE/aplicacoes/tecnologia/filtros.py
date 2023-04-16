from django.core.paginator import Paginator
import requests

from .models import *
from django.db.models import Q

from aplicacoes.administracao.models import *
from aplicacoes.tecnologia.models import *


def filtro_contratos(request):
    id_contratos = []
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 11).values('contrato'):
        id_contratos.append(id['contrato'])

    numero_contrato = request.GET.get('numero_contrato')
    numero_sei = request.GET.get('numero_sei')
    empresa = request.GET.get('empresa')
    situacao = request.GET.get('situacao')

    contratos = Contrato_contrato.objects.filter(id__in= id_contratos)

    #Filtro pelo numero do contrato
    if numero_contrato != None and numero_contrato != '':
        contratos = contratos.filter(numero_contrato__icontains= numero_contrato)

    #Filtro pelo Sei
    if numero_sei != None and numero_sei != '':
        contratos = contratos.filter(numero_sei__contains= numero_sei)

    if empresa != None and empresa != '':
        contratos = contratos.filter(empresa__id= empresa)

    if situacao != None and situacao != '':
        contratos = contratos.filter(situacao= situacao)

    return contratos


def filtro_vagas(request):
    id_contratos = []
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 11).values('contrato'):
        id_contratos.append(id['contrato'])
    itens = Contrato_item.objects.filter(vagas= 1, contrato__id__in= id_contratos, descricao__icontains= 'Link')
    itens = itens.exclude(contrato__empresa__cnpj= '07.928.901/0001-97')
    numero_contrato = request.GET.get('numero_contrato')
    empresa = request.GET.get('empresa')

    if numero_contrato != None and numero_contrato != '':
        itens = itens.filter(contrato__numero_contrato__contains= numero_contrato)

    if empresa != None and empresa != '':
        itens = itens.filter(contrato__empresa__id= empresa)

    return itens


def filtro_links(request, name_bandas, name_operadoras, name_status, name_fornecedor, name_tipo, name_velocidade, name_fontes):
    municipio = request.GET.get('municipio')
    numero_item = request.GET.get('numero_item')
    numero_circuito = request.GET.get('numero_circuito')
    educacional = request.GET.get('educacional')
    departamento = request.GET.get('departamento')

    links = Link.objects.all().values('id', 'item__contrato__numero_contrato', 'unidade_educacional__escola__cod_inep', 'unidade_educacional__escola__nome_escola', 'departamento__sigla', 'departamento__nome', 'tipo', 'fornecedor', 'operadora', 'tipo_banda', 'circuito', 'velocidade', 'status', 'item', 'item__numero_item', 'item__valor_unitario', 'fonte').order_by('-id')
    geral = False

    if numero_circuito != None and numero_circuito != '':
        links = links.filter(circuito__icontains = numero_circuito)
        geral = True

    if numero_item != None and numero_item != '':
        links = links.filter(item= numero_item)
        geral = True

    if educacional != None and educacional != '':
        links = links.filter(unidade_educacional = educacional)
        geral = True

    elif departamento != None and departamento != '':
        links = links.filter(departamento= departamento)
        geral = True

    tipo_filtro = []
    for tipo in name_tipo:
        if request.GET.get(tipo) == 'on':
            tipo_filtro.append(tipo)
    if len(tipo_filtro) > 0:
        links = links.filter(tipo__in = tipo_filtro)

    fornecedor_filtro = []
    for fornecedor in name_fornecedor:
        if request.GET.get(fornecedor) == 'on':
            fornecedor_filtro.append(fornecedor)
    if len(fornecedor_filtro) > 0:
        links = links.filter(fornecedor__in = fornecedor_filtro)
    elif not geral:
        links = links.filter(fornecedor= 'SEE')

    bandas_filtro = []
    for banda in name_bandas:
        if request.GET.get(banda) == 'on':
            bandas_filtro.append(banda)
    if len(bandas_filtro) > 0:
        links = links.filter(tipo_banda__in = bandas_filtro)

    operadoras_filtro = []
    for operadora in name_operadoras:
        if request.GET.get(operadora) == 'on':
            operadoras_filtro.append(operadora)
    if len(operadoras_filtro) > 0:
        links = links.filter(operadora__in = operadoras_filtro)

    status_filtro = []
    for status in name_status:
        if request.GET.get(status) == 'on':
            status_filtro.append(status)
    if len(status_filtro) > 0:
        links = links.filter(status__in = status_filtro)
    else:
        links = links.filter(status= 'ATIVO')

    velocidade_filtro = []
    for velocidade in name_velocidade:
        if request.GET.get(velocidade) == 'on':
            velocidade_filtro.append(velocidade)
    if len(velocidade_filtro) > 0:
        links = links.filter(velocidade__in = velocidade_filtro)

    fonte_filtro = []
    for fonte in name_fontes:
        if request.GET.get(fonte) == 'on':
            fonte_filtro.append(fonte)
    if len(fonte_filtro) > 0:
        links = links.filter(fonte__in = fonte_filtro)

    if municipio != None and municipio != '':
        links = links.filter(Q(departamento__endereco__municipio__icontains= municipio) | Q(unidade_educacional__municipio__icontains= municipio))


    return links


def filtro_chamados(request, tipo= None):
    if tipo == 'tecnico':
        chamado = Solicitacao.objects.filter(tecnico_atribuido= None, situacao__in=('Aberto', 'Pausado')).order_by('-id')
    else:
        # chamado = Solicitacao.objects.all().order_by('-id')
        solicitacao = Solicitacao.objects.values_list('id', flat=True)
        chamado = Solicitacao_chamado.objects.filter(solicitacao__in = solicitacao, sub_chamado = 0).order_by('-solicitacao__id')

    id_chamado = request.GET.get('id_chamado')
    tipo_chamado = request.GET.get('tipo_chamado')
    unidade_administrativa = request.GET.get('unidade_administrativa')
    endereco_escola = request.GET.get('endereco_escola')
    chamado_status = request.GET.get('chamado_status')


    if id_chamado != '' and id_chamado != None:
        chamado = chamado.filter(solicitacao__id = id_chamado)

    if tipo_chamado == 'Interno':
        chamado = chamado.filter(solicitacao__tipo_chamado = tipo_chamado)

    if tipo_chamado == 'Externo':
        chamado = chamado.filter(solicitacao__tipo_chamado = tipo_chamado)

    if unidade_administrativa != '' and unidade_administrativa != None :
        chamado = chamado.filter(solicitacao__unidade_administrativa = unidade_administrativa)

    if endereco_escola != '' and endereco_escola != None :
        chamado = chamado.filter(solicitacao__endereco_escola = endereco_escola)

    if chamado_status == 'Aberto':
        chamado = chamado.filter(solicitacao__situacao = chamado_status)

    if chamado_status == 'Em atendimento':
        chamado = chamado.filter(solicitacao__situacao = chamado_status)

    if chamado_status == 'Finalizado':
        chamado = chamado.filter(solicitacao__situacao = chamado_status)

    return chamado


def filtro_tablets(request):
    solicitacoes = EC_solicitacao.objects.all().values('endereco_escola__escola__id', 'endereco_escola', 'aluno_turma__turma__id', 'endereco_escola__escola__cod_inep', 'endereco_escola__escola__nome_escola', 'aluno_turma__aluno__nome', 'endereco_escola__municipio', 'cad_unico', 'aluno_turma__turma__nome', 'aluno_turma__aluno__nome_responsavel').order_by('endereco_escola__escola__nome_escola', 'aluno_turma__turma__nome', 'aluno_turma__aluno__nome')

    inep = request.GET.get('cod_inep')
    endereco = request.GET.get('nome_unidade')
    turma = request.GET.get('turma')
    aluno_cad = request.GET.get('aluno_cad')

    if inep != None and inep != '':
        solicitacoes = solicitacoes.filter(endereco_escola__escola__cod_inep= int(inep))

    if endereco != None and endereco != '':
        solicitacoes = solicitacoes.filter(endereco_escola__id= endereco)

    if turma != None and turma != '':
        solicitacoes = solicitacoes.filter(aluno_turma__turma= turma)

    if aluno_cad != None and aluno_cad != '':
        solicitacoes = solicitacoes.filter(cad_unico= aluno_cad)

    return solicitacoes


def filtro_auxilio(request, tipo):
    nome = request.GET.get('nome')
    escola = request.GET.get('educacional')
    situacao = request.GET.get('situacao')
    municipio = request.GET.get('municipio')
    page = request.GET.get('page')

    if situacao != 'D':

        if escola is None:
            escola = ''

        if tipo == 'notas':
            if nome is not None and nome != '':
                situacao = 'T'
            elif situacao is None and situacao != '':
                situacao = '1'

        elif tipo == 'solicitacao':
            if situacao is None or situacao == '':
                situacao = 'T'
            elif nome is not None or nome != '':
                situacao = situacao

        if nome is None:
            nome = ''

        if municipio is None:
            municipio = ''

        if page is None:
            page = '1'

        if tipo == 'solicitacao':
            solicitacoes = requests.get(f'https://auxilio.see.ac.gov.br/api/dados-solicitacoes/?chave=d55dafc14c6801c9dc99b3d8778598cf&page={page}&nome={nome}&escola={escola}&situacao={situacao}&municipio={municipio}').json()
            notas = None
        elif tipo == 'devolucao':
            solicitacoes = requests.get(f'https://auxilio.see.ac.gov.br/api/dados-notas/?chave=d55dafc14c6801c9dc99b3d8778598cf&page={page}&nome={nome}&escola={escola}&situacao=2&municipio={municipio}').json()
            notas = None


        elif tipo == 'notas':
            solicitacoes = requests.get(f'https://auxilio.see.ac.gov.br/api/dados-notas/?chave=d55dafc14c6801c9dc99b3d8778598cf&page={page}&nome={nome}&escola={escola}&situacao={situacao}&municipio={municipio}').json()
            notas = solicitacoes[-2]
            solicitacoes.pop(-2)

        quantidade_solicitacoes = solicitacoes[-1]
        solicitacoes.pop()

        gets_primeira = f'page=1&nome={nome}&educacional={escola}&situacao={situacao}&municipio={municipio}'
        gets_anterior = f'page={int(page)-1}&nome={nome}&educacional={escola}&situacao={situacao}&municipio={municipio}'
        gets_proxima = f'page={int(page)+1}&nome={nome}&educacional={escola}&situacao={situacao}&municipio={municipio}'
        gets_ultima = f'page={quantidade_solicitacoes["pg_total"]}&nome={nome}&educacional={escola}&situacao={situacao}&municipio={municipio}'


        return [solicitacoes, quantidade_solicitacoes, gets_primeira, gets_anterior, gets_proxima, gets_ultima, notas]
    else:

        if nome is None:
            nome = ''

        if escola is None:
            escola = ''

        if municipio is None:
            municipio = ''

        if page is None:
            page = '1'

        # Pesquisar para o modal de Filtro - Pesquisa Geral e retorna todos quem já quem fizeram a devolução
        if (situacao == 'D') and (nome == '') and (escola == '') and (municipio == ''):

            devolucao_auxilio = Auxilio_notebook.objects.all().values()
            devolucao_perfil = []

            for dado in devolucao_auxilio:
                dados = requests.get(f'https://auxilio.see.ac.gov.br/api/dado-nota/?chave=d55dafc14c6801c9dc99b3d8778598cf&id={dado["auxilio"]}').json()

                id_servidor = Servidor.objects.filter(cpf=dados[0]['usuario__cpf']).values('id')

                dict_devolucao = {
                    "id": dados[0]['id'],
                    "nome": dados[0]['usuario__nome'],
                    "cpf": dados[0]['usuario__cpf'],
                    "path": dado['arquivo'],
                    "lotacao":dados[0]['usuario__lotacao__nome'],
                    "municipio": dados[0]['usuario__lotacao__municipio']
                }

                devolucao_perfil.append(dict_devolucao)
                quantidade_devolucao = len(devolucao_perfil)

            return [devolucao_perfil, quantidade_devolucao]
        else:
            devolucao_auxilio = Auxilio_notebook.objects.all().values()
            devolucao_perfil = []

            for dado in devolucao_auxilio:
                dados = requests.get(f'https://auxilio.see.ac.gov.br/api/dado-nota/?chave=d55dafc14c6801c9dc99b3d8778598cf&id={dado["auxilio"]}').json()

                id_servidor = Servidor.objects.filter(cpf=dados[0]['usuario__cpf']).values('id')

                dict_devolucao = {
                    "id": dados[0]['id'],
                    "nome": dados[0]['usuario__nome'],
                    "cpf": dados[0]['usuario__cpf'],
                    "path": dado['arquivo'],
                    "lotacao":dados[0]['usuario__lotacao__nome'],
                    "municipio": dados[0]['usuario__lotacao__municipio']
                }

                devolucao_perfil.append(dict_devolucao)
                quantidade_devolucao = len(devolucao_perfil)

            return [devolucao_perfil, quantidade_devolucao]
