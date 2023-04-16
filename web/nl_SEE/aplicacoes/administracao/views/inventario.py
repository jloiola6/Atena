from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

import itertools
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.administracao.models import *
from aplicacoes.administracao.actions.inventario import *
from aplicacoes.atena.models import *

# VIEW PARA CONTROLE DE CATEGORIAS E TIPOS DE ITENS, EXCLUSIVO PARA DEV
def controle_inventario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/inventario/controle-inventario.html'
    user = request.session['username']

    # LISTANDO AS CATEGORIAS EXISTENTES
    categorias = Inventario_item_categoria.objects.all().order_by('nome')

    # LISTANDO OS TIPOS EXISTENTES
    tipos = Inventario_item_tipo.objects.all().order_by('categoria__nome')

    if request.method == 'POST':
        formulario_controle_inventario(request)

    return TemplateResponse(request, template_name, locals())


def pegar_detalhes(lista, editar):
    inventario = []
    for item in lista:
        equipamento = item.equipamento.nome

        if equipamento == 'Computador/Notebook':
            banco = Computador.objects.get(inventario_eletronico= item)
            detalhe = {'processador': banco.processador, 'ram': banco.ram, 'disco': banco.disco, 'ssd': banco.ssd, 'placa_video': banco.placa_video, 'tipo': banco.tipo, 'cor': banco.cor}

        elif equipamento == 'Nobreak':
            banco = Nobreak.objects.get(inventario_eletronico= item)
            detalhe = {'qtd_tomadas': banco.qtd_tomadas, 'estabilizador': banco.estabilizador}

        elif equipamento == 'Projetor':
            banco = Projetor.objects.get(inventario_eletronico= item)
            detalhe = {'resolucao': banco.resolucao, 'potencia': banco.potencia, 'lumens': banco.lumens}

        elif equipamento == 'Impressora':
            banco = Impressora.objects.get(inventario_eletronico= item)
            detalhe = {'tipo_impressao': banco.tipo_impressao, 'conectividade': banco.conectividade}

        elif equipamento == 'Switch':
            banco = Switch.objects.get(inventario_eletronico= item)
            detalhe = {'qtd_RJ45': banco.qtd_RJ45, 'qtd_SFP': banco.qtd_SFP, 'fonte_integrada': banco.fonte_integrada, 'potencia': banco.potencia}

        elif equipamento == 'Geladeira':
            banco = Geladeira.objects.get(inventario_eletrodomestico= item)
            detalhe = {'cor': banco.cor, 'capacidade': banco.capacidade, 'voltagem': banco.voltagem}

        elif equipamento == 'Ar Condicionado':
            banco = Ar_condicionado.objects.get(inventario_eletrodomestico= item)
            detalhe = {'cor': banco.cor, 'capacidade': banco.capacidade, 'voltagem': banco.voltagem}

        elif equipamento == 'Freezer':
            banco = Freezer.objects.get(inventario_eletrodomestico= item)
            detalhe = {'cor': banco.cor, 'capacidade': banco.capacidade, 'voltagem': banco.voltagem}

        elif equipamento == 'Liquidificador':
            banco = Liquidificador.objects.get(inventario_eletrodomestico= item)
            detalhe = {'cor': banco.cor, 'capacidade': banco.capacidade, 'potencia':banco.potencia , 'voltagem': banco.voltagem}

        elif equipamento == 'Fogão':
            banco = Fogao.objects.get(inventario_eletrodomestico= item)
            detalhe = {'cor': banco.cor, 'capacidade': banco.capacidade, 'voltagem': banco.voltagem, 'industrial':banco.industrial}

        elif equipamento == 'Cadeira':
            banco = Cadeira.objects.get(inventario_mobilia= item)
            detalhe = {'tipo': banco.tipo}

        elif equipamento == 'Mesa':
            banco = Mesa.objects.get(inventario_mobilia= item)
            detalhe = {'tipo': banco.tipo}

        elif equipamento == 'Armário':
            banco = Armario.objects.get(inventario_mobilia= item)
            detalhe = {'tipo': banco.tipo}

        elif equipamento == 'Estante':
            banco = Estante.objects.get(inventario_mobilia= item)
            detalhe = {'tipo': banco.tipo}

        elif equipamento == 'Quadro':
            banco = Quadro.objects.get(inventario_mobilia= item)
            detalhe = {'tipo': banco.tipo, 'tamanho': banco.tamanho}
        else:
            detalhe = None

        if editar:
            return detalhe


        inventario.append((item, detalhe))

    return inventario

# VIEW PARA A PÁGINA DE INVENTÁRIO DE UMA ESCOLA
def inventario_perfil(request, id_infraestrutura):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/inventario/inventario-perfil.html'
    user = request.session['username']

    try:
        infraestrutura = Infraestrutura_geral.objects.get(id= id_infraestrutura)
        endereco = Endereco.objects.get(infraestrutura= infraestrutura)
    except:
        return HttpResponseRedirect('/administracao')

    escola = endereco.escola

    # LISTANDO AS DEPENDÊNCIAS DE ACORDO COM A INFRAESTRUTURA
    dependencias = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura).values('id', 'tipo_dependencia_id', 'tipo_dependencia__categoria', 'descricao')

    # LISTANDO OS TIPOS DE DEPENDÊNCIAS PARA AGRUPAMENTO
    categorias_dependencias = dependencias.values('tipo_dependencia__categoria').distinct()

    # for categoria in categorias_dependencias:
    #     print(categoria)

    # PERCORRENDO AS DEPENDÊNCIAS PARA ADICIONAR UM VERIFICADOR DE CASO A DEPENDÊNCIA TENHA ITENS CADASTRADOS
    for dependencia in dependencias:
        dependencia['possui_itens'] = Inventario_item.objects.filter(dependencia_id= dependencia['id']).exists()

    itens = Inventario_item.objects.filter(dependencia__infraestrutura= infraestrutura).order_by('tipo__nome')

    # LISTANDO AS CATEGORIAS DOS ITENS PARA AGRUPAMENTO
    categorias_itens = Inventario_item.objects.filter(dependencia__infraestrutura= infraestrutura).values('dependencia_id', 'tipo__categoria__nome', 'tipo__categoria__id').distinct()

    itens_detalhes = Inventario_item_detalhes.objects.filter(item__dependencia__infraestrutura= infraestrutura)

    # LISTANDO OS ITENS PARA CADASTRO
    itens_categorias = Inventario_item_categoria.objects.all()
    itens_tipos = Inventario_item_tipo.objects.all().order_by('nome')

    if request.method == 'POST':
        dependencia = request.POST.get('dependencia')
        tipo = request.POST.get('tipo')
        print(request.POST)
        return HttpResponseRedirect(f'/administracao/item-formulario/{dependencia}/{tipo}')

    return TemplateResponse(request, template_name, locals())

# VIEW PARA O FORMULÁRIO DE ITENS
def item_formulario(request, id_dependencia, id_tipo):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/inventario/item-formulario/item-formulario.html'
    user = request.session['username']

    try:
        dependencia = Infraestrutura_dependencia.objects.get(id= id_dependencia)
        endereco = Endereco.objects.get(infraestrutura= dependencia.infraestrutura)
        tipo = Inventario_item_tipo.objects.get(id= id_tipo)
    except:
        HttpResponseRedirect('/administracao')

    escola = endereco.escola

    if request.method == 'POST':
        formulario_item(request, tipo, dependencia)

        return HttpResponseRedirect(f'/administracao/inventario-perfil/{dependencia.infraestrutura.id}')

    return TemplateResponse(request, template_name, locals())

# # VAI SUMIR ESSA MERDAAAAAAA
# def inventario_formulario(request):
    # if verificar_manutencao():
    #     return HttpResponseRedirect('/')

    # if not verificacao_maxima(request, [1, 5], True):
    #     return HttpResponseRedirect('/')

    # template_name = 'administracao/unidades/inventario/inventario-formulario.html'
    # user = request.session['username']

    # id_tipo = request.GET.get('id_tipo')
    # id_item = request.GET.get('id_item')
    # if id_tipo != None:
    #     edicao = True
    #     equipamento_item = Equipamento.objects.get(id= id_tipo)

    #     if equipamento_item.tipo == 'eletronico':
    #         tipos = [('eletronico', 'Eletrônico')]
    #         inventario = Inventario_Eletronico.objects.get(id= id_item)
    #     if equipamento_item.tipo == 'eletrodomestico':
    #         tipos = [('eletrodomestico', 'Eletrodoméstico')]
    #         inventario = Inventario_Eletrodomestico.objects.get(id= id_item)
    #     if equipamento_item.tipo == 'mobilia':
    #         tipos = [('mobilia', 'Mobília')]
    #         inventario = Inventario_Mobilia.objects.get(id= id_item)
    #     if equipamento_item.tipo == 'insumo':
    #         tipos = [('insumo', 'Insumo')]
    #         inventario = Inventario_Insumo.objects.get(id= id_item)

    #     detalhes = pegar_detalhes([inventario], edicao)

    #     endereco = inventario.dependencia.infraestrutura.endereco
    #     escola = endereco.escola

    #     equipamentos = [equipamento_item]

    # else:
    #     edicao = False
    #     equipamentos = Equipamento.objects.all().order_by('nome')
    #     tipos = [('mobilia', 'Mobília'), ('eletronico', 'Eletrônico'), ('eletrodomestico', 'Eletrodoméstico'), ('insumo', 'Insumo')]

    # endereco_id = request.GET.get('id')
    # if endereco_id != None:
    #     endereco = Endereco.objects.get(id= endereco_id)
    #     escola = endereco.escola

    # dependencias = Infraestrutura_tipo_dependencia.objects.filter(infraestrutura__endereco= endereco)
    # if dependencias.count() == 0:
    #     return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={endereco.escola.cod_inep}')

    # if request.method == 'POST':
    #     formulario_inventario(request, edicao)
    #     if edicao:
    #         return HttpResponseRedirect(f'/administracao/inventario_perfil?id={endereco.id}')

    # return TemplateResponse(request, template_name, locals())