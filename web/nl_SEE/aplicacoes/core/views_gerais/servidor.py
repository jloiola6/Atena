from datetime import datetime
from aplicacoes.atena.models import Cidade
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.lotacao.filtros import *
from aplicacoes.lotacao.models import *
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from aplicacoes.usuario.models import Permissao
from aplicacoes.lotacao.exportar import *
from aplicacoes.terceirizacao.models import Contrato_lotacao


def descobrir_aplicacao(request, template):
    url = request.get_full_path()
    if 'lotacao' in url:
        lista = [8]
        nome_aplicacao = url.split('/')[1]
        template = template.replace('aplicacao', nome_aplicacao)
        vinculo = 78
    elif 'terceirizacao' in url:
        lista = [9]
        nome_aplicacao = url.split('/')[1]
        template = template.replace('aplicacao', nome_aplicacao)
        vinculo = None
    return lista, template, vinculo


def servidores(request):
    template_name = 'aplicacao/servidor/servidores.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = permissoes[0])

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
    template_name = 'aplicacao/servidor/servidor-formulario.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']

    hoje = datetime.now()

    cpf = request.GET.get('cpf')


    cidades_acre = Cidade.objects.filter(estado__id = 1).order_by('estado__nome')

    if request.method == 'POST':
        servidor = formulario_servidor(request)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_perfil(request):
    template_name = 'aplicacao/servidor/servidor-perfil.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes):
        return HttpResponseRedirect('/')

    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login = user, servico__id = permissoes[0])

    if Permissao.objects.filter(usuario__login = user, servico__id = 14, editar = 1).exists():
        permissao_contrato = True

    id_servidor = request.GET.get('id')
    if id_servidor == None or id_servidor =='' or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    servidor = Servidor.objects.get(id= id_servidor)
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

    if Servidor_contrato.objects.filter(servidor= servidor).exists():
        servidor_contrato = Servidor_contrato.objects.filter(servidor= servidor)

    if Servidor_lotacao.objects.filter(contrato__servidor= servidor).exists():
        servidor_lotacoes = Servidor_lotacao.objects.filter(contrato__servidor= servidor)


    return TemplateResponse(request, template_name, locals())


def servidor_contatos(request):
    template_name = 'aplicacao/servidor/servidor-contatos.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

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
    template_name = 'aplicacao/servidor/servidor-banco.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

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
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')


    return TemplateResponse(request, template_name, locals())


def servidor_endereco(request):
    template_name = 'aplicacao/servidor/servidor-endereco.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

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
    template_name = 'aplicacao/servidor/servidor-base.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    lotacao= False

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
    template_name = 'aplicacao/servidor/servidor-consulta.html'
    permissoes, template_name, vinculo = descobrir_aplicacao(request, template_name)

    if verificar_manutencao() or not verificacao_maxima(request, permissoes, True):
        return HttpResponseRedirect('/')

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


def cadastro_escolaridade(request):
    user = request.session['username']
    template_name = 'core/dados-cadastrais/escolaridade.html'
    usuario = Usuarios.objects.get(login = user)

    formacoes = ["Ensino Médio","Bacharelado","Doutorado","Mestrado","Pós-Graduação","Tecnologo"]

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)

    escolas = Escolas.objects.all().values_list('nome', flat= True)
    universidades = Instituicoes.objects.all()
    cursos = Cursos_graduacao.objects.all().values_list('nome', flat= True)
    cursos_magisterio = Cursos_graduacao.objects.filter(id__in=[2, 5, 306]).values_list('nome', flat= True)

    if request.method == 'POST':
        formulario_escolaridade(request, servidor)
        return HttpResponseRedirect("/")

    return TemplateResponse(request, template_name, locals())
