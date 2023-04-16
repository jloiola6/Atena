from os import link
from aplicacoes.administracao.actions.unidade import *
from aplicacoes.administracao.exportar import *
from aplicacoes.administracao.filtros import *
from aplicacoes.administracao.models import *
from aplicacoes.coex.models import *
from aplicacoes.tecnologia.models import *
from aplicacoes.fundiaria.models import *
from aplicacoes.core.views import (global_municipios, global_regioes,
                                   global_zoneamentos, verificar_manutencao)

# from aplicacoes.dinem.models import Aluno
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import Logs, Permissao, Usuarios, Servico
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from unidecode import unidecode
from aplicacoes.fundiaria.exportar import exportar_pdf_escola

from django.db.models import Sum
import math

ANO_ATUAL = str(date.today().year)

def unidades_educacionais(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1]):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'administracao/unidades/unidades.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)

    aplicacao = 'administracao'

    enderecos = Endereco.objects.filter(tipo='S').values('escola__cod_inep', 'escola__nome_escola', 'municipio', 'regiao', 'tipo_localizacao').order_by('escola__nome_escola')
    print(enderecos)

    login = ('ana.marina', 'erick.nascimento', 'fabio.santos', 'franklin.farias', 'joaopedro.passos', 'joaoteixeira.netto', 'josecarlos.souza', 'tharlis.seixas')
    if user not in login:
        enderecos = enderecos.exclude(id__in = [669, 723, 724, 722, 741, 738])

    #Consultando as etapas de ensino para filtro
    name_tipificacoes = []
    tipificacoes = []
    for tipificacao in Escola.objects.all().values('tipificacao').distinct().exclude(tipificacao= None).order_by('tipificacao'):
        name = (tipificacao['tipificacao'])
        tipificacoes.append((f'id-{name}', name, tipificacao['tipificacao']))
        name_tipificacoes.append(name)

    name_total_alunos = []
    total_alunos = []
    for aluno in Escola.objects.all().values('total_alunos').distinct().exclude(tipificacao= None).order_by('total_alunos'):
        name = (aluno['total_alunos'])
        total_alunos.append((f'id-{name}', name, aluno['total_alunos']))
        name_total_alunos.append(name)

    #Consultando as etapas de ensino para filtro
    name_etapas = []
    etapas = []
    for etapa in Etapa_escola.objects.all().values('etapa__nome').distinct():
        name = (etapa['etapa__nome']).replace(' ', '_')
        etapas.append((f'id-{name}', name, etapa['etapa__nome']))
        name_etapas.append(name)

    #Consultando as modalidades de ensino para filtro
    # name_modalidades = []
    # modalidades = []
    # for modalidade in Turmas.objects.all().values('etapa__modalidade__nome').distinct():
    #     name = (modalidade['etapa__modalidade__nome']).replace(' ', '_')
    #     modalidades.append((f'id-{name}', name, modalidade['etapa__modalidade__nome']))
    #     name_modalidades.append(name)

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        name = ('ETNIA_' + detalhe['etnia']).replace(' ', '_')
        etnias.append((f'id-{name}', name, detalhe['etnia']))
        name_etnia.append(name)

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        name = ('LOCALIZACAO_' + detalhe['localizacao']).replace(' ', '_')
        localizacoes.append((f'id-{name}', name, detalhe['localizacao']))
        name_localizacao.append(name)

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        name = ('ALDEIA_' + detalhe['aldeia']).replace(' ', '_')
        aldeias.append((f'id-{name}', name, detalhe['aldeia']))
        name_aldeia.append(name)

    #resgatando informações globais na aplicação Core
    municipios = global_municipios
    regioes = global_regioes

    #Definindo os names dos inputs checkbox de região
    name_regioes = []
    for regiao in regioes:
        name_regioes.append(unidecode(regiao).replace(' ','-').replace('/', '').replace('--', '-').lower())

    #Definindo os names dos inputs checkbox de municipios
    name_municipios = []
    for municipio in municipios:
        name_municipios.append(unidecode(municipio).replace(' ', '-'))

    #Criando um zip dos label e names dos inputs para usar na tag do front
    qtd_regioes = zip(regioes, name_regioes)
    qtd_municipios = zip(municipios, name_municipios)

    #Definindo informações de id, names e label para inputs checkbox tipo de localização
    tipo_localizacao = [('id-urbAno', 'localizacao_urbAno', 'UrbAno'), ('id-rural', 'localizacao_rural', 'Rural'), ('id-indigena', 'localizacao_indigena', 'Indígena')]

    #Atualizando dados da tabela de acordo com os filtros
    enderecos = filtro_unidades(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes, name_total_alunos)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes, name_total_alunos)
        elif request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_unidades(request, enderecos)


    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
    try:
        quantidade_escolas = enderecos.count()
    except:
        quantidade_escolas = len(enderecos)

    paginator = Paginator(enderecos, 15)
    enderecos = paginator.get_page(page)


    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        # if len(gets.split('&')) > 1:
            #Paginação + filtros passados pela url
        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if "page" not in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

        #Garantindo a existencia dos campos filtrados na página de acordo com os gets na url
        filtros_etapas = []
        filtros_municipio = []
        filtros_regional = []
        filtros_localizacao = []
        filtros_etnias = []
        filtros_aldeias = []
        filtros_localizacao_inidigena = []
        filtros_tipificacoes = []

        for item in gets.split('&'):
            item = item.split('=')
            valor = item[0].replace('Ensino_M%C3%A9dio_-_Regular', 'Ensino_Médio_-_Regular')
            if item[0] == 'cod_inep':
                cod_inep = item[1]
            elif item[0] == 'nome_unidade':
                nome_unidade = item[1].replace('+', ' ')
            elif valor in name_municipios:
                filtros_municipio.append(valor)
            elif valor in name_regioes:
                filtros_regional.append(valor)
            elif valor in name_etapas:
                filtros_etapas.append(valor)
            elif valor in name_etnia:
                filtros_etnias.append(valor)
            elif valor in name_aldeia:
                filtros_aldeias.append(valor)
            elif valor in name_localizacao:
                filtros_localizacao_inidigena.append(valor)
            elif valor in name_tipificacoes:
                filtros_tipificacoes.append(valor)

            for i in tipo_localizacao:
                if i[1] == valor:
                    filtros_localizacao.append(valor)

    return TemplateResponse(request, template_name, locals())


# VIEW PARA A PÁGINA DE SELEÇÃO DE ENDEREÇO DE ESCOLAS QUE POSSUEM ANEXO
def unidade_anexos(request, inep):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/unidade-anexos.html'

    user = request.session['username']

    try:
        escola = Escola.objects.get(cod_inep= inep)
    except:
        return HttpResponseRedirect('/administracao/unidades')

    enderecos = Endereco.objects.filter(escola= escola).order_by('-tipo')

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexos = enderecos.count() > 1

    if not possui_anexos:
        return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={inep}')

    return TemplateResponse(request, template_name, locals())


# VIEW PARA A PÁGINA DE PERFIL DE UMA UNIDADE EDUCACIONAL
def unidade_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5, 7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/unidade-perfil.html'

    user = request.session['username']

    usuarios_editar = ['joaopedro.passos', 'erick.nascimento', 'josecarlos.souza', 'franklin.farias', 'rute.neres', 'fabio.santos', 'gustavo.lima', 'vitor.daniel']

    # DEFININDO UMA CONSTANTE PARA O ANO LETIVO
    ANO_LETIVO = ANO_ATUAL

    # VARIÁVEIS NECESSÁRIAS PARA A CONSTRUÇÃO DA PARTIAL DE PERFIL DE UNIDADE
    aplicacao = 'Administração'

    cod_inep = request.GET.get('inep')
    id_endereco = request.GET.get('id_endereco')

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    try:
        escola = Escola.objects.get(cod_inep= cod_inep)
    except:
        return HttpResponseRedirect('/administracao')

    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexo = Endereco.objects.filter(escola= escola).count() > 1

    # CASO A ESCOLA POSSUA ANEXOS E NENHUM AINDA TENHA SIDO SELECIONADO, ENCAMINHAR PARA A PÁGINA DE SELEÇÃO DE ANEXOS
    if possui_anexo and not id_endereco:
        return HttpResponseRedirect(f'/administracao/unidade-anexos/{cod_inep}')

    # INICIALIZANDO O ENDEREÇO NO CASO DE UM ANEXO TER SIDO SELECIONADO OU CASO A ESCOLA NÃO POSSUA
    try:
        if id_endereco:
            endereco = Endereco.objects.get(escola= escola, id= id_endereco)
        else:
            endereco = Endereco.objects.get(escola= escola)
    except:
        return HttpResponseRedirect('/administracao')

    # INICIALIZANDO OS DADOS DO COMITE EXECUTIVO DE ACORDO COM A ESCOLA
    if Coex.objects.filter(escola= escola, status=1).exists():
        coex = Coex.objects.get(escola= escola, status=1)

        if Consorcio.objects.filter(cnpj= coex.cnpj, status=1).exists():
            consorcio = Consorcio.objects.get(cnpj= coex.cnpj, status=1)

    # INICIALIZANDO OS CONTATOS DA UNIDADE DE ACORDO COM O ENDEREÇO
    contatos = Contato.objects.filter(endereco= endereco)

    # INICIALIZANDO OS DADOS DA EQUIPE GESTORA DA UNIDADE
    diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
        diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagógico(a)', status= 1).exists():
        pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagógico(a)', status= 1).last().contrato.servidor.nome

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
        ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
        administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
        secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    # FIM DAS VARIÁVEIS NECESSÁRIAS PARA A PARTIAL

    # TURMAS

    # LISTANDO AS TURMAS DA UNIDADE COM O ANO LETIVO CORRENTE
    turmas = Turmas.objects.filter(endereco= endereco, ano_letivo= ANO_LETIVO)

    quantidade_turmas = 0
    for turma in turmas:
        if turma.qtd_alunos not in [0, '0', '', None]:
            quantidade_turmas += 1

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

    # OUVIDORIA
    municipios= Cidade.objects.filter(estado=1)
    ocorrencias = ['Desacato','Vias de Fato','Bullying','Abandono','Dano ao Patrimônio','Crimes Sexuais','Trafico de Pessoas','Ameaça','Agressão','Furto','Roubo','Tentativa de Homicídio','Tentativa de Suicídio','Suicídio','Homicídio','Auto lesão','Maus tratos','Calunia Difamação','Injuria','Violência contra mulher','Saída não autorizada da Instituição de ensino','Racismo','Intolerância Religiosa']
    sexos = ['Feminino','Masculino','Outro']
    tempo_gestacao= ['1º Trimestre','2º Trimestre','3º Trimestre','Idade Gestacional Ignorada']
    cores = ['Branco(a)','Preto(a)','Amarelo(a)','Pardo(a)','Indígena','Não Declarada']

    # INFRAESTRUTURA

    # INICIALIZANDO A INFRAESTRUTURA DA UNIDADE E LISTANDO AS DEPENDÊNCIAS FÍSICAS
    infraestrutura = endereco.infraestrutura

    dependencias = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura)

    if dependencias:
        # LISTANDO AS CATEGORIAS E TIPOS DE DEPENDENCIAS FÍSICAS PARA AGRUPAMENTO
        categorias_dependencias = dependencias.values('tipo_dependencia__categoria').distinct()
        tipos_dependencias = dependencias.values('tipo_dependencia', 'tipo_dependencia__categoria', 'tipo_dependencia__tipo').distinct()


    # INVENTÁRIO
    itens = Inventario_item.objects.filter(dependencia__infraestrutura= infraestrutura)

    # LISTANDO OS ITENS PARA CADASTRO
    itens_categorias = Inventario_item_categoria.objects.all()
    itens_tipos = Inventario_item_tipo.objects.all().order_by('nome')

    if itens:
        # LISTANDO AS CATEGORIAS E TIPOS DE ITENS PARA AGRUPAMENTO
        categorias_itens = itens.values('tipo__categoria', 'tipo__categoria__nome').distinct()
        tipos_itens = itens.values('tipo', 'tipo__categoria', 'tipo__nome').distinct()

        for tipo in tipos_itens:
            tipo['quantidade'] = itens.filter(tipo= tipo['tipo']).count()

    if request.method == 'POST':
        # SUBMISSÃO PARA ENTRAR NO FORMULÁRIO DE ITEM
        if request.POST.get('dependencia'):
            id_dependencia = request.POST.get('dependencia')
            id_tipo = request.POST.get('tipo')

            return HttpResponseRedirect(f'/administracao/item-formulario/{id_dependencia}/{id_tipo}')

        # SUBMISSÃO PARA CADASTRAR UM GOOGLE MAP
        if request.POST.get('google_map'):
            adicionar_mapa(request, endereco)

    return TemplateResponse(request, template_name, locals())


# VIEW PARA A PÁGINA DE MATRIZ ESCOLAR DE UMA UNIDADE
def unidade_matriz(request, id_endereco):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/matriz/unidade-matriz.html'
    user = request.session['username']

    try:
        endereco = Endereco.objects.get(id= id_endereco)
    except:
        return HttpResponseRedirect('/administracao')

    # DEFININDO UMA CONSTANTE PARA O ANO LETIVO
    ANO_LETIVO = '2022'

    escola = endereco.escola
    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    # turmas = Turmas.objects.filter(endereco= endereco, ano_letivo= ANO_LETIVO)

    turmas = Turmas.objects.filter(endereco= endereco, ano_letivo= ANO_LETIVO).values('id', 'nome', 'etapa_id', 'ano_serie', 'etapa__nome', 'matriz', 'matriz__nome')

    if turmas:
        # LISTANDO AS ETAPAS DE ENSINO DA ESCOLA
        turmas_etapas = escola_etapas.values('etapa__id', 'etapa__nome')

        # ADICIONANDO CLASSES PARA O CSS
        for etapa in turmas_etapas:
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
            qtd_alunos = Aluno_turma.objects.filter(turma__endereco= endereco, turma__ano_letivo= ANO_LETIVO, turma__etapa__id= serie['etapa'], turma__ano_serie= serie['ano_serie']).count()
            serie['qtd_alunos'] = qtd_alunos

        for turma in turmas:
            # ADICIONANDO A QUANTIDADE DE ALUNOS DA TURMA
            grade = Grade.objects.filter(turma= turma['id'], status= 1)
            qtd_disciplinas = grade.count()
            turma['qtd_disciplinas'] = qtd_disciplinas

            # ADICIONANDO A QUANTIDADE DE HORAS CADASTRADAS NA TURMA
            if qtd_disciplinas > 0:
                total_ch_turma = int(grade.aggregate(Sum('carga_horaria'))['carga_horaria__sum'])
                turma['total_ch'] = total_ch_turma
            else:
                turma['total_ch'] = 0

            try:
                matriz = Matriz.objects.get(id= turma['matriz'])
                matriz_disciplinas = Matriz_disciplina.objects.filter(matriz= matriz)

                total_ch_matriz = int(matriz_disciplinas.aggregate(Sum('carga_horaria'))['carga_horaria__sum'])

                # ADICIONANDO A CARGA HORÁRIA TOTAL EXIGIDA PELA MATRIZ
                turma['total_ch_matriz'] = total_ch_matriz

                # CALCULANDO A PORCENTAGEM DE DISCIPLINAS CUMPRIDAS EM RELAÇÃO À MATRIZ
                turma['porcentagem'] = math.floor((turma['total_ch'] * 100) / turma['total_ch_matriz'])

                if turma['porcentagem'] == 100:
                    status = 'Completo'
                    classe = 'turma__status--completo'
                elif turma['porcentagem'] < 100:
                    status = 'Disponível'
                    classe = 'turma__status--disponivel'
                else:
                    status = 'Excede'
                    classe = 'turma__status--excede'

                turma['status'] = status
                turma['status_classe'] = classe
            except:
                pass

        # LISTANDO AS DISCIPLINAS DAS TURMAS
        grades = Grade.objects.filter(turma__endereco= endereco, status= 1).values('turma__id', 'disciplina__nome', 'carga_horaria', 'professor').order_by('disciplina__nome')

        for grade in grades:
            professor = Servidor_lotacao.objects.get(id= grade['professor'])
            grade['grade_professor'] = professor



    return TemplateResponse(request, template_name, locals())


def unidade_formulario(request):
    # Essa view agora é responsável tanto pela criação de unidades como pela adição de anexos
    # -Pegar o Id da escola ao invés do endereço para ativar a variável edição

    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1], True):
        return HttpResponseRedirect('/')


    template_name = 'administracao/unidades/unidade_formulario.html'
    user = request.session['username']
    inep = request.GET.get('inep')

    edicao = False
    municipios = global_municipios
    zoneamentos = global_zoneamentos
    etapas = Etapa.objects.all()
    dependencias = ['Estadual', 'Federal', 'Municipal', 'Privado']
    localizacao_diferenciada = ['', 'Terra Indígena', 'Quilombo', 'Área de Assentamento']

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        etnias.append(detalhe['etnia'])

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        localizacoes.append(detalhe['localizacao'])

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        aldeias.append(detalhe['aldeia'])

    if request.method == 'POST':
        formulario_unidade(request, edicao)
        if edicao:
            endereco = Endereco.objects.get(id= int(request.GET.get('id')))
            return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={endereco.escola.cod_inep}')
        return HttpResponseRedirect('/administracao/unidades')

    return TemplateResponse(request, template_name, locals())


def editar_dados(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/editar_dados.html'
    user = request.session['username']
    dependencias = ['Estadual', 'Federal', 'Municipal', 'Privado']

    id_escola = request.GET.get('id')
    if id_escola in (None, ''):
        return HttpResponseRedirect('/administracao/unidades')

    escola = Escola.objects.get(id= id_escola)
    etapas = Etapa.objects.all()

    etapa_existentes = []
    for item in Etapa_escola.objects.filter(escola= escola):
        etapa_existentes.append(item.etapa)

    if request.method == 'POST':
        inep = formulario_dados(request, etapa_existentes)
        return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={inep}')

    return TemplateResponse(request, template_name, locals())


def editar_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/editar_endereco.html'
    user = request.session['username']
    municipios = global_municipios
    zoneamentos = global_zoneamentos
    localizacao_diferenciada = ['', 'Terra Indígena', 'Quilombo', 'Área de Assentamento']

    id_endereco = request.GET.get('id')
    if id_endereco in (None, ''):
        return HttpResponseRedirect('/administracao/unidades')

    endereco = Endereco.objects.get(id= id_endereco)
    if Detalhes_Indigena.objects.filter(escola= endereco.escola).exists():
        detalhes_indigenas = Detalhes_Indigena.objects.get(escola= endereco.escola)

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        etnias.append(detalhe['etnia'])

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        localizacoes.append(detalhe['localizacao'])

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        aldeias.append(detalhe['aldeia'])

    if request.method == 'POST':
        formulario_endereco(request)
        return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={endereco.escola.cod_inep}')

    return TemplateResponse(request, template_name, locals())


def unidade_contatos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/unidade_contatos.html'
    user = request.session['username']
    id_endereco = request.GET.get('id')
    edicao = True

    endereco = Endereco.objects.get(id= id_endereco)
    contatos = Contato.objects.filter(endereco= endereco)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        editar_contatos(request, edicao)
        return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={endereco.escola.cod_inep}')

    return TemplateResponse(request, template_name, locals())


def turma_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    id_endereco = request.GET.get('id')
    id_turma = request.GET.get('turma')
    if id_turma != None:
        turma = Turmas.objects.get(id= id_turma)
        endereco = turma.endereco
        escola = endereco.escola
        identificar_turma = turma.nome.split(' ')
        edicao = True

        etapa_escola = Etapa_escola.objects.filter(escola= escola)
        id_etapas = []
        for item in etapa_escola:
            id_etapas.append(item.etapa.id)

    else:
        endereco = Endereco.objects.get(id= id_endereco)
        escola = endereco.escola
        edicao = False

    etapa_escola = Etapa_escola.objects.filter(escola= escola).exclude(etapa__id= 1).exclude(etapa__id= 2)
    id_etapas = []
    for item in etapa_escola:
        id_etapas.append(item.etapa.id)

    etapas = Etapa.objects.filter(id__in= id_etapas)

    user = request.session['username']
    template_name = 'administracao/unidades/turma/turma_formulario.html'
    turnos = ['Matutino', 'Vespertino', 'Noturno', 'Integral']

    serie_fundamental1 = ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano']
    serie_fundamental2 = ['6º Ano', '7º Ano', '8º Ano', '9º Ano']
    serie_medio = ['1ª Série', '2ª Série', '3ª Série']

    turmas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    modulos = ['Módulo I - A', 'Módulo I - B', 'Módulo II - A', 'Módulo II - B', 'Módulo III - A', 'Módulo III - B', 'Módulo IV - A', 'Módulo IV - B', 'Módulo V - A', 'Módulo V - B', 'Módulo VI - A', 'Módulo VI - B', 'Módulo VII - A', 'Módulo VII - B']


    if request.method == 'POST':
        formulario_turma(request, edicao)
        if edicao:
            return HttpResponseRedirect(f'/administracao/turma_perfil?id={id_turma}')

    return TemplateResponse(request, template_name, locals())


def turma_perfil_antigo(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/turma/turma_perfil.html'
    user = request.session['username']

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    id_turma = request.GET.get('id')
    turma = Turmas.objects.get(id= id_turma)
    escola = turma.endereco.escola
    alunos = Aluno_turma.objects.filter(turma= turma, status= 1).order_by('aluno__nome')
    qtd_alunos = alunos.count()

    # Coletando os mediadores na turma
    ids_alunos = alunos.values_list('aluno', flat= True)
    professores = Professor_aluno.objects.filter(aluno_id__in= ids_alunos)

    mediadores = []

    for p in professores:
        professor = Servidor_lotacao.objects.get(id= p.professor)
        mediadores.append({'professor': professor, 'aluno': p.aluno})


    #Coleta a página atual para atualzar informações na tabela
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

    grades = []
    for grade in Grade.objects.filter(turma= turma, status= 1):
        if grade.professor not in (None, 0):
            grades.append((grade, Servidor_lotacao.objects.get(id= grade.professor).contrato.servidor))
        else:
            grades.append((grade, 'Sem Professor'))

    possui_grades = len(grades) > 0

    return TemplateResponse(request, template_name, locals())

# VIEW PARA O PERFIL DE UMA TURMA
def turma_perfil(request, id_turma):
    if verificar_manutencao() or not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/turma/turma-perfil.html'
    user = request.session['username']

    # LISTANDO AS PERMISSÕES DO USUÁRIO
    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    try:
        turma = Turmas.objects.get(id= id_turma)
    except:
        return HttpResponseRedirect('adminitracao/')

    escola = turma.endereco.escola

    if turma.ano_letivo == ANO_ATUAL:
        alunos = Aluno_turma.objects.filter(turma= turma, status= 1).order_by('aluno__nome')
    else:
        alunos = Aluno_turma.objects.filter(turma= turma).order_by('aluno__nome')

    qtd_alunos = alunos.count()

    # Coletando os mediadores na turma
    # ids_alunos = alunos.values_list('aluno', flat= True)
    # professores = Professor_aluno.objects.filter(aluno_id__in= ids_alunos)

    # mediadores = []

    # for p in professores:
    #     professor = Servidor_lotacao.objects.get(id= p.professor)
    #     mediadores.append({'professor': professor, 'aluno': p.aluno})


    #Coleta a página atual para atualzar informações na tabela
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

    # grades = []
    # for grade in Grade.objects.filter(turma= turma, status= 1):
    #     if grade.professor not in (None, 0):
    #         grades.append((grade, Servidor_lotacao.objects.get(id= grade.professor).contrato.servidor))
    #     else:
    #         grades.append((grade, 'Sem Professor'))

    # possui_grades = len(grades) > 0

    # CONTINGENCIA PARA EXCLUIR ENTURMAÇÕES RAPIDAEMENTE
    if request.POST:
        try:
            enturmacao = Aluno_turma.objects.get(id= request.POST.get('enturmacao'))
            enturmacao.delete()
        except:
            pass

    return TemplateResponse(request, template_name, locals())


def grade_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/turma/grade_formulario.html'
    user = request.session['username']

    id_turma = request.GET.get('id')
    id_grade = request.GET.get('grade')
    if id_grade != None:
        grade = Grade.objects.get(id= id_grade)
        turma = grade.turma
        edicao = True
    else:
        turma = Turmas.objects.get(id= id_turma)
        edicao = False
    endereco = turma.endereco
    escola = endereco.escola


    disciplinas_existentes = []
    for i in Grade.objects.filter(turma= turma):
        disciplinas_existentes.append(i.disciplina.id)

    if edicao:
        del disciplinas_existentes[disciplinas_existentes.index(grade.disciplina.id)]

    disciplinas = Disciplinas.objects.all()
    lista_professores = ['Professor(a)', 'Professor(a) AEE', 'Professor(a) de Multimeios']
    servidores = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao__in= lista_professores).values('id', 'contrato__servidor__nome').distinct().order_by('contrato__servidor__nome')

    #GAMBIARRA, APAGAR Futuramente e fazer da forma correta...
    professores = []
    nome = []
    for servidor in servidores:
        if servidor['contrato__servidor__nome'] not in nome:
            professores.append({'id': servidor['id'], 'contrato__servidor__nome': servidor['contrato__servidor__nome']})
        nome.append(servidor['contrato__servidor__nome'])

    if request.method == 'POST':
        formulario_grade_disciplina(request, edicao)
        if edicao:
            return HttpResponseRedirect(f'/administracao/turma_perfil?id={grade.turma.id}')
        else:
            return HttpResponseRedirect(f'/administracao/turma_perfil?id={turma.id}')

    return TemplateResponse(request, template_name, locals())


def deletar_grade(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    edicao = True
    id_grade = request.GET.get('id_grade')
    grade = Grade.objects.get(id= id_grade)

    excluir_disciplina(request, grade, edicao)

    return HttpResponseRedirect(f'/administracao/turma_perfil?id={grade.turma.id}')


def organizacao_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades/organizacao/organizacao_formulario.html'

    id_escola = request.GET.get('id')
    escola = Escola.objects.get(id= id_escola)
    edicao = False

    if Organizacao_escolar.objects.filter(escola= escola).exists():
        edicao = True
        organizacao = Organizacao_escolar.objects.get(escola= escola)

        if Organizacao_formas_organizacao.objects.filter(organizacao_escolar= organizacao).exists():
            formas_organizacao = Organizacao_formas_organizacao.objects.filter(organizacao_escolar= organizacao)
            formas = []
            for item in formas_organizacao:
                formas.append(item.tipo_organizacao)

        if Organizacao_instrumento_educativo.objects.filter(organizacao_escolar= organizacao).exists():
            instrumento_educativo = Organizacao_instrumento_educativo.objects.filter(organizacao_escolar= organizacao)
            instrumentos = []
            for item in instrumento_educativo:
                instrumentos.append(item.instrumento)

        if Organizacao_reserva_cota.objects.filter(organizacao_escolar= organizacao).exists():
            reserva_cota = Organizacao_reserva_cota.objects.filter(organizacao_escolar= organizacao)
            reserva = []
            for item in reserva_cota:
                reserva.append(item.tipo_cota)

        if Organizacao_colegiados_escola.objects.filter(organizacao_escolar= organizacao).exists():
            colegiados_escola = Organizacao_colegiados_escola.objects.filter(organizacao_escolar= organizacao)
            colegiados = []
            for item in colegiados_escola:
                colegiados.append(item.orgao_colegiado)

    if request.method == 'POST':
        formulario_organizacao_escolar(request, edicao)
        return HttpResponseRedirect(f'/administracao/organizacao_perfil?id={escola.id}')

    return TemplateResponse(request, template_name, locals())


def organizacao_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/organizacao/organizacao-perfil.html'
    user = request.session['username']

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    id_escola = request.GET.get('id')
    escola = Escola.objects.get(id= id_escola)

    if Organizacao_escolar.objects.filter(escola= escola).exists():
        organizacao = Organizacao_escolar.objects.get(escola= escola)

        if Organizacao_formas_organizacao.objects.filter(organizacao_escolar= organizacao).exists():
            formas_organizacao = Organizacao_formas_organizacao.objects.filter(organizacao_escolar= organizacao)
            formas = []
            for item in formas_organizacao:
                formas.append(item.tipo_organizacao)

        if Organizacao_instrumento_educativo.objects.filter(organizacao_escolar= organizacao).exists():
            instrumento_educativo = Organizacao_instrumento_educativo.objects.filter(organizacao_escolar= organizacao)
            instrumentos = []
            for item in instrumento_educativo:
                instrumentos.append(item.instrumento)

        if Organizacao_reserva_cota.objects.filter(organizacao_escolar= organizacao).exists():
            reserva_cota = Organizacao_reserva_cota.objects.filter(organizacao_escolar= organizacao)
            reservas = []
            for item in reserva_cota:
                reservas.append(item.tipo_cota)

        if Organizacao_colegiados_escola.objects.filter(organizacao_escolar= organizacao).exists():
            colegiados_escola = Organizacao_colegiados_escola.objects.filter(organizacao_escolar= organizacao)
            colegiados = []
            for item in colegiados_escola:
                colegiados.append(item.orgao_colegiado)

    return TemplateResponse(request, template_name, locals())


def unidade_historico(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    user = request.session['username']

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    id_escola = request.GET.get('id')
    endereco = Endereco.objects.get(escola__id= id_escola)

    escola = endereco.escola
    contatos = Contato.objects.filter(endereco__id= endereco.id)

    lista_contatos = []
    for contato in contatos:
        lista_contatos.append(contato.id)

    template_name = 'administracao/unidades/unidade_historico.html'

    historico_escola = Historico.objects.filter(tabela= 'administracao_escola', objeto= endereco.escola.id).order_by('-data')
    historico_endereco = Historico.objects.filter(tabela= 'administracao_endereco', objeto= endereco.id).order_by('-data')
    historico_contatos = Historico.objects.filter(tabela= 'administracao_contato', objeto__in= lista_contatos).order_by('-data')

    historico = []
    for item in historico_escola:
        historico.append(item)

    for item in historico_endereco:
        historico.append(item)

    for item in historico_contatos:
        historico.append(item)

    possui_historico = historico_escola.count() > 0 or historico_endereco.count() > 0 or  historico_contatos.count() > 0

    datas = []
    for acao in historico:
        data = acao.data.split(' ')

        if data[0] not in datas:
            datas.append(data[0])

    return TemplateResponse(request, template_name, locals())


def unidade_anexo(request):

    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades/unidade_anexo.html'

    municipios = global_municipios
    zoneamentos = global_zoneamentos

    id_escola = request.GET.get('id')
    escola = Escola.objects.get(id = id_escola)

    # modalidades = Modalidade.objects.all()
    etapas = Etapa.objects.all()
    dependencias = ['Estadual', 'Federal', 'Municipal', 'Privado']
    localizacao_diferenciada = ['', 'Terra Indígena', 'Quilombo', 'Área de Assentamento']

    #Consultando as etnias de ensino indigena para filtro
    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        etnias.append(detalhe['etnia'])

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        localizacoes.append(detalhe['localizacao'])

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        aldeias.append(detalhe['aldeia'])

    if request.method == 'POST':
        formulario_anexo(request, escola)
        return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={escola.cod_inep}')


    return TemplateResponse(request, template_name, locals())


def aluno_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/turma/aluno_formulario.html'
    user = request.session['username']


    id_turma = request.GET.get('id')
    edicao = False
    turma = Turmas.objects.get(id= id_turma)

    generos = [('M', 'Masculino'), ('F', 'Feminino'), ('T', 'Transgênero'), ('N', 'Não binário'), ('O', 'Outro')]

    # Carregando estados e cidades para atualizar a naturalidade dos alunos
    estados = Estado.objects.filter(id= 1)
    cidades = Cidade.objects.filter(estado_id= 1).order_by('nome')

    if request.method == 'POST':
        formulario_aluno(request, edicao)
        return HttpResponseRedirect(f'/administracao/turma_perfil?id={turma.id}')

    return TemplateResponse(request, template_name, locals())


def aluno_perfil(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades/turma/aluno_perfil.html'

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    id_aluno = request.GET.get('id')
    alunos_turma = Aluno_turma.objects.filter(aluno= id_aluno)

    for aluno_turma in alunos_turma:
        aluno = aluno_turma.aluno
        turma = aluno_turma.turma
        escola = turma.endereco.escola

    professores_aee = Professor_aluno.objects.filter(aluno = id_aluno).values_list('professor', flat=True)
    servidores = Servidor_lotacao.objects.filter(id__in= professores_aee, status= 1).values('contrato__servidor__nome', 'contrato__cargo__nome', 'carga_horaria')

    return TemplateResponse(request, template_name, locals())


def vincular_professor_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades/turma/vincular_professor_formulario.html'

    id_aluno = request.GET.get('id_aluno')
    aluno = Aluno.objects.get(id= id_aluno)
    turma = aluno.turma
    endereco = turma.endereco

    professores = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Professor(a) AEE').values('id', 'contrato__servidor__nome').distinct().order_by('contrato__servidor__nome')

    if request.method == "POST":
        formulario_vincular_professor(request, aluno)
        return HttpResponseRedirect(f'/administracao/aluno_perfil?id={id_aluno}')

    return TemplateResponse(request, template_name, locals())


def unidade_consulta(request):
    if verificar_manutencao() or not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/unidade-consulta.html'
    user = request.session['username']

    base_unidade = Endereco.objects.all().values('escola__cod_inep')

    inep = request.GET.get('inep')

    if inep:
        unidade = Endereco.objects.get(escola__cod_inep= inep)

    if request.method == 'POST':
        inep_unidade = request.POST.get('inep')

        if Endereco.objects.filter(escola__cod_inep= inep_unidade).exists():
            unidade = Endereco.objects.filter(escola__cod_inep= inep_unidade)[0]
            return HttpResponseRedirect(f'unidade-consulta?inep={inep_unidade}')
        else:
            return HttpResponseRedirect(f'unidade_formulario?inep={inep_unidade}')

    return TemplateResponse(request, template_name, locals())


def ouvidoria_unidade(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'administracao/unidades/ouvidoria/unidade-ouvidoria.html'

    id_escola= request.GET.get('id')
    escola= Escola.objects.filter(id=id_escola).values('id', 'nome_escola', 'cod_inep').last()
    estado_civil=[]
    cores=[]
    tempo_gestacao=[]
    orientacao_sexual=[]
    identidade_genero=[]
    nacionalidades=[]

    return TemplateResponse(request, template_name, locals())