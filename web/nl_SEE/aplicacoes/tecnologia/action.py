from .models import *

from aplicacoes.administracao.models import *
from aplicacoes.core.uploads import *
from aplicacoes.core.actions import dict_compare, salvar_historico


def formulario_link(request, edicao):
    #Dados Link
    tipo = request.POST.get('tipo')
    fornecedor = request.POST.get('fornecedor')
    operadora = request.POST.get('operadora')
    tipo_banda = request.POST.get('tipo_banda')
    status = request.POST.get('status')
    iplan = request.POST.get('iplan')
    ipwan = request.POST.get('ipwan')
    circuito = request.POST.get('circuito')
    usuario_equipamento = request.POST.get('usuario_equipamento')
    senha_equipamento = request.POST.get('senha_equipamento')
    velocidade = request.POST.get('velocidade')

    #Coletando dado caso seja unidade ou departamento
    if tipo == 'UNIDADE EDUCACIONAL':
        unidade = int(request.POST.get('unidade'))
        departamento = None
    else:
        departamento = int(request.POST.get('departamento'))
        unidade = None

    #Consultando o banco
    if edicao:
        # pass
        id_link = int(request.GET.get('link'))
        inputs = {'id': id_link, 'tipo': tipo, 'fornecedor': fornecedor, 'operadora': operadora, 'tipo_banda': tipo_banda, 'status': status, 'iplan': iplan, 'ipwan': ipwan, 'circuito': circuito, 'usuario_equipamento': usuario_equipamento, 'senha_equipamento': senha_equipamento, 'velocidade': velocidade, 'unidade_educacional_id': unidade, 'departamento_id': departamento}
        link = Link.objects.filter(id= id_link)

        modificacoes = dict_compare(link.values()[0], inputs)

        link = link[0]

    else:
        modificacoes = None
        link = Link()

    #Salvando no banco dados do Link
    if tipo == 'UNIDADE EDUCACIONAL':
        endereco = Endereco.objects.get(id= unidade)
        link.unidade_educacional = endereco
        link.departamento = None
    else:
        link.departamento = Departamento.objects.get(id= departamento)
        link.unidade_educacional = None

    link.tipo = tipo
    link.fornecedor = fornecedor
    link.operadora = operadora
    link.tipo_banda = tipo_banda
    link.status = status
    link.iplan = iplan
    link.ipwan = ipwan
    link.circuito = circuito
    link.usuario_equipamento = usuario_equipamento
    link.senha_equipamento = senha_equipamento
    link.velocidade = velocidade
    link.save()

    salvar_historico(request, link, edicao, 'tecnologia_links', modificacoes)



def devolucao_auxilio(request, auxilio, documento, data):
    termo = request.FILES.get('termo')
    nome = auxilio['usuario__nome'].replace(' ','_')+'.pdf'

    devolucao_existente = Auxilio_notebook.objects.get(auxilio= auxilio['id'])
    devolucao_existente.data = data
    devolucao_existente.notaFiscal = int(documento)
    devolucao_existente.arquivo = handle_uploaded_file(termo, nome, 'tecnologia/auxilio/devolucoes', '')
    devolucao_existente.save()

    salvar_historico(request, devolucao_existente, False, 'auxilio_notebook')