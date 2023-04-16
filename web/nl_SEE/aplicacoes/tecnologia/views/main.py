from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao
# Create your views here.

def index(request):
    if not verificacao_maxima(request, [12, 13, 20, 21, 26, 28, 29, 30, 31, 32]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/index.html'
    user = request.session['username']

    auxilio_permissao = Permissao.objects.filter(usuario__login= user, consultar= 1, servico__in = [28, 29, 30]).exists()
    chamado_permissao = Permissao.objects.filter(usuario__login= user, consultar= 1, servico__in = [21, 31, 32]).exists()

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    return TemplateResponse(request, template_name, locals())
