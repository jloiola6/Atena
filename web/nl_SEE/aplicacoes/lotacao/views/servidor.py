from datetime import datetime
from traceback import print_tb
from aplicacoes.atena.models import Cidade
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.usuario.models import Permissao, Logs
from aplicacoes.lotacao.exportar import *
from aplicacoes.terceirizacao.models import Contrato_lotacao
from aplicacoes.lotus.models import Servidor_contrato as Lotus_contrato, Servidor_lotacao as Lotus_lotacao, Servidor_curriculo as Lotus_curriculo


def servidores(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidores.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 8)

    page = request.GET.get('page')
    if page is None:
        page = 1

    servidores = filtro_servidores(request)
    quantidade_servidores = servidores.count()
    paginator = Paginator(servidores, 15)
    servidores = paginator.get_page(page)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_servidores(request)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_servidores(request)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        if len(gets.split('&')) > 1:
            #Paginação + filtros passados pela url
            proxima_pagina = str(int(page)+1)
            pagina_anterior = str(int(page)-1)

            gets = f'page={page}&' + gets

            gets_primeira = gets.replace(f'page={page}', 'page=1')
            gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
            gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
            gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

    return TemplateResponse(request, template_name, locals())


def servidor_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-formulario.html'
    user = request.session['username']

    hoje = datetime.now()

    cpf = request.GET.get('cpf')
    cidades_acre = Cidade.objects.filter(estado__id = 1).order_by('estado__nome')

    if request.method == 'POST':
        formulario_servidor(request)
        servidor = Servidor.objects.get(cpf = cpf)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8]):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-perfil.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = 8)
    permissao_VF = Permissao.objects.filter(usuario__login = user, servico__id = 23, editar = 1).exists()

    if Permissao.objects.filter(usuario__login = user, servico__id = 14, editar = 1).exists():
        permissao_contrato = True

    usuarios_excluir = ['joaopedro.passos', 'erick.nascimento', 'josecarlos.souza', 'franklin.farias', 'rute.neres', 'gustavo.lima', 'fabio.santos']

    id_servidor = request.GET.get('id')
    if id_servidor == None or id_servidor =='' or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    servidor = Servidor.objects.get(id= id_servidor)

    historico_base = Atualizacao_cadastral.objects.filter(servidor=servidor.id).last()

    if historico_base:
        historico_realizado = Logs.objects.filter(id=historico_base.log)
        print('-'*100)
        print(historico_realizado[0].id)
        historico_login = historico_realizado[0].usuario.login

    cpf_vf = f'{servidor.cpf[0:3]}.{servidor.cpf[3:6]}.{servidor.cpf[6:9]}-{servidor.cpf[9:11]}'
    cpf = f'{servidor.cpf[0:3]}******-{servidor.cpf[9:13]}'

    if Contrato_lotacao.objects.filter(servidor= servidor).exists():
        servidor_contrato_terceirizado = True
        contrato_lotacoes = Contrato_lotacao.objects.filter(servidor= servidor).values('id', 'endereco__escola__nome_escola', 'data_inicio', 'data_termino', 'unidade_administrativa__nome', 'item__contrato__id', 'item__contrato__numero_contrato', 'item__numero_item', 'item__descricao', 'item__valor_unitario', 'status').distinct().order_by('-status')

        contrato_lotacao = []
        ids_contratos = []
        for contrato in contrato_lotacoes:
            if contrato['item__contrato__id'] not in ids_contratos:
                contrato_lotacao.append(contrato)
                ids_contratos.append(contrato['item__contrato__id'])
        contrato_lotacao = contrato_lotacao[::-1]

        ultimo_contrato = Contrato_lotacao.objects.filter(servidor= servidor, status= 1).last()
    else:
        servidor_contrato_terceirizado = False

    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

    if Servidor_contato.objects.filter(servidor= servidor).exists():
        servidor_contato = Servidor_contato.objects.filter(servidor= servidor)

    if Servidor_banco.objects.filter(servidor= servidor).exists():
        servidor_banco = Servidor_banco.objects.get(servidor= servidor)

    digitos_contratos = []
    if Servidor_contrato.objects.filter(servidor= servidor).exists():
        servidor_contrato = Servidor_contrato.objects.filter(servidor= servidor).order_by('situacao', '-digito')
        digitos_contratos = servidor_contrato.values_list('digito', flat= True)

    contratos_lotus = Lotus_contrato.objects.filter(matricula= servidor.matricula, cpf= servidor.cpf).exclude(digito__in= digitos_contratos)
    lotacoes_lotus = Lotus_lotacao.objects.filter(matricula= servidor.matricula).order_by('-data_inicio')

    # BUSCANDO AS LOTAÇÕES DO SERVIDOR DA CASA
    if Servidor_lotacao.objects.filter(contrato__servidor= servidor).exists():
        servidor_lotacoes = Servidor_lotacao.objects.filter(contrato__servidor= servidor)

        lotacoes = servidor_lotacoes.values('id', 'unidade_escolar', 'unidade_escolar__escola__nome_escola', 'unidade_adm__nome', 'funcao', 'data_inicio', 'data_termino', 'status', 'motivo').order_by('-id')

        for lotacao in lotacoes:
            autorizacao = Autorizacao_lotacao.objects.filter(lotacao= lotacao['id'])

            if(autorizacao):
                lotacao['autorizador'] = autorizacao[0].autorizador

    if Servidor_documento.objects.filter(servidor= servidor).exists():
        qtd_documentos = Servidor_documento.objects.filter(servidor = servidor).count()
        qr_documentos = Servidor_documento.objects.filter(servidor = servidor)[0:3]

        documentos = []

        for documento in qr_documentos:
            formato_documento = str(documento.documento).split('.')[1]
            caminho = str(documento.path_arquivo())
            dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
            documentos.append(dict_documento)

    if Servidor_escolaridade.objects.filter(servidor= servidor).exists():
        escolaridade_atena = Servidor_escolaridade.objects.filter(servidor= servidor)
    if Lotus_curriculo.objects.filter(cpf= servidor.cpf).exists():
        escolaridade_lotus = Lotus_curriculo.objects.filter(cpf= servidor.cpf)

    cargos = Cargo.objects.filter(situacao = "ATIVO")
    tipos_contratos = ('EFETIVO', 'TEMPORÁRIO', 'COMISSÃO', 'CONTRATAÇÃO DIRETA', 'PERMUTA', 'CEDIDO', 'ESTAGIÁRIO')
    situacoes = ('AFASTADO', 'APOSENTADO', 'CEDIDO', 'EM EXERCÍCIO', 'EXONERADO/RESCISO', 'EXONERADO', 'FALECIDO', 'LICENCIADO')

    cargos_efetivos = Cargo.objects.filter(tipo='EFETIVO')
    cargos_temporario = Cargo.objects.filter(tipo='TEMPORÁRIO')
    cargos_comissao = Cargo.objects.filter(tipo='COMISSÃO').exclude(id__in = [60, 61, 62, 63, 64, 65, 66])
    cargos_permuta = Cargo.objects.filter(tipo='PERMUTA/CEDIDO')

    if request.method == 'POST':
        if request.POST.get('btn-excluir-servidor') == 'excluir-servidor':
            excluir_servidor(request, servidor)
            return HttpResponseRedirect(f'servidores')

        if request.POST.get('btn-exportar') == 'exportar':
            return exportar_pdf_declaracao(request, servidor)

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

                print(cargo)
                return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_servidor={id_servidor}&tipo_contrato={tipo_contrato}&id_cargo={cargo}')


            # Caso o tipo de contrato seja 'ESTAGIÁRIO' ele não passará cargo via GET
            return HttpResponseRedirect(f'/lotacao/contrato-formulario?id_servidor={id_servidor}&tipo_contrato={tipo_contrato}')
    return TemplateResponse(request, template_name, locals())


def servidor_contatos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-contatos.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)

    contatos = Servidor_contato.objects.filter(servidor= servidor)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        edicao = False
        editar_contatos(request, edicao)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')


    return TemplateResponse(request, template_name, locals())


def servidor_banco(request):
    if verificar_manutencao() or not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-banco.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')

    if id_servidor != None:
        edicao = False
        servidor = Servidor.objects.get(id= id_servidor)
    else:
        edicao = True
        id_servidor_banco = request.GET.get("id_servidor_banco")
        servidor_banco = Servidor_banco.objects.get(id = id_servidor_banco)
        servidor = servidor_banco.servidor

    tipos = ("Conta corrente", "Conta salário" , "Conta poupança")

    if request.method == 'POST':
        formulario_servidor_banco(request, edicao, servidor)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')


    return TemplateResponse(request, template_name, locals())


def servidor_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-endereco.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')

    if id_servidor != None:
        edicao= False
        servidor = Servidor.objects.get(id= id_servidor)
    else:
        edicao= True
        id_servidor_endereco = request.GET.get('id_servidor_endereco')
        servidor_endereco = Servidor_endereco.objects.get(id = id_servidor_endereco)
        servidor = servidor_endereco.servidor

    cidades = Cidade.objects.filter(estado__id= 1).order_by('estado__nome')

    if request.method == 'POST':
        formulario_servidor_endereco(request, edicao, servidor)
        return HttpResponseRedirect(f'/lotacao/servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_base(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-base.html'
    user = request.session['username']
    lotacao= True

    id_servidor = request.GET.get('id')

    if id_servidor != None:
        edicao= True
        servidor = Servidor.objects.get(id= id_servidor)
        servidor.data_nascimento = str(servidor.data_nascimento)

    generos = ("Masculino", "Feminino", "Não binário", "Outro")
    nacionalidades = ("Brasileiro(a)", "Estrangeiro(a)")

    if request.method == 'POST':
        formulario_servidor_base(request, edicao, servidor, lotacao)
        return HttpResponseRedirect(f'/lotacao/servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_consulta(request):
    if verificar_manutencao() or not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/servidor-consulta.html'
    user = request.session['username']

    base_cpf = Servidor.objects.all().values('cpf')

    id_servidor = request.GET.get('id')

    if id_servidor:
        servidor = Servidor.objects.get(id= id_servidor)
        cpf = servidor.cpf

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        cpf = re.sub('\D', '', cpf)

        if Servidor.objects.filter(cpf= cpf).exists():
            servidor = Servidor.objects.filter(cpf= cpf)[0]
            return HttpResponseRedirect(f'servidor-consulta?id={servidor.id}')
        else:
            return HttpResponseRedirect(f'servidor-formulario?cpf={cpf}')

    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [8], True):
        return HttpResponseRedirect('/')

    template_name = 'lotacao/servidor/documento-formulario.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)
    categorias = ['Comprovante de Residência','CNH', 'CPF', 'Passaporte', 'RG', 'Outros']
    qtd_documento = Servidor_documento.objects.filter(servidor= servidor).count()

    if request.method == 'POST':
        formulario_documento(request, servidor)
        if qtd_documento < 3:
            return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')
        else:
            return HttpResponseRedirect(f'gerenciador-documento?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def escolaridade(request):
    user = request.session['username']
    template_name = 'lotacao/servidor/escolaridade.html'
    usuario = Usuarios.objects.get(login = user)

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)

    formacoes = ["Ensino Médio", "Ensino Médio - Magistério", "Tecnólogo", "Bacharelado", "Licenciatura" ,"Doutorado", "Mestrado", "Pós-Graduação"]

    escolas = Escolas.objects.all().values_list('nome', flat= True)
    universidades = Instituicoes.objects.all()
    cursos = Cursos_graduacao.objects.all().values_list('nome', flat= True)
    cursos_magisterio = Cursos_graduacao.objects.filter(id__in=[2, 55, 306]).values_list('nome', flat= True)

    if request.method == 'POST':
        formulario_escolaridade(request, servidor)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def gerenciador_documento(request):
    template_name = 'lotacao/servidor/gerenciador-documento.html'

    user = request.session['username']

    servidor_id = request.GET.get('id')
    servidor = Servidor.objects.get(id= servidor_id)

    servidor_documento = Servidor_documento.objects.filter(servidor = servidor_id)

    documentos = []
    comprovante_reside = []
    cnh = []
    cpf = []
    passaporte = []
    rg = []
    outros = []

    for documento in servidor_documento:
        formato_documento = str(documento.documento).split('.')[1]

        caminho = str(documento.path_arquivo())
        dict_documento = {'id': documento.id, 'descricao': documento.descricao, 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
        documentos.append(dict_documento)

        if dict_documento['categoria'] == 'Comprovante de Residência':
            comprovante_reside.append(dict_documento)

        elif dict_documento['categoria'] == 'CNH':
            cnh.append(dict_documento)

        elif dict_documento['categoria'] == 'CPF':
            cpf.append(dict_documento)

        elif dict_documento['categoria'] == 'Passaporte':
            passaporte.append(dict_documento)

        elif dict_documento['categoria'] == 'RG':
            rg.append(dict_documento)

        elif dict_documento['categoria'] == 'Outros':
            outros.append(dict_documento)

    return TemplateResponse(request, template_name, locals())
