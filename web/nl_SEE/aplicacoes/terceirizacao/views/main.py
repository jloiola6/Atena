from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao

def index(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9, 16, 17, 18]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/index.html'
    user = request.session['username']

    permissoes_banco = Permissao.objects.filter(usuario__login= user, consultar= 1)
    permissoes = []
    for permissao in permissoes_banco:
        permissoes.append(permissao.servico.id)

    return TemplateResponse(request, template_name, locals())
