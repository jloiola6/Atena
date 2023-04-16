from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao

from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import Permissao

def index(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8, 14, 15, 23, 24, 25, 33, 34, 36, 37]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/index.html'
    user = request.session['username']

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    return TemplateResponse(request, template_name, locals())
