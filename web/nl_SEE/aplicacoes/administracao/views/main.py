from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.administracao.models import * 
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao



# Create your views here.
def index(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [1, 2, 5, 10]):
        return HttpResponseRedirect('/')

    if Permissao.objects.filter(usuario__login= request.session['username'], servico= 5).exists():
        permissao = Permissao.objects.get(usuario__login= request.session['username'], servico= 5)
        inep = Gestor_Escolar.objects.get(permissao= permissao)
        gestor = True

    template_name = 'administracao/index.html'
    user = request.session['username']
    
    permissoes_banco = Permissao.objects.filter(usuario__login= user, consultar= 1)
    permissoes = []
    for permissao in permissoes_banco:
        permissoes.append(permissao.servico.id)
            
    return TemplateResponse(request, template_name, locals())
