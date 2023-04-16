from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.tecnologia.models import Solicitacao_chamado, Solicitacao_tecnico
from aplicacoes.core.filtros import filtro_chamados
from .models import *
from django.core.paginator import Paginator

from aplicacoes.usuario.models import Permissao, Aplicacao
from aplicacoes.usuario.views import logout, verification
from aplicacoes.atena.models import Detalhes
from aplicacoes.core.models import *
from aplicacoes.lotacao.models import Servidor_documento
from aplicacoes.terceirizacao.models import Contrato_lotacao
from aplicacoes.administracao.models import Escola, Endereco
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.core.actions import *
from aplicacoes.atena.models import Cidade

from aplicacoes.core.exportar import exportar_atualizacao_lotacao

# Create your views here.

#variaveis global
global_municipios = ['Acrelândia', 'Assis Brasil', 'Brasiléia','Bujari', 'Capixaba', 'Cruzeiro do Sul', 'Epitaciolândia', 'Feijó', 'Jordão', 'Manoel Urbano', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Plácido de Castro', 'Porto Acre', 'Porto Walter', 'Rio Branco', 'Rodrigues Alves', 'Santa Rosa do Purus', 'Sena Madureira', 'Senador Guiomard', 'Tarauacá', 'Xapuri']

global_zoneamentos = ['Centro', 'Baixada', 'Universitário', 'São Francisco/ Tancredo Neves', 'Belo Jardim / Cidade do Povo']

global_regioes = ['Alto Acre', 'Baixo Acre', 'Juruá',  'Purus', 'Tarauacá / Envira']


def verificar_manutencao():
    if Detalhes.objects.get(id=1).situacao == 'Ativo':
        return False
    else:
        return True


def index(request):
    # if not 'https://' in request.build_absolute_uri():
    #     return redirect("https://atena.see.ac.gov.br")

    if verificar_manutencao():
        template_name = 'atena/pagina-manutencao.html'
        user = request.session['username']

        permissao_atena =  Permissao.objects.filter(usuario__login= user, servico__id= 7).exists()

        return TemplateResponse(request, template_name, locals())

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'index.html'
    user = request.session['username']

    if Usuarios.objects.get(login= request.session['username']).status == 'Inativo':
        return HttpResponseRedirect('/logout')

    permissoes = Permissao.objects.filter(usuario__login= user, consultar= 1).values_list('servico__aplicacao__id', flat= True).distinct()

    return TemplateResponse(request, template_name, locals())


def manutencao(request):
    user = request.session['username']
    template_name = 'index_manutencao.html'

    permissao_atena =  Permissao.objects.filter(usuario__login= user, servico__id= 7).exists()

    return TemplateResponse(request, template_name, locals())


def perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'core/servidor/meu-perfil.html'
    id_servidor = Usuarios.objects.get(login = user).servidor

    permissao = None


    if id_servidor == None or id_servidor =='' or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    dicionario = {'nome': None, 'cpf': None, 'item': None, 'antiga': None, 'nova': None}
    servidor = Servidor.objects.get(id= id_servidor)

    if Atualizacao_cadastral.objects.filter(servidor= servidor).exists():
        try:
            historico_base = Atualizacao_cadastral.objects.filter(servidor= servidor).last()
            print(historico_base)
            historico_realizado = Logs.objects.filter(id=historico_base.log)
            historico_login = historico_realizado[0].usuario.login
        except:
            pass

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
        try:
            contrato = Contrato_lotacao.objects.get(id = ultimo_contrato.id)
            if Confirmacao_lotacao.objects.filter(terceirizado_id = ultimo_contrato.id).exists():
                confirmacao_lotacao = Confirmacao_lotacao.objects.get(terceirizado_id = ultimo_contrato.id)
                data_verificacao = confirmacao_lotacao.data_atualizacao
                existe = True
            else:
                if contrato.unidade_administrativa is not None:
                    lotacao_atual = contrato.unidade_administrativa.nome
                else:
                    lotacao_atual = contrato.endereco.escola.nome_escola
        except:
            pass

        if Confirmacao_lotacao.objects.filter(terceirizado_id = ultimo_contrato.id).exists():
            confirmacao_lotacao = Confirmacao_lotacao.objects.get(terceirizado_id = ultimo_contrato.id)
            data_verificacao = confirmacao_lotacao.data_atualizacao
            existe = True
        else:
            if contrato.unidade_administrativa is not None:
                lotacao_atual = contrato.unidade_administrativa.nome
            else:
                lotacao_atual = contrato.endereco.escola.nome_escola

    else:
        servidor_contrato_terceirizado = False


    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

    if Servidor_contato.objects.filter(servidor= servidor).exists():
        servidor_contato = Servidor_contato.objects.filter(servidor= servidor)

    if Servidor_banco.objects.filter(servidor= servidor).exists():
        servidor_banco = Servidor_banco.objects.get(servidor= servidor)

    if Servidor_contrato.objects.filter(servidor= servidor).exists():
        servidor_contrato = Servidor_contrato.objects.filter(servidor= servidor)

    if Servidor_lotacao.objects.filter(contrato__servidor= servidor).exists():
        servidor_lotacoes = Servidor_lotacao.objects.filter(contrato__servidor= servidor, status= 1)
        lotacoes = servidor_lotacoes.values('id', 'contrato__digito', 'unidade_escolar', 'unidade_escolar__escola__nome_escola', 'unidade_adm__nome', 'funcao', 'data_inicio', 'data_termino', 'status', 'motivo')

        verificacoes = []
        id_verificacoes = []
        for lotacao in lotacoes:
            autorizacao = Autorizacao_lotacao.objects.filter(lotacao= lotacao['id'])

            if(autorizacao):
                lotacao['autorizador'] = autorizacao[0].autorizador

            if Confirmacao_lotacao.objects.filter(lotacao= lotacao['id']).exists():
                verificacoes.append(Confirmacao_lotacao.objects.get(lotacao= lotacao['id']))

                #gambiarra marota
                id_verificacoes.append(lotacao['id'])

    if Servidor_documento.objects.filter(servidor= servidor).exists():
        qtd_documentos = Servidor_documento.objects.filter(servidor = servidor).count()
        qr_documentos = Servidor_documento.objects.filter(servidor = servidor)[:3]

        documentos = []

        for documento in qr_documentos:
            formato_documento = str(documento.documento).split('.')[1]
            caminho = str(documento.path_arquivo())
            dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
            documentos.append(dict_documento)

    if Servidor_escolaridade.objects.filter(servidor= servidor).exists():
        escolaridades = Servidor_escolaridade.objects.filter(servidor= servidor)

    if Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id).exists():
        chamados = Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id)[:3]
        qtd_chamados = Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id).count()


    unidades_adm = Unidade_administrativa.objects.filter().values('id', 'nome').exclude(nome= None).order_by('nome')
    unidades_educacionais = Escola.objects.filter().values('id', 'nome_escola').exclude(nome_escola= None).exclude(id__in=[669,723,724,722,741,738,740]).order_by('nome_escola')


    if request.method == 'POST':
        try:
            valor = request.POST.get('btn-exportar-termo-lotacao')
            if 'exportar-termo' in valor:
                id_lotacao = valor.split('-')[-1]
                return exportar_atualizacao_lotacao(request, id_lotacao, servidor_contrato_terceirizado)
        except:
            verificar_lotacao(request)
            return HttpResponseRedirect(f'meu-perfil')

    return TemplateResponse(request, template_name, locals())

def editar_dados(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'core/servidor/editar-dados.html'
    user = request.session['username']
    lotacao = False

    id_servidor = Usuarios.objects.get(login = user).servidor

    if id_servidor != None:
        edicao= True
        servidor = Servidor.objects.get(id= id_servidor)
        servidor.data_nascimento = str(servidor.data_nascimento)

    generos = ("Masculino", "Feminino", "Não binário", "Outro")
    nacionalidades = ("Brasileiro(a)", "Estrangeiro(a)")

    if request.method == 'POST':
        formulario_servidor_base(request, edicao, servidor, lotacao)
        return HttpResponseRedirect(f'meu-perfil')

    return TemplateResponse(request, template_name, locals())


def servidor_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'core/servidor/servidor-endereco.html'
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
        return HttpResponseRedirect(f'meu-perfil')

    return TemplateResponse(request, template_name, locals())


def servidor_contatos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'core/servidor/servidor-contatos.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)

    contatos = Servidor_contato.objects.filter(servidor= servidor)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        edicao = False
        editar_contatos(request, edicao)
        return HttpResponseRedirect(f'meu-perfil')


    return TemplateResponse(request, template_name, locals())


def servidor_banco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'core/servidor/servidor-banco.html'
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

    instituicoes = ("Banco do Brasil", "Bradesco", "Caixa Econômica Federal", "Santander")
    tipos = ("Conta corrente", "Conta salário" , "Conta poupança")

    if request.method == 'POST':
        formulario_servidor_banco(request, edicao, servidor)
        return HttpResponseRedirect(f'meu-perfil')


    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    try:
        if request.session['atualizar-senha']:
            return HttpResponseRedirect('/dados-cadastrais')
    except:
        pass

    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    template_name = 'core/servidor/documento-formulario.html'
    user = request.session['username']

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)
    categorias = ['Comprovante de Residência','CNH', 'CPF', 'Passaporte', 'RG', 'Outros']
    qtd_documento = Servidor_documento.objects.filter(servidor= servidor).count()

    if request.method == 'POST':
        formulario_documento(request, servidor)
        if qtd_documento < 3:
            return HttpResponseRedirect(f'meu-perfil')
        else:
            return HttpResponseRedirect(f'servidor-galeria?id={id_servidor}')

    return TemplateResponse(request, template_name, locals())


def dados_cadastrais(request):
    if not verification(request):
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'core/dados-cadastrais/alterar-senha.html'
    usuario = Usuarios.objects.get(login = user)

    if request.method == 'POST':
        alterar_senha(request, usuario)
        return HttpResponseRedirect("/")

    return TemplateResponse(request, template_name, locals())


def cadastro_escolaridade(request):
    user = request.session['username']
    template_name = 'core/dados-cadastrais/escolaridade.html'
    usuario = Usuarios.objects.get(login = user)
    id_servidor = Usuarios.objects.get(login = user).servidor

    if id_servidor == None or id_servidor =='' or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    servidor = Servidor.objects.get(id= id_servidor)

    formacoes = ["Ensino Médio", "Ensino Médio - Magistério", "Tecnólogo", "Bacharelado", "Licenciatura" ,"Doutorado", "Mestrado", "Pós-Graduação"]

    escolas = Escolas.objects.all().values_list('nome', flat= True)
    universidades = Instituicoes.objects.all()
    cursos = Cursos_graduacao.objects.all().values_list('nome', flat= True)
    cursos_magisterio = Cursos_graduacao.objects.filter(id__in=[2, 55, 306]).values_list('nome', flat= True)

    if request.method == 'POST':
        formulario_escolaridade(request, servidor)
        return HttpResponseRedirect("meu-perfil")

    return TemplateResponse(request, template_name, locals())

def saiba_mais(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'core/saiba-mais/index.html'
    user = request.session['username']

    return TemplateResponse(request, template_name, locals())


def historico_chamados(request):
    user = request.session['username']
    template_name = 'core/servidor/historico-chamados.html'

    id_servidor = Usuarios.objects.get(login = user).servidor

    if id_servidor == None or id_servidor =='' or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    servidor = Servidor.objects.get(id= id_servidor)
    servico = Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id).values('servico').order_by('servico').distinct()
    situacao = Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id).values('solicitacao__situacao').order_by('solicitacao__situacao').distinct()

    chamados = filtro_chamados(request, servidor)
    quantidade_chamados = chamados.count()

    page = request.GET.get('page')
    if page is None:
        page = 1

    paginator = Paginator(chamados, 15)
    chamados = paginator.get_page(page)

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

def suporte(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'core/suporte/index.html'
    user = request.session['username']

    celular = '3213-2389'
    email = 'suporteatena@see.ac.gov.br'

    return TemplateResponse(request, template_name, locals())

def servidor_galeria(request):
    template_name = 'core/servidor/galeria-imagens.html'

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
