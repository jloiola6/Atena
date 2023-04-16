from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import *
from .action import *

from aplicacoes.administracao.models import *
from aplicacoes.atena.models import Estado, Cidade
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.dinem.relatorios import *
from aplicacoes.dinem.filtros import *
from aplicacoes.coex.models import *
from aplicacoes.lotacao.models import *
from aplicacoes.dinem.actions.aluno_boletim import *

# Create your views here.
def index(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if Permissao.objects.filter(usuario__login= request.session['username'], servico= 4).exists():
        permissao = Permissao.objects.get(usuario__login= request.session['username'], servico= 4)
        inep = Gestor_Escolar.objects.get(permissao= permissao)
        return HttpResponseRedirect(f'/dinem/unidade_perfil?inep={inep}')

    if not verificacao_maxima(request, [3]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'dinem/index.html'

    enderecos = filtro_dinem(request)
    quantidade_escolas = len(enderecos)

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
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

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if "page" not in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

    return TemplateResponse(request, template_name, locals())

# VIEW PARA A PÁGINA DE SELEÇÃO DE ENDEREÇO DE ESCOLAS QUE POSSUEM ANEXO
def unidade_anexos(request, inep):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'dinem/unidade-anexos.html'

    user = request.session['username']

    try:
        escola = Escola.objects.get(cod_inep= inep)
    except:
        return HttpResponseRedirect('/dinem')

    enderecos = Endereco.objects.filter(escola= escola).order_by('-tipo')

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexos = enderecos.count() > 1

    if not possui_anexos:
        return HttpResponseRedirect(f'/dinem/unidade_perfil?inep={inep}')

    return TemplateResponse(request, template_name, locals())

# VIEW PARA A PÁGINA DE PERFIL DE UMA UNIDADE
def unidade_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')

    template_name = 'dinem/unidade-perfil.html'

    user = request.session['username']

    # DEFININDO CONSTANTES PARA O ANO LETIVO E ETAPAS DE ENSINO
    ANO_LETIVO = '2022'
    ETAPAS = [5, 6]

    # VARIÁVEIS NECESSÁRIAS PARA A CONSTRUÇÃO DA PARTIAL DE PERFIL DE UNIDADE
    aplicacao = 'DINEM'

    cod_inep = request.GET.get('inep')
    id_endereco = request.GET.get('id_endereco')

    try:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 1)
    except:
        permissao = Permissao.objects.get(usuario__login= user, servico__id= 5)

    try:
        escola = Escola.objects.get(cod_inep= cod_inep)
    except:
        return HttpResponseRedirect('/dinem')

    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    # VERIFICANDO SE A ESCOLA POSSUI ANEXOS
    possui_anexo = Endereco.objects.filter(escola= escola).count() > 1

    # CASO A ESCOLA POSSUA ANEXOS E NENHUM AINDA TENHA SIDO SELECIONADO, ENCAMINHAR PARA A PÁGINA DE SELEÇÃO DE ANEXOS
    if possui_anexo and not id_endereco:
        return HttpResponseRedirect(f'/dinem/unidade-anexos/{cod_inep}')

    # INICIALIZANDO O ENDEREÇO NO CASO DE UM ANEXO TER SIDO SELECIONADO OU CASO A ESCOLA NÃO POSSUA
    try:
        if id_endereco:
            endereco = Endereco.objects.get(escola= escola, id= id_endereco)
        else:
            endereco = Endereco.objects.get(escola= escola)
    except:
        return HttpResponseRedirect('/dinem')

    # INICIALIZANDO OS DADOS DO COMITE EXECUTIVO DE ACORDO COM A ESCOLA
    if Coex.objects.filter(escola= escola, status=1).exists():
        coex = Coex.objects.get(escola= escola)

        if Consorcio.objects.filter(cnpj= coex.cnpj).exists():
            consorcio = Consorcio.objects.get(cnpj= coex.cnpj)

    # INICIALIZANDO OS CONTATOS DA UNIDADE DE ACORDO COM O ENDEREÇO
    contatos = Contato.objects.filter(endereco= endereco)

    # INICIALIZANDO OS DADOS DA EQUIPE GESTORA DA UNIDADE
    diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
        diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).exists():
        pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
        ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
        administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
        secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    # FIM DAS VARIÁVEIS NECESSÁRIAS PARA A PARTIAL

    turmas = Turmas.objects.filter(endereco= endereco, etapa__in=ETAPAS, ano_letivo= ANO_LETIVO)
    quantidade_turmas = turmas.count()

    if turmas:
        # LISTANDO AS ETAPAS DE ENSINO MÉDIO
        turmas_etapas = escola_etapas.filter(etapa__id__in= ETAPAS)

        # LISTANDO AS SÉRIES COM TOTAL DE ALUNOS
        turmas_series = turmas.values('etapa', 'ano_serie').order_by('ano_serie').distinct()

        for serie in turmas_series:
            qtd_alunos = Aluno_turma.objects.filter(turma__ano_letivo= ANO_LETIVO ,turma__endereco= endereco, turma__etapa= serie['etapa'], turma__ano_serie= serie['ano_serie']).count()
            serie['qtd_alunos'] = qtd_alunos

        turmas = turmas.order_by('nome')

    return TemplateResponse(request, template_name, locals())

# VIEW PARA A PÁGINA DE TURMAS DE UMA UNIDADE
def unidade_turmas(request, id_endereco):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')

    template_name = 'dinem/unidade-turmas.html'

    user = request.session['username']

    # DEFININDO CONSTANTES PARA O ANO LETIVO E ETAPAS DE ENSINO
    ETAPAS = [5, 6]

    try:
        endereco = Endereco.objects.get(id= id_endereco)
    except:
        return HttpResponseRedirect('/dinem')

    escola = endereco.escola
    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    possui_turmas = Turmas.objects.filter(endereco= endereco).exists()
    turmas = Turmas.objects.filter(endereco= endereco).order_by('nome')

    if possui_turmas:
        # LISTANDO OS ANOS LETIVOS COM BASE NAS TURMAS CADASTRADAS
        anos_letivos = Turmas.objects.filter(endereco= endereco).values('ano_letivo').distinct().order_by('-ano_letivo')

        # LISTANDO AS ETAPAS COM BASE NOS ANOS LETIVOS DAS TURMAS CADASTRADAS
        etapas_turmas = Turmas.objects.filter(endereco= endereco, etapa__id__in= ETAPAS).values('etapa', 'etapa__nome', 'ano_letivo').distinct()

        # LISTANDO AS SÉRIES COM BASE NAS ETAPAS DE ENSINO
        series_turmas = Turmas.objects.filter(endereco= endereco, etapa__in=ETAPAS).values('etapa', 'etapa__nome', 'ano_letivo', 'ano_serie').order_by('ano_serie').distinct()

    return TemplateResponse(request, template_name, locals())

# VIEW PARA A PÁGINA DE UMA TURMA
def turma_perfil(request, id_turma):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'dinem/turma_perfil.html'

    # id_turma = request.GET.get('id')
    turma = Turmas.objects.get(id= id_turma)

    # alunos = Aluno_turma.objects.filter(turma= turma, status= 1).order_by('aluno__nome')
    alunos = Aluno_turma.objects.filter(turma= turma).values('id', 'aluno__id', 'aluno__nome', 'aluno__nascimento', 'aluno__sexo').order_by('aluno__nome')
    qtd_alunos = alunos.count()

    ids = []
    for aluno in alunos:
        qtd_relatorios = RelatorioFinal.objects.filter(aluno__id= aluno['aluno__id']).count()
        if turma.ano_serie == '3ª Série':
            if qtd_relatorios == 3:
                aluno['situacao'] = 'Finalizado'
                ids.append(qtd_relatorios)
            elif qtd_relatorios == 0:
                aluno['situacao'] = 'Pendente'
            elif qtd_relatorios < 3:
                aluno['situacao'] = 'Parcial'

        elif turma.ano_serie == '1ª Série' or turma.ano_serie == '2ª Série':
            if qtd_relatorios == 1:
                aluno['situacao'] = 'Finalizado'
                ids.append(qtd_relatorios)
            elif qtd_relatorios == 0:
                aluno['situacao'] = 'Pendente'
        
        # elif turma.ano_serie == '2ª Série':
        #     if qtd_relatorios == 2:
        #         aluno['situacao'] = 'Finalizado'
        #         ids.append(qtd_relatorios)
        #     elif qtd_relatorios == 0:
        #         aluno['situacao'] = 'Pendente'
        #     elif qtd_relatorios == 1:
        #         aluno['situacao'] = 'Parcial'

        # elif turma.ano_serie == '1ª Série':
        #     if qtd_relatorios == 1:
        #         aluno['situacao'] = 'Finalizado'
        #         ids.append(qtd_relatorios)
        #     elif qtd_relatorios == 0:
        #         aluno['situacao'] = 'Pendente'
      
    if alunos.count() == len(ids):
        btn_relatorio = True
    else:
        btn_relatorio = False

    # relatorio = RelatorioFinal.objects.filter(aluno__turma= turma).values('aluno__id').distinct()
    # ids = []
    # for item in relatorio:
    #     ids.append(int(item['aluno__id']))

    # relatorio_alunos = []
    # for aluno in alunos:
    #     if aluno.id in ids:
    #         relatorios = RelatorioFinal.objects.filter(aluno__id= aluno.id).count()
    #         if relatorios == 3:
    #             relatorio_alunos.append((aluno, 'Finalizado'))
    #         elif relatorios > 3:
    #             relatorio_alunos.append((aluno, 'Parcial'))
    #     else:
    #         relatorio_alunos.append((aluno, 'Pendente'))


    # if alunos.count() == len(ids):
    #     btn_relatorio = True
    # else:
    #     btn_relatorio = False

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

    grades = Grade.objects.filter(turma= turma)

    possui_grades = len(grades) > 0

    return TemplateResponse(request, template_name, locals())

def aluno_perfil(request, id_aluno_turma): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')
    user = request.session['username']
    template_name = 'dinem/aluno_perfil.html'

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    try:
        aluno_turma = Aluno_turma.objects.get(id= id_aluno_turma)
    except:
        return HttpResponseRedirect('/dinem')

    aluno = aluno_turma.aluno
    turma = aluno_turma.turma
    cpf_aluno = f'{aluno.cpf[0:3]}.{aluno.cpf[3:6]}.{aluno.cpf[6:9]}-{aluno.cpf[9:11]}'

    # Verificando a existêcia do dado de nome do pai do aluno
    possui_pai = aluno.nome_pai != ''

    relatorios = RelatorioFinal.objects.filter(aluno= aluno).order_by('etapa')

    if turma.ano_serie == '3ª Série':
        historico = relatorios.count() == 3
        if not historico:
            etapas_pendentes = ['1ª Série', '2ª Série', '3ª Série']

            for relatorio in relatorios:
                etapa = relatorio.etapa

                if etapa in etapas_pendentes:
                    etapas_pendentes.remove(etapa)
    elif turma.ano_serie == '2ª Série':
        historico = relatorios.count() == 1
        if not historico:
            etapas_pendentes = ['2ª Série']

            for relatorio in relatorios:
                etapa = relatorio.etapa

                if etapa in etapas_pendentes:
                    etapas_pendentes.remove(etapa)
    # elif turma.ano_serie == '2ª Série':
    #     historico = relatorios.count() == 2
    #     if not historico:
    #         etapas_pendentes = ['1ª Série', '2ª Série']

    #         for relatorio in relatorios:
    #             etapa = relatorio.etapa

    #             if etapa in etapas_pendentes:
    #                 etapas_pendentes.remove(etapa)
    elif turma.ano_serie == '1ª Série':
        historico = relatorios.count() == 1
        if not historico:
            etapas_pendentes = ['1ª Série']

            for relatorio in relatorios:
                etapa = relatorio.etapa

                if etapa in etapas_pendentes:
                    etapas_pendentes.remove(etapa)
    
    if request.POST:
        try:
            enturmacao = Aluno_turma.objects.get(id= id_aluno_turma)
            enturmacao.delete()
            return HttpResponseRedirect(f'/dinem/turma_perfil/{turma.id}')
        except:
            pass

    return TemplateResponse(request, template_name, locals())


def aluno_formulario(request, id_aluno_turma): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')

    template_name = 'dinem/aluno_formulario.html'
    user = request.session['username']

    aluno_turma = Aluno_turma.objects.get(id= id_aluno_turma)

    if aluno_turma != None:
        edicao = True
        aluno = aluno_turma.aluno
        turma = aluno_turma.turma
        data_aluno = aluno_turma.aluno.nascimento
    else:
        edicao = False
        turma = aluno_turma.turma

    generos = [('M', 'Masculino'), ('F', 'Feminino'), ('T', 'Transgênero'), ('N', 'Não binário'), ('O', 'Outro')]

    if request.method == 'POST':
        formulario_aluno(request, edicao, aluno, turma)
        if edicao:
            return HttpResponseRedirect(f'/dinem/aluno_perfil/{aluno_turma.id}')

        return HttpResponseRedirect(f'/dinem/turma_perfil/{aluno_turma.id}')

    return TemplateResponse(request, template_name, locals())

def aluno_boletim(request, id_aluno_turma, etapa): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [3, 4]):
        return HttpResponseRedirect('/')

    template_name = 'dinem/aluno-boletim/aluno_boletim.html'
    # template_name = 'dinem/aluno_boletim.html'
    user = request.session['username']

    aluno_turma = Aluno_turma.objects.get(id= id_aluno_turma)
    aluno = aluno_turma.aluno
    turma = aluno_turma.turma
    resultados = [('APROVADO', 'Aprovado'), ('APROVADO COM DEPENDÊNCIA', 'Aprovado com Dependência'), ('REPROVADO', 'Reprovado')]

    edicao = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa).exists()
    if edicao:
        relatorio = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)

    if request.method == 'POST':
        situacao = request.POST.get('resultado')
        # formulario_relatorio_aluno(request, edicao)
        formulario_aluno_boletim(request, turma, aluno, etapa, edicao)
        return HttpResponseRedirect(f'/dinem/aluno_perfil/{aluno_turma.id}')

    return TemplateResponse(request, template_name, locals())