from aplicacoes.administracao.models import * 
from aplicacoes.core.actions import dict_compare, salvar_historico


def formulario_departamento(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')

    #Salvando no banco dados do departamento
    departamento = Departamento()
    diretoria = Diretoria.objects.get(id= request.GET.get('id'))
    departamento.diretoria = diretoria
    departamento.nome = nome
    departamento.sigla = sigla
    departamento.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...

    salvar_historico(request, departamento, edicao, 'administracao_departamento')


def formulario_divisao(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')

    #Salvando no banco dados da divisão
    divisao = Divisao()
    departamento = Departamento.objects.get(id= request.GET.get('id'))
    divisao.departamento = departamento
    divisao.nome = nome
    divisao.sigla = sigla
    divisao.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...

    salvar_historico(request, divisao, edicao, 'administracao_divisao')


def formulario_nucleo(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')

    #Salvando no banco dados do nucleo
    nucleo = Nucleo()
    divisao = Divisao.objects.get(id= request.GET.get('id'))
    nucleo.divisao = divisao
    nucleo.nome = nome
    nucleo.sigla = sigla
    nucleo.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...

    salvar_historico(request, nucleo, edicao, 'administracao_nucleo')