from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.models import Permissao

from aplicacoes.administracao.models import *
from aplicacoes.tecnologia.actions.educacao_conectada import *
from aplicacoes.tecnologia.models import Ec_tablet
from aplicacoes.tecnologia.filtros import filtro_tablets
from aplicacoes.tecnologia.exportar import exportar_pdf_tablets, exportar_pdf_tablets_aluno

def educacao_conectada(request):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/educacao-conectada.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())

# APAGAR AQUI QUANDO ACABAR
def tablets(request):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/index.html'
    user = request.session['username']

    enderecos = Endereco.objects.all().values('id', 'escola__cod_inep', 'escola__nome_escola').order_by('escola')
    endereco_id = request.GET.get('nome_unidade')

    escolas_id = list(EC_solicitacao.objects.values_list('endereco_escola__escola__id', flat= True))
    enderecos_busca = Endereco.objects.filter(escola__id__in= escolas_id).values('id', 'escola__cod_inep', 'escola__nome_escola').order_by('escola')


    solicitacoes = filtro_tablets(request)
    try:
        quantidade_solicitacoes = solicitacoes.count()
    except:
        quantidade_solicitacoes = 0

    if endereco_id:
        selecionar_endereco = Endereco.objects.get(id= endereco_id)
        id_turma = request.GET.get('turma')

        if id_turma:
            selecionar_turma = Turmas.objects.get(id= id_turma)

        turmas_id = list(EC_solicitacao.objects.filter(endereco_escola= endereco_id).values_list('aluno_turma__turma__id', flat= True))
        turmas = Turmas.objects.filter(id__in= turmas_id).values('id', 'nome').order_by('nome').distinct()

    id_escola = request.GET.get('escola')
    if id_escola != None:
        return HttpResponseRedirect(f'/tecnologia/tablet-formulario?id={id_escola}')

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'lista_alunos':
            return exportar_pdf_tablets(request, user)
        else:
            return exportar_pdf_tablets_aluno(request, user, solicitacoes)

    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(solicitacoes, 15)
    solicitacoes = paginator.get_page(page)

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


# VIEW PARA A PÁGINA COM AS ESCOLAS PARTICIPANTES DO PROGRAMA
def escolas(request):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/escolas.html'
    user = request.session['username']

    # LISTANDO AS ETAPAS DE ENSINO MÉDIO PARA FILTRO DE ESCOLAS
    etapas_medio = [5, 6]

    ineps = Etapa_escola.objects.filter(etapa_id__in= etapas_medio).values('escola__cod_inep').distinct()

    print(ineps.count())

    escolas = Escola.objects.filter(cod_inep__in= ineps).order_by('nome_escola')
    # escolas = Etapa_escola.objects.filter(etapa__id__in= etapas_medio).values('escola__id', 'escola__cod_inep','escola__nome_escola').order_by('escola__nome_escola').distinct()

    # for escola in escolas:
    #     print(escola)
    #     escola['municipio']

    escolas_aux = escolas

    quantidade_escolas = escolas.count()
    print(quantidade_escolas)

    page = request.GET.get('page')

    if not page:
        page = 1

    paginator = Paginator(escolas, 15)
    escolas = paginator.get_page(page)

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


# VIEW PARA A PÁGINA DE PERFIL DE UMA ESCOLA
def escola_perfil(request, id_escola):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/escola-perfil.html'
    user = request.session['username']

    try:
        escola = Escola.objects.get(id= id_escola)
    except:
        return HttpResponseRedirect('/tecnologia/escolas')

    # DEFININDO CONSTANDO PARA O ANO LETIVO
    ANO_LETIVO = 2023

    # LISTANDO AS ETAPAS DE ENSINO MÉDIO PARA FILTRO DE ESCOLAS
    etapas_medio = [5, 6]

    # INICIALIZANDO AS ETAPAS DE ENSINO DA ESCOLA
    escola_etapas = Etapa_escola.objects.filter(escola= escola, etapa__id__in= etapas_medio)

    # REDIRECIONANDO A PÁGINA CASO A ESCOLA NÃO POSSUA ETAPA DE ENSINO MÉDIO
    if not escola_etapas:
        return HttpResponseRedirect('/tecnologia/escolas')

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexo = Endereco.objects.filter(escola= escola).count() > 1

    # EXTRAINDO O ID ENDEREÇO PASSADO NA URL
    id_endereco = request.GET.get('id_endereco')

    # CASO A ESCOLA POSSUA ANEXOS E NENHUM AINDA TENHA SIDO SELECIONADO, ENCAMINHAR PARA A PÁGINA DE SELEÇÃO DE ANEXOS
    if possui_anexo and not id_endereco:
        return HttpResponseRedirect(f'/tecnologia/escola-anexos/{id_escola}')

    # INICIALIZANDO O ENDEREÇO NO CASO DE UM ANEXO TER SIDO SELECIONADO OU CASO A ESCOLA NÃO POSSUA
    try:
        if id_endereco:
            endereco = Endereco.objects.get(escola= escola, id= id_endereco)
        else:
            endereco = Endereco.objects.get(escola= escola)
    except:
        return HttpResponseRedirect('/tecnologia/escolas')

    if endereco.tipo == 'S':
        tipo_endereco = 'Sede'
    else:
        tipo_endereco = f'Anexo {endereco.numero_anexo}'

    # TURMAS

    # LISTANDO AS TURMAS DA UNIDADE COM O ANO LETIVO CORRENTE
    turmas = Turmas.objects.filter(endereco= endereco, ano_letivo= ANO_LETIVO)
    quantidade_turmas = turmas.count()

    if turmas:
        # LISTANDO AS ETAPAS DE ENSINO DA ESCOLA
        turmas_etapas = escola_etapas.values('etapa__id', 'etapa__nome')

        # ADICIONANDO O TOTAL DE ALUNOS POR ETAPA DE ENSINO
        for etapa in turmas_etapas:
            qtd_alunos = Aluno_turma.objects.filter(turma__endereco= endereco, turma__ano_letivo= ANO_LETIVO, turma__etapa__id= etapa['etapa__id'], status=1).count()
            etapa['qtd_alunos'] = qtd_alunos

            # ADICIONANDO CLASSES PARA O CSS
            if etapa['etapa__id'] in [3, 4]:
                etapa['classe'] = 'dropdown--fundamental'
            elif etapa['etapa__id'] in [5, 6]:
                etapa['classe'] = 'dropdown--medio'
            elif etapa['etapa__id'] in [7, 8, 9]:
                etapa['classe'] = 'dropdown--eja'
            elif etapa['etapa__id'] in [10]:
                etapa['classe'] = 'dropdown--aee'
            elif etapa['etapa__id'] in [11]:
                etapa['classe'] = 'dropdown--aprender-caminho'
            elif etapa['etapa__id'] in [12, 13, 14]:
                etapa['classe'] = 'dropdown--caminhos-campo'
            else:
                etapa['classe'] = ''

        # LISTANDO OS ANOS E SÉRIES DE CADA ETAPA DE ENSINO
        turmas_series = turmas.values('etapa', 'ano_serie').order_by('ano_serie').distinct()

        for serie in turmas_series:
            qtd_alunos = Aluno_turma.objects.filter(turma__endereco= endereco, turma__ano_letivo= ANO_LETIVO, turma__etapa__id= serie['etapa'], turma__ano_serie= serie['ano_serie'], status=1).count()
            serie['qtd_alunos'] = qtd_alunos

        turmas = turmas.order_by('nome')

    return TemplateResponse(request, template_name, locals())


# VIEW PARA A PÁGINA DE SELEÇÃO DE ENDEREÇO DE ESCOLAS QUE POSSUEM ANEXO
def escola_anexos(request, id_escola):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/escola-anexos.html'

    user = request.session['username']

    try:
        escola = Escola.objects.get(id= id_escola)
    except:
        return HttpResponseRedirect('/tecnologia/escolas')

    enderecos = Endereco.objects.filter(escola= escola).order_by('-tipo')

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexos = enderecos.count() > 1

    if not possui_anexos:
        return HttpResponseRedirect(f'/tecnologia/escola-perfil/{id_escola}')

    return TemplateResponse(request, template_name, locals())

# VIEW PARA A PÁGINA DE UMA TURMA
def turma_perfil(request, id_turma):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/turma-perfil.html'
    user = request.session['username']

    try:
        turma = Turmas.objects.get(id= id_turma)
    except:
        return HttpResponseRedirect('/tecnologia/escolas')

    # LISTANDO AS ETAPAS DE ENSINO MÉDIO PARA FILTRO DE ESCOLAS
    etapas_medio = [5, 6]

    if turma.etapa.id not in etapas_medio:
        return HttpResponseRedirect('/tecnologia/escolas')

    # Verificando se a turma tem alunos com entrega pendente pra exportar o termo e se tiver pegar a lista de alunos
    exportar = False
    if Ec_tablet.objects.filter(aluno_turma__turma= turma, status__in = [1, 0]).exists():
        lista = []
        exportar = True
        for i in Ec_tablet.objects.filter(aluno_turma__turma= turma, status__in = [1, 0]):
            lista.append(i.aluno_turma.id)
        print(lista)
    # LISTANDO OS ALUNOS MATRICLADOS NA TURMA
    # alunos = Aluno_turma.objects.filter(turma= turma).order_by('aluno__nome')
    alunos = Aluno_turma.objects.filter(turma= turma, status= 1).values('id', 'aluno__id', 'aluno__nome', 'aluno__nascimento', 'aluno__sexo', 'aluno__bolsa_familia').order_by('aluno__nome')

    for aluno in alunos:
        if aluno['aluno__sexo'] == 'M':
            aluno['aluno__sexo'] = 'Masculino'
        else:
            aluno['aluno__sexo'] = 'Feminino'

        if aluno['aluno__bolsa_familia']:
            aluno['aluno__bolsa_familia'] = 'Possui'
        else:
            aluno['aluno__bolsa_familia'] = 'Não possui'

        id = aluno['id']

        try:
            aluno['tablet_status'] = Ec_tablet.objects.get(aluno_turma__id= id).status
        except:
            aluno['tablet_status'] = None


        if aluno['tablet_status'] == 0:
            aluno['tablet_status_title'] = 'Entrega pendente'
            aluno['tablet_status_classe'] = 'tablet-status tablet--pendente'
        elif aluno['tablet_status'] == 1:
            aluno['tablet_status_title'] = 'Entregue à escola'
            aluno['tablet_status_classe'] = 'tablet-status tablet--entregue'
        elif aluno['tablet_status'] == 2:
            aluno['tablet_status_title'] = 'Finalizado'
            aluno['tablet_status_classe'] = 'tablet-status tablet--finalizado'
        elif aluno['tablet_status'] is None:
            aluno['tablet_status_title'] = 'Não cadastrado'
            aluno['tablet_status_classe'] = 'tablet-status tablet--nao-cadastrado'


    qtd_alunos = alunos.count()

    # LISTANDO AS SITUAÇÕES DOS TABLETS DA TURMA
    tablets_pendentes = Ec_tablet.objects.filter(aluno_turma__turma= turma, status= 0).count()
    tablets_entregues = Ec_tablet.objects.filter(aluno_turma__turma= turma, status= 1).count()
    tablets_finalizados = Ec_tablet.objects.filter(aluno_turma__turma= turma, status= 2).count()

    # CALCULANDO A QUANTIDADE DE TABLETS NÃO CADASTRADOS
    tablets_nao_cadastrados = qtd_alunos - (tablets_pendentes + tablets_entregues)

    page = request.GET.get('page')

    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
    paginator = Paginator(alunos, 15)
    alunos = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if request.POST:
        if('entregar' in request.POST):
            tablets_pendentes = Ec_tablet.objects.filter(aluno_turma__turma= turma, status= 0)
            entregar_tablets(tablets_pendentes)

        if request.POST.get('exportar-aluno-pdf') == 'exportar-aluno-pdf':
            dados = []
            for dado in Ec_tablet.objects.filter(aluno_turma__turma= turma, status__in =  [0, 1]).values('aluno_turma__aluno__nome', 'aluno_turma__turma__endereco__escola__nome_escola', 'aluno_turma__aluno__nome_mae', 'aluno_turma__aluno__nome_pai', 'imei_tablet', 'serial_chip', 'serial_tablet', 'aluno_turma__turma__nome', 'aluno_turma__turma__turno', 'cad_unico').order_by('aluno_turma__aluno__nome'):
                dados.append(dado)
            return exportar_pdf_tablets_aluno(request, user, dados)

        return HttpResponseRedirect(f'/tecnologia/turma-perfil/{turma.id}')

    return TemplateResponse(request, template_name, locals())


# VIEW PARA O CADASTRO DE TABLETS POR TURMA
def tablet_formulario(request, id_turma):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/tablet-formulario.html'
    user = request.session['username']

    try:
        turma = Turmas.objects.get(id= id_turma)
    except:
        return HttpResponseRedirect('/tecnologia/escolas')

    # id_escola = request.GET.get('id')
    # turmas = Turmas.objects.filter(endereco= id_escola, ano_letivo= '2022').order_by('nome')
    retirar = Ec_tablet.objects.filter(aluno_turma__turma= turma).values_list('aluno_turma')
    alunos = Aluno_turma.objects.filter(turma= turma, status= 1).exclude(id__in= retirar).order_by('aluno__nome')

    qtd_alunos = alunos.count()
    # print(len(alunos))


    # if id_escola == None or id_escola == '':
    #     return HttpResponseRedirect('/tecnologia/index-tablet')



    if request.method == "POST":
        formulario_tablet(request, alunos)
        return HttpResponseRedirect(f'/tecnologia/turma-perfil/{turma.id}')

    return TemplateResponse(request, template_name, locals())


def aluno_perfil(request, id_aluno_turma):
    if not verificacao_maxima(request, [26]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/educacao-conectada/tablets/aluno-perfil.html'
    user = request.session['username']

    try:
        aluno_turma = Aluno_turma.objects.get(id= id_aluno_turma)
    except:
        return HttpResponseRedirect('/tecnologia/educacao-conectada/')

    try:
        aluno = Ec_tablet.objects.get(aluno_turma = id_aluno_turma)
    except:
        return HttpResponseRedirect(f'/tecnologia/turma-perfil/{aluno_turma.turma.id}')

    if request.method == "POST":
        editar_dados(request, id_aluno_turma)
        return HttpResponseRedirect(f'/tecnologia/turma-perfil/{aluno.aluno_turma.turma.id}')

    return TemplateResponse(request, template_name, locals())