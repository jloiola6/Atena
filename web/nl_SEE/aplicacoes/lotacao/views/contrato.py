from dataclasses import asdict
from pydoc import text
from xml.dom.pulldom import SAX2DOM
from aplicacoes.atena.models import Cidade
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.actions.contrato import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.administracao.models import Grade, Professor_aluno
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from datetime import *

from aplicacoes.usuario.models import Permissao
from aplicacoes.lotacao.exportar import *
from aplicacoes.lotus.models import Servidor_lotacao as Lotacao_lotus, Servidor_lotacao_turma as Turma_lotus, Servidor_ocorrencia as Ocorrencia_lotus, Servidor_contrato as Lotus_contrato, Servidor_contrato_aditivo as Lotus_contrato_aditivo
# from aplicacoes.lotacao.tests import inativador_de_datas
data = datetime.now()

def contratos(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/contratos.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login = user, servico__id = 14)

    filtro = False
    if '?' in request.build_absolute_uri() and str(request.build_absolute_uri()).split('?')[-1] != 'cargo=&carga_horaria=&tipo_contrato=&situacao=&municipio=' and str(request.build_absolute_uri()).split('?')[-1] != 'cpf=&matricula=&nome=':
        if 'page=' in str(request.build_absolute_uri()):
            for i in str(request.build_absolute_uri()).split('&')[1:]:
                if i[-1] != '=':
                    filtro = True
        else:
            filtro = True


    contratos = filtro_contrato(request)
    contratos1 = filtro_contrato(request)
    quantidade_contratos = contratos.count()
    cargos = Servidor_contrato.objects.all().values('cargo__nome').exclude(cargo__nome= None).distinct()
    carga_horarias = Servidor_contrato.objects.all().values('cargo__carga_horaria').exclude(cargo__carga_horaria= None).distinct()
    tipo_contratos = Servidor_contrato.objects.all().values('tipo_contrato').exclude(tipo_contrato= None).distinct()
    municipios = Servidor_contrato.objects.all().values('municipio').exclude(municipio= None).distinct()
    situacoes = Servidor_contrato.objects.all().values('situacao').exclude(situacao= None).distinct()
    # contratosAd = Servidor_ocorrencia_funcional.objects.filter().values('id', 'contrato__id', 'data_termino')
    # contratosinativar = []

    # for i in contratosAd:
    #     if inativador_de_datas(i['data_termino']):
    #         contratosinativar.append(i['id'])

    page = request.GET.get('page')
    if page is None:
        page = '1'

    paginator = Paginator(contratos, 15)
    contratos = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():

        gets = (request.get_full_path().split('?')[1])

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if 'page' not in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

    if request.method == 'POST':
        return exportar_pdf_contratos(request, contratos1, quantidade_contratos)

    return TemplateResponse(request, template_name, locals())


def contratos_filtros(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/filtros-avancados.html'
    user = request.session['username']
    cargos = Servidor_contrato.objects.all().values('cargo__id','cargo__nome', 'cargo').distinct().exclude(cargo__isnull= True)
    cargas_horarias = Servidor_contrato.objects.all().values('cargo__carga_horaria').distinct()
    tipos_contratos = Servidor_contrato.objects.all().values('cargo__tipo').distinct().exclude(cargo__isnull= True)
    municipios = Servidor_contrato.objects.all().values('municipio').distinct().exclude(municipio__isnull= True)
    situacoes = Servidor_contrato.objects.all().values('situacao').distinct().exclude(situacao__isnull= True)
    disciplina_convocacao = Servidor_contrato.objects.all().values('disciplina_convocacao__id', 'disciplina_convocacao__nome', 'disciplina_convocacao').distinct().exclude(disciplina_convocacao__isnull= True)
    diario_homologacao = Servidor_contrato.objects.all().values('diario_homologacao').distinct().exclude(diario_homologacao__isnull= True)

    get = request.build_absolute_uri().split('?')
    if len(get) > 1:
        return HttpResponseRedirect(f'/lotacao/contratos?{get[1]}')

    return TemplateResponse(request, template_name, locals())


def contrato_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/contrato-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    id_servidor = request.GET.get('id_servidor')

    usuarios_excluir = ['joaopedro.passos', 'erick.nascimento', 'josecarlos.souza', 'franklin.farias', 'rute.neres', 'fabio.santos', 'gustavo.lima', 'vitor.daniel']
    # Caso o id do contrato seja passado via GET o formulário vai abrir em modo edição

    if id_contrato != None:
        edicao = True
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor
        data_convocacao = str(contrato.data_convocacao)
        data_contrato = str(contrato.data_contrato)
        data_inicio = str(contrato.data_inicio)

    # Caso o id do servidor seja passado via GET o formulário procede normalmente
    elif id_servidor != None:
        servidor = Servidor.objects.get(id= id_servidor)

        edicao = False


    tipo_contrato = request.GET.get('tipo_contrato')

    if tipo_contrato != 'ESTAGIÁRIO':
        id_cargo = request.GET.get('id_cargo')
        cargo = Cargo.objects.get(id= id_cargo)


        disciplinas = Disciplinas.objects.all().exclude(id__in= [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])

    cargos = Cargo.objects.all()
    tipos_contratos = ('EFETIVO', 'TEMPORÁRIO', 'COMISSÃO', 'CONTRATAÇÃO DIRETA', 'PERMUTA', 'ESTAGIÁRIO', 'CEDIDO')
    cidades = Cidade.objects.filter(estado= 1)
    situacoes = ('EM EXERCÍCIO', 'EXONERADO/RESCISO', 'APOSENTADO', 'CEDIDO', 'EXONERADO', 'FALECIDO', 'LICENCIADO', 'AFASTADO')

    if request.method == 'POST':
        contrato = formulario_contrato(request, edicao, servidor)
        if contrato:
            return HttpResponseRedirect(f'contrato-perfil/{contrato.id}')
        else:
            return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def contrato_perfil_antigo(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/contrato-perfil copy.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 14)

    usuarios_excluir = ['joaopedro.passos', 'erick.nascimento', 'josecarlos.souza', 'franklin.farias', 'rute.neres', 'gustavo.lima', 'fabio.santos', 'vitor.daniel']

    permissao_lotacao =  Permissao.objects.filter(usuario__login = user, servico__id = 15, editar = 1).exists()
    permissao_VF = Permissao.objects.filter(usuario__login = user, servico__id = 23, editar = 1).exists()
    permissao_VDP = Permissao.objects.filter(usuario__login = user, servico__id = 24, editar = 1).exists()

    id_contrato = request.GET.get('id_contrato')
    id_contrato_lotus = request.GET.get('id_contrato_lotus')

    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

        if Contrato_cancelamento.objects.filter(contrato= contrato).exists():
            qr_documentos = Contrato_cancelamento.objects.filter(contrato= contrato)
            documentos = []

            for documento in qr_documentos:
                formato_documento = str(documento.documento).split('.')[1]
                caminho = str(documento.path_arquivo())
                dict_documento = {'id': documento.id, 'formato': formato_documento, 'caminho': caminho}
                documentos.append(dict_documento)

        # DADOS PARA O MODAL DE FORMULÁRIO DE LOTAÇÃO
        enderecos = Endereco.objects.all().order_by('escola__nome_escola')
        unidades_administrativas = Unidade_administrativa.objects.all().exclude(id=1)
        funcoes = Funcao.objects.all().order_by('nome')

        if contrato.cargo:
            if not "PROFESSOR" in contrato.cargo.nome:
                funcoes = funcoes.exclude(id__in= [56, 66, 81])


        if Servidor_endereco.objects.filter(servidor= servidor).exists():
            servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

        lotacoes_lotus = Lotacao_lotus.objects.filter(matricula= servidor.matricula, digito= contrato.digito).order_by('-data_inicio')
        turma_lotus = Turma_lotus.objects.filter(matricula= servidor.matricula, digito= contrato.digito)

        lotacoes = []
        for lotacao in Servidor_lotacao.objects.filter(contrato= contrato).order_by('-id'):

            if Grade_professor_adm.objects.filter(professor= lotacao.id).exists():
                professor_adm = Grade_professor_adm.objects.get(professor= lotacao.id)
                lotacoes.append((lotacao, None, None, professor_adm))

            elif Grade.objects.filter(professor= lotacao.id).exists():
                grades = []

                turnos = Grade.objects.filter(professor= lotacao.id, disciplina__isnull= False).values_list('turma__turno', flat= True).distinct()
                for disciplina in Grade.objects.filter(professor= lotacao.id, disciplina__isnull= False).values_list('disciplina__nome', flat= True).distinct():
                    for turno in turnos:
                        turmas = ''
                        if Grade.objects.filter(professor= lotacao.id, disciplina__nome= disciplina, turma__turno= turno).exists():
                            for ano_serie in Grade.objects.filter(professor= lotacao.id, disciplina__nome= disciplina, turma__turno= turno).values_list('turma__ano_serie', flat= True).distinct():
                                for turma in Grade.objects.filter(professor= lotacao.id, disciplina__nome= disciplina, turma__turno= turno, turma__ano_serie= ano_serie).values_list('turma__nome', flat= True).distinct():
                                    if len(turmas) > 0:
                                        turmas += ', '+ turma
                                    else:
                                        turmas = turma
                            texto = f'{disciplina} | {turno} | {turmas}'
                            grades.append(texto)

                for rota in Grade.objects.filter(professor= lotacao.id, disciplina__isnull= True).values_list('rota', flat= True).distinct():
                    if lotacao.funcao != 'Professor(a) AEE' and lotacao.funcao != 'Coordenador(a) Pedagógico(a) de Anos':
                        texto = f'{rota} | '
                    else:
                        texto = ''
                    for turno in ['Matutino', 'Vespertino', 'Noturno', 'Integral']:
                        if Grade.objects.filter(professor= lotacao.id, rota= rota, turma__turno= turno).exists():
                            texto += f'{turno} | '
                            for ano_serie in Grade.objects.filter(professor= lotacao.id, rota= rota, turma__turno= turno).values_list('turma__ano_serie', flat= True).distinct():
                                texto += f'{ano_serie} ('
                                for turma in Grade.objects.filter(professor= lotacao.id, rota= rota, turma__turno= turno, turma__ano_serie= ano_serie).values_list('turma__nome', flat= True).distinct():
                                    texto += f'{turma[-1]}, '
                                texto = texto[:-2]
                                texto += ')'
                                grades.append(texto)
                                if lotacao.funcao != 'Professor(a) AEE' and lotacao.funcao != 'Coordenador(a) Pedagógico(a) de Anos':
                                    texto = f'{rota} | {turno} | '
                                else:
                                    texto = f'{turno} | '

                lotacoes.append((lotacao, grades, None, None))

            elif Professor_aluno.objects.filter(professor= lotacao.id).exists():
                aluno = Professor_aluno.objects.filter(professor= lotacao.id)
                lotacoes.append((lotacao, None, aluno, None))
            else:
                lotacoes.append((lotacao, None, None, None))


        ultima_lotacao = Servidor_lotacao.objects.filter(contrato= contrato).last()

        if Servidor_ocorrencia_funcional.objects.filter(contrato= contrato).exists():
            ocorrencias = Servidor_ocorrencia_funcional.objects.filter(contrato= contrato)

        if servidor.matricula != None:
            contrato_id = f'{servidor.matricula.strip()}-{contrato.digito}'
            ocorrencias_lotus = Ocorrencia_lotus.objects.filter(contrato__contains= contrato_id)

        if Servidor_hora_complementar.objects.filter(contrato= contrato).exists():
            hora_complementar = Servidor_hora_complementar.objects.filter(contrato= contrato)

        if Servidor_gratificacao.objects.filter(contrato= contrato).exists():
            gratificacoes = Servidor_gratificacao.objects.filter(contrato= contrato)

        if Servidor_contrato_aditivo.objects.filter(contrato= contrato).exists():
            aditivos = Servidor_contrato_aditivo.objects.filter(contrato= id_contrato, status= 1)
            ultimo_aditivo = Servidor_contrato_aditivo.objects.filter(contrato= id_contrato, status= 1).last()

        if Lotus_contrato_aditivo.objects.filter(cpf= servidor.cpf, digito= contrato.digito).exists():
            aditivos_lotus = Lotus_contrato_aditivo.objects.filter(cpf= servidor.cpf, digito= contrato.digito)

        if Servidor_vdp.objects.filter(contrato= contrato).exists():
            vdps = Servidor_vdp.objects.filter(contrato= contrato)

    elif id_contrato_lotus != None:
        id_contrato = None
        contrato = Lotus_contrato.objects.get(id= id_contrato_lotus)

        if Servidor.objects.filter(matricula= contrato.matricula).exists():
            servidor = Servidor.objects.get(matricula= contrato.matricula)
        elif Servidor.objects.filter(cpf= contrato.cpf).exists():
            servidor = Servidor.objects.get(cpf= contrato.cpf)

        lotacoes_lotus = Lotacao_lotus.objects.filter(matricula= servidor.matricula, digito= contrato.digito)
        turma_lotus = Turma_lotus.objects.filter(matricula= servidor.matricula, digito= contrato.digito)

        if servidor.matricula != None:
            contrato_id = f'{servidor.matricula.strip()}-{contrato.digito}'
            ocorrencias_lotus = Ocorrencia_lotus.objects.filter(contrato= contrato_id)

        if Lotus_contrato_aditivo.objects.filter(id_contrato= id_contrato_lotus).exists():
            aditivos_lotus = Lotus_contrato_aditivo.objects.filter(id_contrato= id_contrato_lotus)
    else:
        return HttpResponseRedirect('/')

    if contrato.cargo != None and not lotacoes_lotus:
        cargo = Cargo.objects.get(nome=contrato.cargo)
        if cargo.vencimento == 0.0:
            contrato_vencimento = Servidor_contrato.objects.get(id = id_contrato)
            data = str(contrato_vencimento.data_inicio).split('-')
            ano_atual = datetime.today().strftime('%Y')

            teste = int(ano_atual) - int(data[0])
            referencia = 1
            referencia = referencia + teste//3

            data_referencia = str(ano_atual + '-' +data[1] + '-' + data[2])

    # Consultas para alimentar o modal para o formulário de contrato
    cargos = Cargo.objects.all()
    tipos_contratos = ('EFETIVO', 'TEMPORÁRIO', 'COMISSÃO', 'CONTRATAÇÃO DIRETA', 'PERMUTA', 'CEDIDO', 'ESTAGIÁRIO')


    cargos_efetivos = Cargo.objects.filter(tipo='EFETIVO')
    cargos_temporario = Cargo.objects.filter(tipo='TEMPORÁRIO')
    cargos_comissao = Cargo.objects.filter(tipo='COMISSÃO')
    cargos_permuta = Cargo.objects.filter(tipo='PERMUTA/CEDIDO')

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'contrato':
            return exportar_pdf_contrato(request, user, contrato)
        
        if request.POST.get('exportar-fieldset-formatos') == 'cancelamento':
            return pdf_contrato_cancelamento(request, user, contrato)
        
        if request.POST.get('termo_cancelamento') == 'termo_cancelamento':
            cancelamento_contrato(request, contrato)
            return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

        if 'btn-exportar' in request.POST:
            valor = request.POST.get('btn-exportar')

            # if valor == 'exportar-contrato':
            #     return exportar_pdf_contrato(request, user, contrato)
            if valor == 'exportar-aditivo':
                return exportar_pdf_aditivo(request, contrato, servidor)
            elif valor == 'Lotus-contrato':
                return exportar_lotus_contrato(request, user, contrato, id_contrato_lotus)
            elif 'exportar-memorando' in valor:
                id_lotacao = valor.split('-')[-1]
                return exportar_pdf_lotacao(request, id_lotacao, user)

        elif 'btn-formulario-lotacao' in request.POST:
            requisicao = request.POST

            tipo_lotacao = requisicao.get('tipo-lotacao')
            tipo_unidade = requisicao.get('tipo-unidade')

            if tipo_unidade == 'escolar':
                unidade = requisicao.get('endereco')
                funcao = requisicao.get('funcao_escolar')
            else:
                unidade = requisicao.get('administrativa')
                funcao = requisicao.get('funcao_adm')

            if tipo_lotacao == 'Sem Lotação':
                funcao = ''

            elif tipo_lotacao == 'Cedido' or tipo_lotacao == 'Permuta':
                funcao = requisicao.get('funcao')


            return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={id_contrato}&tipo-lotacao={tipo_lotacao}&tipo-unidade={tipo_unidade}&unidade={unidade}&funcao={funcao}')

        elif 'btn-excluir' in request.POST:
            valor = request.POST.get('btn-excluir')
            id_lotacao = valor.split('-')[-1]
            lotacao_excluir(request, id_lotacao)
            return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

        elif request.POST.get('btn-excluir-contrato') == 'excluir-contrato':
            excluir_contrato(request, id_contrato)
            return HttpResponseRedirect(f'/lotacao/servidor-perfil?id={servidor.id}')

        elif 'btn-excluir-aditivo' in request.POST:
            valor = request.POST.get('btn-excluir-aditivo')
            id_aditivo = valor.split('-')[-1]
            excluir_contrato_aditivo(request, id_aditivo)
            return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

        elif 'btn-exportar-lotus' in request.POST:
            valor = request.POST.get('btn-exportar-lotus')
            id_lotacao = valor.split('-')[-1]

            if 'lotus-' in valor:
                return exportar_lotacao_lotus(request, user, servidor, id_lotacao)

        elif 'btn-contrato-formulario' in request.POST:
            tipo_contrato = request.POST.get('tipo')

            if tipo_contrato != 'ESTAGIÁRIO':

                if tipo_contrato =='EFETIVO':
                    cargo = request.POST.get('cargos-efetivos')
                elif tipo_contrato == 'TEMPORÁRIO':
                    cargo = request.POST.get('cargos-temporarios')
                elif tipo_contrato == 'CONTRATAÇÃO DIRETA':
                    cargo = request.POST.get('cargos-contratacao-direta')
                elif tipo_contrato == 'COMISSÃO':
                    cargo = request.POST.get('cargos-comissaos')
                elif tipo_contrato == 'PERMUTA':
                    cargo = request.POST.get('cargos-permutas')
                elif tipo_contrato == 'CEDIDO':
                    cargo = request.POST.get('cargos-cedido')

                return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_contrato={id_contrato}&tipo_contrato={tipo_contrato}&id_cargo={cargo}')

            # Caso o tipo de contrato seja 'ESTAGIÁRIO' ele não passará cargo via GET
            return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_contrato={id_contrato}&tipo_contrato={tipo_contrato}')
    # lotacoes = lotacoes[-1: 0: -1]
    return TemplateResponse(request, template_name, locals())


# VIEW PARA O PERFIL DE UM CONTRATO
def contrato_perfil(request, id_contrato):
    if verificar_manutencao() or not verificacao_maxima(request, [14]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/contrato-perfil.html'
    user = request.session['username']
    
    # OBJETO DA PERMISSÃO DO SERVIÇO DE CONTRATOS
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 14)
    permissao_VF = Permissao.objects.filter(usuario__login = user, servico__id = 23, editar = 1).exists()

    # LISTANDO AS PERMISSÕES DO USUÁRIO
    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__id', flat= True)

    # VERIFICANDO PERMISSÃO PARA A ADIÇÃO DE NOVAS LOTAÇÕES
    permissao_lotacao =  Permissao.objects.filter(usuario__login = user, servico__id = 15, editar = 1).exists()

    try:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
    except:
        return HttpResponseRedirect('/lotacao')
    
    # ENCAPSULANDO O OBJETO DO SERVIDOR DO CONTRATO
    servidor = contrato.servidor

    # VERIFICANDO SE O SERVIDOR POSSUI ENDEREÇO CADASTRADO
    possui_endereco = Servidor_endereco.objects.filter(servidor= servidor).exists()

    # CONSULTAS PARA ALIMENTAR O MODAL PARA O FORMULÁRIO DE CONTRATO
    cargos = Cargo.objects.all()
    tipos_contratos = ('EFETIVO', 'TEMPORÁRIO', 'COMISSÃO', 'CONTRATAÇÃO DIRETA', 'PERMUTA', 'CEDIDO', 'ESTAGIÁRIO')


    cargos_efetivos = Cargo.objects.filter(tipo='EFETIVO')
    cargos_temporario = Cargo.objects.filter(tipo='TEMPORÁRIO')
    cargos_comissao = Cargo.objects.filter(tipo='COMISSÃO')
    cargos_permuta = Cargo.objects.filter(tipo='PERMUTA/CEDIDO')

    # BUSCANDO LOTAÇÕES DO CONTRATO UTILIZANDO VALUES PARA TRATAMENTO DOS DADOS
    lotacoes = Servidor_lotacao.objects.filter(contrato= contrato, status__in= [0, 1]).values().order_by('-status' ,'-id')

    for lotacao in lotacoes:
        lotacao['turno'] = []

        # ADICIONANDO O NOME DAS UNIDADES
        if lotacao['unidade_escolar_id']:
            lotacao['unidade_escolar'] = Endereco.objects.get(id= lotacao['unidade_escolar_id'])
        elif lotacao['unidade_adm_id']:
            lotacao['unidade_adm'] = Unidade_administrativa.objects.get(id= lotacao['unidade_adm_id'])

        if lotacao['funcao'] == 'Professor(a)' and lotacao['unidade_adm_id']:
            lotacao['disciplinas'] = Grade_professor_adm.objects.filter(professor= lotacao['id'])

        # ADICIONANDO AS TURMAS CASO A FUNÇÃO SEJA DE PROFESSOR
        if lotacao['funcao'] in ['Professor(a)', 'Professor(a) AEE', 'Coordenador(a) Pedagógico(a) de Anos'] and lotacao['unidade_escolar_id']:
            lotacao['turmas'] = Grade.objects.filter(professor= lotacao['id'], turma__ano_letivo= lotacao['ano_referencia'])

        # ADICIONANDO OS ALUNOS CASO A FUNÇÃO SEJA CORRESPONDENTE
        if lotacao['funcao'] in ['Mediador', 'Atendente Pessoal', 'Atendimento Domiciliar', 'Interprete', 'Professor(a) Brailista'] and lotacao['unidade_escolar_id']:
            ids_alunos = Professor_aluno.objects.filter(professor= lotacao['id']).values_list('aluno__id', flat= True).distinct()

            alunos = Aluno_turma.objects.filter(aluno_id__in= ids_alunos, turma__ano_letivo= lotacao['ano_referencia'])
            lotacao['alunos'] = alunos
            
    qtd_lotacoes = lotacoes.count()

    # DADOS PARA O MODAL DE FORMULÁRIO DE LOTAÇÃO
    enderecos = Endereco.objects.all().order_by('escola__nome_escola')
    unidades_administrativas = Unidade_administrativa.objects.all().exclude(id=1)
    funcoes = Funcao.objects.all().order_by('nome')

    if contrato.cargo:
        if not "PROFESSOR" in contrato.cargo.nome:
            funcoes = funcoes.exclude(id__in= [56, 66, 81])
    
    # Verifica se o servidor possui endereço cadastrado
    servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)
        
    # Ocorrência funcional 
    ocorrencias = Servidor_ocorrencia_funcional.objects.filter(contrato= contrato)

    # Aditivar contrato
    aditivos = Servidor_contrato_aditivo.objects.filter(contrato= id_contrato, status= 1)
    ultimo_aditivo = Servidor_contrato_aditivo.objects.filter(contrato= id_contrato, status= 1).last()

    # DETECTANDO SUBMISSÃO DE FORMULÁRIO NA PÁGINA
    if request.POST:
        # SUBMISSÃO PARA A EXPORTAÇÃO DE UM CONTRATO
        if 'exportar-contrato' in request.POST:
            if request.POST.get('exportar-contrato') == 'contrato':
                return exportar_pdf_contrato(request, user, contrato)
            
            elif request.POST.get('exportar-contrato') == 'cancelamento':
                return pdf_contrato_cancelamento(request, user, contrato)

        # SUBMISSÕES RELACIONADAS ÀS LOTAÇÕES DO CONTRATO

        # EXPORTAÇÃO DE UM MEMORANDO
        if 'btn-exportar-memorando' in request.POST:
            id_lotacao = request.POST.get('btn-exportar-memorando')
            return exportar_pdf_lotacao(request, id_lotacao, user)
        
        # EXPORTAÇÃO DE UM ADITIVO
        if request.POST.get('btn-exportar') == 'exportar-aditivo':
            return exportar_pdf_aditivo(request, contrato, servidor)


        # EXCLUSÃO DE UMA LOTAÇÃO
        if 'btn-excluir' in request.POST:
            id_lotacao = request.POST.get('btn-excluir')
            lotacao_excluir(request, id_lotacao)

            return HttpResponseRedirect(f'/lotacao/contrato-perfil/{id_contrato}')     
        
        # ADIÇÃO DE UMA LOTAÇÃO
        if 'btn-formulario-lotacao' in request.POST:
            requisicao = request.POST

            tipo_lotacao = requisicao.get('tipo-lotacao')
            tipo_unidade = requisicao.get('tipo-unidade')

            if tipo_unidade == 'escolar':
                unidade = requisicao.get('endereco')
                funcao = requisicao.get('funcao_escolar')
            else:
                unidade = requisicao.get('administrativa')
                funcao = requisicao.get('funcao_adm')

            if tipo_lotacao == 'Sem Lotação':
                funcao = ''

            elif tipo_lotacao == 'Cedido' or tipo_lotacao == 'Permuta':
                funcao = requisicao.get('funcao')

            return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={id_contrato}&tipo-lotacao={tipo_lotacao}&tipo-unidade={tipo_unidade}&unidade={unidade}&funcao={funcao}')
        
    return TemplateResponse(request, template_name, locals())


def ocorrencia_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [23], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/ocorrencia-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    id_ocorrencia = request.GET.get('id_ocorrencia')

    if id_contrato != None:
        edicao = False
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    if id_ocorrencia != None:
        edicao = True   
        dados_ocorrencia = Servidor_ocorrencia_funcional.objects.get(id=id_ocorrencia,contrato_id=id_contrato, status=1)
    
    if request.method == 'POST':
        formulario_ocorrencia(request,  contrato, edicao, id_ocorrencia)
        return HttpResponseRedirect(f'/lotacao/contrato-perfil/{id_contrato}')

    return TemplateResponse(request, template_name, locals())


def cargo_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/cargo-formulario.html'
    user = request.session['username']

    id_servidor = request.GET.get('id_servidor')
    id_contrato = request.GET.get('id_contrato')
    niveis = ['FUNDAMENTAL', 'MAGISTÉRIO',  'MÉDIO', 'MÉDIO - MAGISTÉRIO', 'MÉDIO PROFISSIONAL', 'MÉDIO REGULAR', 'SUPERIOR', 'SUPERIOR EM LICENCIATURA CURTA', 'SUPERIOR SEM LICENCIATURA']

    if request.method == "POST":
        formulario_cargo(request)
        if id_servidor != None:
            return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_servidor={id_servidor}')
        else:
            return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_contrato={id_contrato}')

    return TemplateResponse(request, template_name, locals())


def complemento_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/complemento-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    if request.method == 'POST':
        formulario_complemento_hora(request, contrato)
        return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

    return TemplateResponse(request, template_name, locals())


def gratificacao_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/gratificacao-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    if request.method == 'POST':
        formulario_gratificacao(request, contrato)
        return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

    return TemplateResponse(request, template_name, locals())


def finalizar_contrato(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/finalizar-contrato.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    id_lotacao = request.GET.get('id_lotacao')
    if id_contrato == None and id_lotacao == None:
        return HttpResponseRedirect('/')

    if id_contrato:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor
        lotacao = None
    else:
        lotacao = Servidor_lotacao.objects.get(id = id_lotacao)
        contrato = lotacao.contrato
        servidor = contrato.servidor

    if request.method == 'POST':
        contrato_finalizar(request, id_contrato, lotacao)
        # if id_contrato:
        #     return HttpResponseRedirect(f'/lotacao/lotacao-formulario?id_contrato={id_contrato}')
        # else:
        return HttpResponseRedirect(f'/lotacao/contrato-perfil/{contrato.id}')

    return TemplateResponse(request, template_name, locals())


def aditivo_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [14], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/aditivo-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    if request.method == 'POST':
        formulario_aditivo(request, contrato)
        return HttpResponseRedirect(f'/lotacao/contrato-perfil/{id_contrato}')

    return TemplateResponse(request, template_name, locals())


def vdp_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [24], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/contrato/vdp-formulario.html'
    user = request.session['username']

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato = Servidor_contrato.objects.get(id= id_contrato)
        servidor = contrato.servidor

    if request.method == 'POST':
        formulario_vdp(request, contrato)
        return HttpResponseRedirect(f'/lotacao/contrato-perfil?id_contrato={id_contrato}')

    return TemplateResponse(request, template_name, locals())