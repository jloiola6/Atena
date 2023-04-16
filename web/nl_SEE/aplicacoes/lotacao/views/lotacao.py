from __future__ import print_function
from re import template
from traceback import print_tb
from aplicacoes.administracao.models import *
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.actions.lotacao import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import Etapa, Disciplinas
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from aplicacoes.lotacao.exportar import *

def lotacoes(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    #Template referente a view
    template_name = 'lotacao/lotacao/lotacoes.html'

    #Usuario logado
    user = request.session['username']
    
    # Verificar se existe filtragem de acordo a URL da página
    filtro = '?' in str(request.build_absolute_uri()) and str(request.build_absolute_uri()).split('?')[-1] != 'cpf=&matricula=&nome=' and str(request.build_absolute_uri()).split('?')[-1] != 'tipo=&cargo=&subconta=&funcao=&administrativa=&educacional=&municipio=&regiao=' and str(request.build_absolute_uri()).split('?')[-1] != 'data=&data-final='

    #Verficar se o filtro está ativo para mostrar o Butão de Exportar no Template
    if filtro:
        if 'page=' in str(request.build_absolute_uri()):
            filtro = False
        else:
            for i in str(request.build_absolute_uri()).split('&')[1:]:
                if i[-1] != '=':
                    filtro = True


    #Função de Filtro s
    lotacoes = filtro_lotacao(request)

    # Dados de preenchimento para o modal
    consulta_lotacao = Servidor_lotacao.objects.all().values('unidade_adm__id', 'unidade_adm__nome', 'unidade_adm__sigla', 'unidade_escolar__escola__id','unidade_escolar__escola__nome_escola', 'contrato__cargo__id', 'contrato__cargo__nome', 'funcao', 'unidade_escolar__municipio', 'unidade_escolar__municipio', 'unidade_escolar__regiao').order_by('unidade_escolar__municipio')

    unidades_adm = Servidor_lotacao.objects.all().values('unidade_adm__id', 'unidade_adm__nome', 'unidade_adm__sigla').exclude(unidade_adm__isnull= True).distinct().order_by('unidade_adm__nome')

    unidades_educacionais = Servidor_lotacao.objects.all().values('unidade_escolar__escola__id','unidade_escolar__escola__nome_escola', 'unidade_escolar__municipio').exclude(unidade_escolar__escola__nome_escola= None).distinct().order_by('unidade_escolar__escola__nome_escola')

    municipios = Servidor_lotacao.objects.all().values_list('unidade_escolar__municipio', flat= True).exclude(unidade_escolar__municipio= None).distinct().order_by('unidade_escolar__municipio')

    regional = Servidor_lotacao.objects.all().values_list('unidade_escolar__regiao', flat= True).exclude(unidade_escolar__regiao= None).distinct().order_by('unidade_escolar__regiao')

    tipo_lotacoes = Servidor_lotacao.objects.all().values('tipo_lotacao').exclude(tipo_lotacao= None).distinct()

    cargos = Servidor_lotacao.objects.all().values('contrato__cargo__id', 'contrato__cargo__nome').distinct()

    subcontas = Servidor_lotacao.objects.all().values('subconta__id', 'subconta__sub', 'subconta__fonte').distinct()

    funcoes = Servidor_lotacao.objects.all().values('funcao').distinct()


    #Paginação
    quantidade_lotacoes = len(lotacoes)
    page = request.GET.get('page')

    if page is None:
        page = 1

    valor_paginacao = 15*int(page)

    lotacoes_aux = lotacoes[valor_paginacao-15:valor_paginacao]

    # Dados para o detalhes da lotação
    for lotacao in lotacoes_aux:
        lotacao['enturmacao_escola'] = Grade.objects.filter(professor= lotacao['id'], status= 1)
        lotacao['enturmacao_alunos'] = Professor_aluno.objects.filter(professor= lotacao['id'], status= 1)
        lotacao['enturmacao_disciplinas_adm'] = Grade_professor_adm.objects.filter(professor= lotacao['id'], status= 1)

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

    if request.method == 'POST':
        return exportar_pdf_lotacao_tabela(request, quantidade_lotacoes)

    return TemplateResponse(request, template_name, locals())

def lotacao_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/lotacao/lotacao-formulario/lotacao-formulario.html'
    user = request.session['username']
    data_atual = date.today()

    ANO_LETIVO = '2023'

    id_contrato = request.GET.get('id_contrato')

    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    tipo_lotacao = request.GET.get('tipo-lotacao')
    tipo_unidade = request.GET.get('tipo-unidade')

    id_unidade = request.GET.get('unidade')
    funcao = request.GET.get('funcao')

    erro = request.GET.get('erro')

    if tipo_unidade == 'escolar':
        unidade = Endereco.objects.get(id= id_unidade)
    else:
        unidade = Unidade_administrativa.objects.get(id= id_unidade)

    subcontas = Servidor_subconta.objects.all().order_by('sub')

    # Consultas para caso a função do servidor seja Professor
    if tipo_unidade == 'escolar' and (funcao == 'Professor(a)' or funcao == 'Professor(a) AEE' or funcao == 'Coordenador(a) Pedagógico(a) de Anos'):
        escola = unidade.escola
        turmas = Turmas.objects.filter(endereco= unidade, ano_letivo = ANO_LETIVO).order_by('nome')
        etapas = Etapa_escola.objects.filter(escola= escola).order_by('etapa_id')

    if tipo_unidade == 'escolar' and (funcao == 'Atendente Pessoal' or funcao == 'Atendimento Domiciliar' or funcao == 'Interprete' or funcao == 'Mediador' or funcao == 'Professor(a) Brailista'):
        escola = unidade.escola
        turmas = Turmas.objects.filter(endereco= unidade, ano_letivo = ANO_LETIVO).order_by('nome')
        etapas = Etapa_escola.objects.filter(escola= escola).order_by('etapa_id')


    disciplinas = Disciplinas.objects.all().order_by('nome')

    estados = Estado.objects.all().order_by('nome')
    cidades = Cidade.objects.all().order_by('nome')

    rotas = ['CHSA', 'CNT', 'LGG', 'MAT']
    unidades_chsa = ['2U1S1', '2U2S1', '2U3S1', '2U4S1', '2U1S2', '2U2S2', '2U3S2', '2U4S2', '3U1S1', '3U2S1', '3U3S1', '3U4S1', '3U5S1', '3U6S1', '3U1S2', '3U2S2', '3U3S2', '3U4S2', '3U5S2', '3U6S2']
    unidades_cnt = ['2U1S1', '2U2S1', '2U3S1', '2U4S1', '2U1S2', '2U2S2', '2U3S2', '2U4S2', '3U1S1', '3U2S1', '3U3S1', '3U4S1', '3U5S1', '3U6S1', '3U1S2', '3U2S2', '3U3S2', '3U4S2', '3U5S2', '3U6S2']
    unidades_lgg = ['2U1S1', '2U2S1', '2U3S1', '2U4S1', '2U1S2', '2U2S2', '2U3S2', '2U4S2', '3U1S1', '3U2S1', '3U3S1', '3U4S1', '3U5S1', '3U1S2', '3U2S2', '3U3S2', '3U4S2', '3U5S2']
    unidades_mat = ['2U1S1', '2U2S1', '2U3S1', '2U4S1', '2U1S2', '2U2S2', '2U3S2', '2U4S2', '3U1S1', '3U2S1', '3U3S1', '3U4S1', '3U5S1', '3U1S2', '3U2S2', '3U3S2', '3U4S2', '3U5S2']

    orgaos = ['Secretaria Adjunta de Administração', 'CREF - Conselho Regional de Educação Física', 'TRF1 - Tribunal Regional Federal da 1° Região', 'Prefeitura Municipal de Porto Velho', 'Câmara Municipal de São Luiz do Quintude - Alagoas', 'Ministério Público Federal', 'Câmara dos Deputados - Distrito Federal', 'Prefeitura de Nova Iguaçu - Rio de Janeiro', 'COLONACRE - Companhia de Desenvolvimento Agrário e Colonização do Acre', 'Vara da Infância e Juventude', 'TCE - Tribunal de Contas do Estado do Acre', 'Senado Federal', 'Governo do Estado de Goiás', 'UFAC - Universidade Federal do Acre','TJAC - Tribunal de Justiça do Estado do Acre','SINPROACRE - Sindicato dos Professores de Rede Pública de Ensino do Estado do Acre','SINTEAC - Sindicato dos Trabalhadores em Educação do Acre','SINTAE - Sindicato dos Técnicos Administrativos e Apoio Administrativos Educacionais do Acre','SEGOV – Secretaria Extraordinária de Assuntos Governamentais','ALEAC – Assembleia Legislativa do Estado do Acre', 'TRE – Tribunal Regional Eleitoral', 'Governo do Estado da Paraíba', 'Governador', 'Vice Governador', 'PGE – Procuradoria Geral do Estado', 'CGE – Controladoria Geral do Estado', 'DPE – Defensoria Pública Geral do Estado', 'OAB – Ordem dos Advogados do Brasil', 'Chefe do Gabinete Militar', 'MPAC – Ministério Público do Estado do Acre', 'Subchefe do Gabinete Militar', 'Representação em Brasilia', 'Comandante Geral da Policia Militar', 'Subcomandante Geral da Policia Militar', 'Corpo de Bombeiros', 'SECC – Secretaria de Estado da Casa Civil', 'SEPLAG – Secretaria de Estado de Planejamento e Gestão', 'SEICT – Secretaria de Estado de Indústria, Ciência e Tecnologia', 'SEINFRA – Secretaria de Estado de Infraestrutura', 'SECOM – Secretaria de Estado de Comunicação', 'SESACRE – Secretaria de Estado da Saúde', 'SEE – Secretaria de Estado da Educação, Cultura e Esportes', 'SEJUSP – Secretaria de Estado da Justiça e Segurança Pública', 'SEET – Secretaria de Estado de Empreendedorismo e Turismo', 'SEMAPI – Secretaria de Estado do Meio Ambiente e das Políticas Indígenas', 'SEPA – Secretaria de Estado de Produção e Agronegócio', 'SEASDHM – Secretaria de Estado de Assistência Social dos Direitos Humanos e de Políticas para Mulheres', 'SEDUR – Secretaria de Estado de Desenvolvimento Urbano e Regional', 'PCAC – Policia Civil do Estado do Acre', 'SEFAZ – Secretaria de Estado de Fazenda', 'ACREPREVIDÊNCIA – Instituto de Previdência do Estado do Acre', 'JUCEAC – Junta Comercial do Estado do Acre', 'DERACRE – Departamento de Estradas de Rodagens do Acre', 'IMAC – Instituto de Meio Ambiente do Acre', 'SANEACRE – Serviço de Água e Esgoto do Estado do Acre', 'IMC – Instituto de Mudanças Climáticas e Regulação de Serviços Ambientais', 'DETRAN – Departamento Estadual de Trânsito do Acre', 'IDAF – Instituto de Defesa Agropecuária e Florestal do Estado do Acre', 'ITERACRE – Instituto de Terras do Acre', 'IAPEN – Instituto de Administração Penitenciária', 'IAIS – Instituto de Assistência e Inclusão Social', 'ISE – Instituto Socioeducativo do Estado do Acre', 'AGEAC – Agência Reguladora de Serviços Públicos do Estado do Acre', 'OCA – Organização em Centros de Atendimento', 'PROCON – Instituto de Proteção e Defesa do Consumidor', 'IEPTEC – Instituto de Educação Profissional e Tecnológica', 'FUNTAC – Fundação de Tecnologia do Estado do Acre', 'FEM – Fundação de Cultura Elias Mansour', 'FUNDHACRE – Fundação Hospital Estadual do Acre', 'FDRHCD – Fund. de Desenv. de Recursos Humanos da Cultura e do Desporto do Estado do Acre', 'FUNDAC – Fundação Aldeia de Comunicação do Acre', 'ACREDATA – Empresa de Processamento de Dados', 'CODISACRE – Companhia de Desenvolvimento Industrial do Estado do Acre', 'CAGEACRE – Companhia de Armazéns Gerais e Entrepostos do Acre', 'EMATER – Empresa de Assistência Técnica e Extensão Rural do Acre', 'SANACRE – Companhia de Saneamento do Acre', 'CILA – Companhia Industrial de Laticínios do Acre', 'ANAC – Agência de Negócios do Estado do Acre S/A', 'COHAB – Companhia de Habitação do Acre', 'CDSA – Companhia de Desenvolvimento e Serviços Ambientais', 'AZPE/AC – Administradora da Zona de Processamento de Exportação do Acre S/A', 'SEME de Acrelândia', 'Prefeitura de Acrelândia', 'SEME de Assis Brasil', 'Prefeitura de Assis Brasil', 'SEME de Brasiléia', 'Prefeitura de Brasiléia', 'SEME de Bujari', 'Prefeitura de Bujari', 'SEME de Capixaba', 'Prefeitura de Capixaba', 'SEME de Cruzeiro do Sul', 'Prefeitura de Cruzeiro do Sul', 'SEME de Epitaciolândia', 'Prefeitura de Epitaciolândia', 'SEME de Feijó', 'Prefeitura de Feijó', 'SEME de Jordão', 'Prefeitura de Jordão', 'SEME de Manoel Urbano', 'Prefeitura de Manoel Urbano', 'SEME de Marechal Thaumaturgo', 'Prefeitura de Marechal Thaumaturgo', 'SEME de Mâncio Lima', 'Prefeitura de Mâncio Lima', 'SEME de Plácido de Castro', 'Prefeitura de Plácido de Castro', 'SEME de Porto Acre', 'Prefeitura de Porto Acre', 'SEME de Porto Walter', 'Prefeitura de Porto Walter', 'SEME de Rio Branco', 'Prefeitura de Rio Branco', 'SEME de Rodrigues Alves', 'Prefeitura de Rodrigues Alves', 'SEME de Santa Rosa do Purus', 'Prefeitura de Santa Rosa do Purus', 'SEME de Sena Madureira', 'Prefeitura de Sena Madureira', 'SEME de Senador Guiomard', 'Prefeitura de Senador Guiomard', 'SEME de Tarauacá', 'Prefeitura de Tarauacá', 'SEME de Xapuri', 'Prefeitura de Xapuri', 'MDIC - Ministério do Desenvolvimento, Indústria, Comércio e Serviços - Brasília', 'SEAD - Secretaria de Estado de Administração', 'SEAGRI - SECRETARIA DE ESTADO DE AGRICULTURA']
    orgaos.sort()

    if request.method == 'POST':
        edicao = False
        if formulario_lotacao(request, edicao, contrato, tipo_lotacao, tipo_unidade, unidade, funcao):
            return HttpResponseRedirect(f'contrato-perfil/{contrato.id}')
        else:
            url = str(request.build_absolute_uri()).split('/lotacao/')[1]
            return HttpResponseRedirect(f'{url}&erro=repetido')


    return TemplateResponse(request, template_name, locals())

def subconta_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/lotacao/subconta-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor
        lotacoes = Servidor_lotacao.objects.filter(contrato= contrato)

    if request.method == 'POST':
        formulario_subconta(request)
        return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())

def turma_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/lotacao/turma-formulario.html'
    user = request.session['username']
    turnos = ['Matutino', 'Vespertino', 'Noturno', 'Integral']
    serie_fundamental1 = ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano']
    serie_fundamental2 = ['6º Ano', '7º Ano', '8º Ano', '9º Ano']
    serie_medio = ['1ª Série', '2ª Série', '3ª Série']

    turmas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    modulos = ['Módulo I', 'Módulo I - A', 'Módulo I - B', 'Módulo II', 'Módulo II - A', 'Módulo II - B', 'Módulo III', 'Módulo III - A', 'Módulo III - B', 'Módulo IV', 'Módulo IV - A', 'Módulo IV - B', 'Módulo V', 'Módulo V - A', 'Módulo V - B']

    id_contrato = request.GET.get('id_contrato')
    id_endereco = request.GET.get('id')
    contrato = Servidor_contrato.objects.get(id= id_contrato)
    servidor = contrato.servidor
    endereco = Endereco.objects.get(id= id_endereco)
    escola = endereco.escola

    etapa_escola = Etapa_escola.objects.filter(escola= escola)
    id_etapas = []
    for item in etapa_escola:
        id_etapas.append(item.etapa.id)

    etapas = Etapa.objects.filter(id__in= id_etapas)

    if request.method == "POST":
        formulario_turma(request, endereco)
        return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())

def aluno_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/lotacao/aluno-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    contrato = Servidor_contrato.objects.get(id= id_contrato)
    servidor = contrato.servidor

    id_turma = request.GET.get('id_turma')
    turma = Turmas.objects.get(id= id_turma)
    escola = turma.endereco

    generos = [('M', 'Masculino'), ('F', 'Feminino'), ('T', 'Transgênero'), ('N', 'Não binário'), ('O', 'Outro')]

    # Carregando estados e cidades para atualizar a naturalidade dos alunos
    estados = Estado.objects.filter()
    cidades = Cidade.objects.filter(estado_id= 1).order_by('nome')

    if request.method == 'POST':
        formulario_aluno(request, turma)
        return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={contrato.id}')

    return TemplateResponse(request, template_name, locals())

def lotacoes_filtros(request):
    if verificar_manutencao() or not verificacao_maxima(request, [15]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/lotacao/filtros-avancados.html'
    user = request.session['username']

    cargos = Servidor_lotacao.objects.all().values('contrato__cargo__id', 'contrato__cargo__nome').distinct()
    unidades_adm = Servidor_lotacao.objects.exclude(unidade_adm__isnull= True).values('unidade_adm__id', 'unidade_adm__nome', 'unidade_adm__sigla').distinct().order_by('unidade_adm__nome')
    unidades_educacionais = Servidor_lotacao.objects.exclude(unidade_escolar__isnull= True).values('unidade_escolar__escola__id','unidade_escolar__escola__nome_escola', 'unidade_escolar__municipio').exclude(unidade_escolar__escola__nome_escola= None).distinct().order_by('unidade_escolar__escola__nome_escola')
    municipios = Servidor_lotacao.objects.all().values_list('unidade_escolar__municipio', flat= True).exclude(unidade_escolar__municipio= None).distinct().order_by('unidade_escolar__municipio')
    regionais = Servidor_lotacao.objects.all().values_list('unidade_escolar__regiao', flat= True).exclude(unidade_escolar__regiao= None).distinct().order_by('unidade_escolar__regiao')
    subcontas = Servidor_lotacao.objects.all().values('subconta__id', 'subconta__sub', 'subconta__fonte').exclude(subconta__sub = None).distinct()
    funcoes = Servidor_lotacao.objects.all().values('funcao').exclude(funcao='').exclude(funcao = None).distinct().order_by('funcao')
    disciplinas = Grade.objects.exclude(status= 0).exclude(professor__isnull= True).values('disciplina__nome').distinct()
    etapas = Grade.objects.all().values('turma__etapa__id', 'turma__etapa__nome').exclude(turma__etapa__nome= None).distinct()
    tipo_lotacoes = Servidor_lotacao.objects.all().values_list('tipo_lotacao', flat= True).exclude(tipo_lotacao= None).distinct()

    get = request.build_absolute_uri().split('?')
    if len(get) > 1:
        return HttpResponseRedirect(f'/lotacao/lotacoes?{get[1]}')

    return TemplateResponse(request, template_name, locals())