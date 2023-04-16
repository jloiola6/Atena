from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao

def view_generica(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')   

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'aplicacao/pasta/arquivo.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())