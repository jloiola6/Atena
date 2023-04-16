from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from aplicacoes.lotacao.models import Servidor, Servico, Lotacao_assinatura
from aplicacoes.administracao.models import Endereco
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.actions.lotacao import *
from datetime import datetime

def autorizacao_lotacao(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [37]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/autorizacao/index.html'
    user = request.session['username']

    lista_municipios = []
    servidor_lotacao = Servidor_lotacao.objects.all()
    municipio = servidor_lotacao.filter(status = 2).values('unidade_escolar__municipio', 'unidade_adm__endereco__municipio').distinct()
    unidade_adm = servidor_lotacao.filter(status = 2).values('unidade_adm__nome', 'unidade_adm__sigla').distinct()
    unidade_escolar = servidor_lotacao.filter(status = 2).values('unidade_escolar__escola__nome_escola').distinct()
    tecnicos = Lotacao_assinatura.objects.filter(lotacao__status = 2).values('tecnico').distinct()
    for i in municipio:
        if i['unidade_escolar__municipio'] == None and i['unidade_adm__endereco__municipio'] not in lista_municipios:
            lista_municipios.append(i['unidade_adm__endereco__municipio'])
        elif i['unidade_adm__endereco__municipio'] == None and i['unidade_escolar__municipio'] not in lista_municipios:
            lista_municipios.append(i['unidade_escolar__municipio'])
    lotacoes = filtro_autorizacao(request)

    quantidade_lotacoes= len(lotacoes)
    data = datetime.today()

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    lotacao_aux = lotacoes[valor_paginacao-15:valor_paginacao]
    grades = []
    for lotacao in lotacao_aux:
        id_lotacao= lotacao['id']

        try:
            lotacao['assinatura'] = Lotacao_assinatura.objects.get(lotacao= id_lotacao)
        except:
            lotacao['assinatura'] = None

        try:
            lotacao['assinatura__tecnico'] = Lotacao_assinatura.objects.get(lotacao= id_lotacao).tecnico
        except:
            lotacao['assinatura__tecnico'] = None

        lotacao['enturmacao_escola'] = Grade.objects.filter(professor= id_lotacao, status= 1)
        lotacao['enturmacao_alunos'] = Professor_aluno.objects.filter(professor= id_lotacao, status= 1)
        lotacao['enturmacao_disciplinas_adm'] = Grade_professor_adm.objects.filter(professor= id_lotacao, status= 2)
        turnos = []

        if lotacao['turno_manha']:
            turnos.append('Manhã')

        if lotacao['turno_tarde']:
            turnos.append('Tarde')

        if lotacao['turno_noite']:
            turnos.append('Noite')

        lotacao['turnos'] = turnos

    verificador= False
    usuario= Usuarios.objects.filter(login= user).values_list('id')
    permissoes = Permissao.objects.filter(usuario_id= usuario[0], servico_id= 37)
    for i in permissoes:
        if Permissao.objects.filter(id= i.id, editar= 0, imprimir= 0, consultar= 1 ).exists():
            verificador= True


    paginator = Paginator(lotacoes, 15)
    paginacao = paginator.get_page(page)

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

    if request.method == 'POST':
        id_lotacao = request.POST.get('lotacao')

        lotacao_autorizar(request, id_lotacao, user, data)
        return HttpResponseRedirect(f'/lotacao/autorizacao-lotacao')

    return TemplateResponse(request, template_name, locals())


def autorizacao_verbas(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [38]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/autorizacao-verbas/index.html'
    user = request.session['username']

    lista_municipios = []
    servidor_lotacao = Servidor_lotacao.objects.all()
    municipio = servidor_lotacao.filter(status = 2).values('unidade_escolar__municipio', 'unidade_adm__endereco__municipio').distinct()
    unidade_adm = servidor_lotacao.filter(status = 2).values('unidade_adm__nome', 'unidade_adm__sigla').distinct()
    unidade_escolar = servidor_lotacao.filter(status = 2).values('unidade_escolar__escola__nome_escola').distinct()
    tecnicos = Lotacao_assinatura.objects.filter(lotacao__status = 2).values('tecnico').distinct()
    for i in municipio:
        if i['unidade_escolar__municipio'] == None and i['unidade_adm__endereco__municipio'] not in lista_municipios:
            lista_municipios.append(i['unidade_adm__endereco__municipio'])
        elif i['unidade_adm__endereco__municipio'] == None and i['unidade_escolar__municipio'] not in lista_municipios:
            lista_municipios.append(i['unidade_escolar__municipio'])
    lotacoes = filtro_autorizacao_verbas(request)

    quantidade_lotacoes= len(lotacoes)
    data = datetime.today()

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)
    lotacao_aux = lotacoes[valor_paginacao-15:valor_paginacao]
    grades = []
    verificador= False
    for lotacao in lotacao_aux:
        id_lotacao= lotacao['id']


        try:
            lotacao['assinatura'] = Lotacao_assinatura.objects.get(lotacao= id_lotacao)
        except:
            lotacao['assinatura'] = None

        try:
            lotacao['assinatura__tecnico'] = Lotacao_assinatura.objects.get(lotacao= id_lotacao).tecnico
        except:
            lotacao['assinatura__tecnico'] = None

        lotacao['enturmacao_escola'] = Grade.objects.filter(professor= id_lotacao, status= 1)
        lotacao['enturmacao_alunos'] = Professor_aluno.objects.filter(professor= id_lotacao, status= 1)
        lotacao['enturmacao_disciplinas_adm'] = Grade_professor_adm.objects.filter(professor= id_lotacao, status= 2)
        turnos = []

        if lotacao['turno_manha']:
            turnos.append('Manhã')

        if lotacao['turno_tarde']:
            turnos.append('Tarde')

        if lotacao['turno_noite']:
            turnos.append('Noite')

        lotacao['turnos'] = turnos

    usuario= Usuarios.objects.filter(login= user).values_list('id')
    permissoes = Permissao.objects.filter(usuario_id= usuario[0], servico_id= 38)
    for i in permissoes:
        if Permissao.objects.filter(id= i.id, editar= 0, imprimir= 0, consultar= 1 ):
            verificador= True

    if request.GET:
        print(request.GET)

    paginator = Paginator(lotacoes, 15)
    paginacao = paginator.get_page(page)

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

    if request.method == 'POST':
        id_lotacao = request.POST.get('lotacao')

        lotacao_autorizar(request, id_lotacao, user, data)
        return HttpResponseRedirect(f'/lotacao/autorizacao-verbas')

    return TemplateResponse(request, template_name, locals())