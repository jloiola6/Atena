from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao

from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import Permissao

from aplicacoes.core.models import Historico
from aplicacoes.usuario.models import Usuarios
from aplicacoes.lotacao.models import Servidor_lotacao
from aplicacoes.lotacao.filtros import *

def tecnico(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8, 14, 15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/tecnico/tecnico.html'
    user = request.session['username']

    lotacoes_historico = Historico.objects.filter(tabela= 'lotacao_servidor_lotacao', log__usuario__login= user, acao= 'A').values_list('objeto', flat= True)

    lotacoes = filtro_tecnico(request,lotacoes_historico)
    quantidade_lotacoes= len(lotacoes)
    autorizacao= Autorizacao_lotacao.objects.filter(lotacao__in= lotacoes_historico).values('autorizador','lotacao','autorizador__nome','lotacao__contrato__servidor__matricula','lotacao__contrato__servidor__id','status','data','motivo','lotacao__id','lotacao__contrato__servidor__nome','lotacao__contrato__digito','lotacao__unidade_escolar','lotacao__unidade_adm','lotacao__funcao', 'lotacao__data_memorando', 'status')

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    lotacao_aux = lotacoes[valor_paginacao-15:valor_paginacao]

    paginator = Paginator(lotacoes, 15)
    lotacoes = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():

        gets = (request.get_full_path().split('?')[1])

        if 'page' not in gets:
            gets = f'page={page}&' + gets

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', gets_ultima)



    return TemplateResponse(request, template_name, locals())
