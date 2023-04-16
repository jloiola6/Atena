from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.administracao.models import * 
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.administracao.actions.organograma import *
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao



def organograma(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [2]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/organograma/organograma.html'
    user = request.session['username']

    diretorias = Diretoria.objects.all().order_by('id')
    departamentos = Departamento.objects.all()
    divisoes = Divisao.objects.all()
    nucleos = Nucleo.objects.all()

    return TemplateResponse(request, template_name, locals())








# def departamento_formulario(request):
#     if verificar_manutencao():
#         return HttpResponseRedirect('/')   

#     if not verificacao_maxima(request, [2]):
#         return HttpResponseRedirect('/')

#     id_diretoria= request.GET.get('id')
#     diretoria = Diretoria.objects.get(id= id_diretoria)

#     template_name = 'administracao/organograma/departamento_formulario.html'
#     user = request.session['username']

#     if request.method == 'POST':
#         formulario_departamento(request)

#     return TemplateResponse(request, template_name, locals())


# def divisao_formulario(request):
#     if verificar_manutencao():
#         return HttpResponseRedirect('/')   

#     if not verificacao_maxima(request, [2]):
#         return HttpResponseRedirect('/')

#     id_departamento= request.GET.get('id')
#     departamento = Departamento.objects.get(id= id_departamento)

#     user = request.session['username']
#     template_name = 'administracao/organograma/divisao_formulario.html'

#     if request.method == 'POST':
#         formulario_divisao(request)

#     return TemplateResponse(request, template_name, locals())


# def nucleo_formulario(request):
#     if verificar_manutencao():
#         return HttpResponseRedirect('/')   

#     if not verificacao_maxima(request, [2]):
#         return HttpResponseRedirect('/')

#     id_divisao= request.GET.get('id')
#     divisao = Divisao.objects.get(id= id_divisao)

#     template_name = 'administracao/organograma/nucleo_formulario.html'
#     user = request.session['username']

#     if request.method == 'POST':
#         formulario_nucleo(request)

#     return TemplateResponse(request, template_name, locals())
