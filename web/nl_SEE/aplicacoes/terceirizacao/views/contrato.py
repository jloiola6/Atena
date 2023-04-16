from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.administracao.models import *
from aplicacoes.atena.models import Cidade
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.models import Cargo
from aplicacoes.terceirizacao.actions.contrato import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.usuario.views import verificacao_maxima


def contrato_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True, 9):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/contrato/contrato-formulario.html'
    user = request.session['username']

    id_servidor = request.GET.get('id_servidor')
    if id_servidor != None:
        edicao = False
        servidor = Servidor.objects.get(id= id_servidor)

        id_item = request.GET.get('id_item')
        if id_item == None:
            #Pegando os contratos vinculados ao DETER
            id_contratos = []
            for contrato in Vinculacao_contrato.objects.filter(unidade_administrativa= 78).values('contrato__id'):
                id_contratos.append(contrato['contrato__id'])

            itens = Contrato_item.objects.filter(status= 1, contrato__in= id_contratos).values('id', 'contrato__numero_contrato', 'numero_item', 'descricao').exclude(vagas=0)
        else:
            itens = Contrato_item.objects.filter(id= id_item).values('id', 'contrato__numero_contrato', 'numero_item', 'descricao').exclude(vagas=0)

        itens = itens.order_by('contrato__numero_contrato')
        postos = Contrato_posto_vigilante.objects.filter(status= 1).values('id', 'item__contrato__numero_contrato', 'item__numero_item', 'endereco__escola__nome_escola', 'unidade_administrativa__sigla','unidade_administrativa__nome').exclude(vagas_ocupadas=2)
        endrecos = Endereco.objects.all().values('id', 'escola__cod_inep', 'escola__nome_escola' ).order_by('escola__nome_escola')
        unidades_administrativas = Unidade_administrativa.objects.all().values('id', 'sigla', 'nome').exclude(id= 1).order_by('sigla')

    cargos = Cargo.objects.all()
    tipos_contratos = ('EFETIVO', 'TEMPORÁRIO', 'COMISSÃO')
    cidades = Cidade.objects.filter(estado= 1)
    situacoes = ('EM EXERCÍCIO', 'EXONERADO/RESCISO', 'APOSENTADO', 'CEDIDO', 'EXONERADO', 'FALECIDO', 'LICENCIADO', 'AFASTADO')

    if request.method == 'POST':
        formulario_contrato_lotacao(request, edicao, servidor)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())

def finalizar_contrato(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True, 9):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/contrato/finalizar-contrato.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato == None:
        return HttpResponseRedirect('/')

    lotacao = Contrato_lotacao.objects.get(id= id_contrato)
    contrato = lotacao.item.contrato
    servidor = lotacao.servidor

    situacao = request.GET.get('situacao')
    finalizar = request.GET.get('finalizar')
    if request.method == 'POST':
        contrato_finalizar(request, lotacao)
        if situacao != None:
            return HttpResponseRedirect(f'/terceirizacao/contrato-formulario?id_servidor={servidor.id}&id_item={lotacao.item.id}')
        elif finalizar != None:
            return HttpResponseRedirect(f'/terceirizacao/servidor-perfil?id={servidor.id}')
        else:
            return HttpResponseRedirect(f'/terceirizacao/contrato-formulario?id_servidor={servidor.id}')

    return TemplateResponse(request, template_name, locals())

def ocorrencia_formulario_terceirizacao(request):
    if verificar_manutencao() or not verificacao_maxima(request, [16], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/contrato/ocorrencia-formulario-terceirizacao.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato_lotacao = Contrato_lotacao.objects.get(id = id_contrato)
        item = contrato_lotacao.item
        contrato = item.contrato
        servidor = contrato_lotacao.servidor

    ocorrencia = ['LICENÇA PATERNIDADE', 'LICENÇA MATERNIDADE', 'FÉRIAS', 'LAUDO MÉDICO DEFINITIVO DE FUNÇÃO', 'LICENÇA PARA TRATAMENTO DE SAÚDE', 'TEMPORARIAMENTE EM OUTRA FUNÇÃO', 'LICENÇA ACOMPANHANTE', 'LICENÇA PRÊMIO', 'AUXÍLIO DOENÇA', 'APOSENTADORIA', 'READEQUAÇÃO - LEI NALUH', 'AFASTAMENTO PARA ESTUDO FORA DO ESTADO (COM ÔNUS)', 'LICENÇA PARA EXERCÍCIO DE MANDATO  ELETIVO', 'LICENÇA PARA DESEMPENHO DE MANDATO CLASSISTA', 'LICENÇA PARA INTERESSE PARTICULAR (SEM ÔNUS)', 'LICENÇA ADOÇÃO', 'RETORNO AO TRABALHO', 'FALECIMENTO', 'LICENÇA PARA ATIVIDADE POLITICA', 'EXONERAÇÃO À PEDIDO', 'DEMISSÃO', 'ATESTADO MEDICO', 'AFASTAMENTO PARA ACOMPANHAR O CÔNJUGE', 'CESSÃO COM ÔNUS', 'CESSÃO SEM ÔNUS', 'LICENÇA CASAMENTO ', 'LICENCA PARA MANDATO ELEITORAL', 'EXONERAÇÃO']

    if request.method == 'POST':
        formulario_ocorrencia_terceirizacao(request, contrato_lotacao)
        return HttpResponseRedirect(f'/terceirizacao/servidor_contrato_perfil?id_contrato={id_contrato}')

    return TemplateResponse(request, template_name, locals())
