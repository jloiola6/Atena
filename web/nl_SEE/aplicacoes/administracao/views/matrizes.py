from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.administracao.models import *
from aplicacoes.administracao.actions.matrizes import *

# VIEW DA PÁGINA DE MATRIZES
def matrizes(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/matrizes/matrizes.html'
    user = request.session['username']

    matrizes = Matriz.objects.all()

    return TemplateResponse(request, template_name, locals())

# VIEW DA PÁGINA DE FORMULÁRIO DE MATRIZ
def matriz_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    etapas = Etapa.objects.all()

    disciplinas = Disciplinas.objects.all().order_by('nome')

    template_name = 'administracao/matrizes/matriz-formulario.html'
    user = request.session['username']

    if request.method == 'POST':
        formulario_matriz(request)

        return HttpResponseRedirect('/administracao/matrizes')

    return TemplateResponse(request, template_name, locals())

# VIEW DA PÁGINA DE UMA MATRIZ
def matriz(request, id_matriz):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/matrizes/matriz.html'
    user = request.session['username']

    try:
        matriz = Matriz.objects.get(id= id_matriz)
    except:
        return HttpResponseRedirect('/administracao')


    disciplinas = Matriz_disciplina.objects.filter(matriz= matriz).order_by('disciplina__nome')

    return TemplateResponse(request, template_name, locals())