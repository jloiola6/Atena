from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.atena.models import * 
from aplicacoes.administracao.models import * 
from aplicacoes.administracao.actions.contrato import *

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao


def contrato_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    tipo_contrato = request.GET.get('tipo')
    if tipo_contrato == 'limpeza':
        template_name = 'administracao/contrato/contrato-limpeza-formulario.html'
    elif tipo_contrato == 'produto':
        template_name = 'administracao/contrato/contrato-produto-formulario.html'
    elif tipo_contrato == 'servico':
        template_name = 'administracao/contrato/contrato-servico-formulario.html'
    elif tipo_contrato == 'trabalho':
        template_name = 'administracao/contrato/contrato-trabalho-formulario.html'
    elif tipo_contrato == 'vigilante':
        template_name = 'administracao/contrato/contrato-vigilante-formulario.html'
    user = request.session['username']

    fontes = ('100 (RP)', '200 (RP)', '300 (RP)', '500 (RP)')
    empresas = Contrato_empresa.objects.all()
    unidades_administrativas = Unidade_administrativa.objects.all().exclude(categoria= 1).order_by('nome')

    if request.method == 'POST':
        contrato = formulario_contrato(request)
        return HttpResponseRedirect(f'/administracao/contrato-perfil?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())


def empresa_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [10], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/contrato/empresa-formulario.html'
    user = request.session['username']

    estados = Estado.objects.all().order_by('nome')
    cidades = Cidade.objects.all().order_by('nome')

    #Fazer tela de edição depois

    if request.method == 'POST':
        formulario_empresa(request)
        return HttpResponseRedirect(f'/administracao/contratos')

    return TemplateResponse(request, template_name, locals())
