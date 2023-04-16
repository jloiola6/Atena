from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao


def index(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'coex/index.html'
    user = request.session['username']
    
    permissoes_banco = Permissao.objects.filter(usuario__login= user, consultar= 1)
    permissoes = []
    for permissao in permissoes_banco:
        permissoes.append(permissao.servico.id)

    return TemplateResponse(request, template_name, locals())
