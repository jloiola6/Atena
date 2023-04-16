from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
import re

from aplicacoes.terceirizacao.exportar import *
from aplicacoes.administracao.models import *
from aplicacoes.atena.models import *
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.models import *
from aplicacoes.core.geral_actions.servidor import *
from aplicacoes.terceirizacao.filtros import *
from aplicacoes.terceirizacao.models import *
from aplicacoes.usuario.views import verificacao_maxima

from aplicacoes.administracao.exportar import exportar_pdf_servidor_lotado


def servidores(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidores.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 9)

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
            gets_ultima = gets.replace(f'page={page}', gets_ultima)

    return TemplateResponse(request, template_name, locals())


def servidor_consulta(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-consulta.html'
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


def servidor_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-formulario.html'
    user = request.session['username']

    cidades = Cidade.objects.filter(estado__id = 1)
    cpf = request.GET.get('cpf')

    if request.method == 'POST':
        servidor = formulario_servidor(request)
        return HttpResponseRedirect(f'/terceirizacao/servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_perfil(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9, 17]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-perfil.html'
    user = request.session['username']
    if Permissao.objects.filter(usuario__login= user, servico= 9).exists():
        permissao = Permissao.objects.get(usuario__login= user, servico= 9)
    else:
        lotacao = True

    id_servidor = request.GET.get('id')
    if id_servidor == None or not Servidor.objects.filter(id= id_servidor).exists():
        return HttpResponseRedirect('/')

    servidor = Servidor.objects.get(id= id_servidor)
    historico_base = Atualizacao_cadastral.objects.filter(servidor= servidor.id).last()

    if Contrato_lotacao.objects.filter(servidor= servidor).exists():
        servidor_contrato = True
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
        servidor_contrato = False

    if Servidor_contrato.objects.filter(servidor= servidor).exists():
        servidor_contrato_see = Servidor_contrato.objects.filter(servidor= servidor)

    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

    if Servidor_contato.objects.filter(servidor= servidor).exists():
        servidor_contato = Servidor_contato.objects.filter(servidor= servidor)

    if Servidor_banco.objects.filter(servidor= servidor).exists():
        servidor_banco = Servidor_banco.objects.get(servidor= servidor)

    if Servidor_escolaridade.objects.filter(servidor= servidor).exists():
        escolaridades = Servidor_escolaridade.objects.filter(servidor= servidor)

    return TemplateResponse(request, template_name, locals())


def servidor_contatos(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-contatos.html'
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


def servidores_lotados(request):
    if verificar_manutencao() or not verificacao_maxima(request, [17]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidores-lotados.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico= 17)

    # if request.GET.get('pdf'):
    #     render_to_pdf('administracao/unidades-administrativas/servidores-lotados.html')

    id_unidade = request.GET.get('id')
    unidade = Unidade_administrativa.objects.get(id= id_unidade)

    servidores = filtro_servidores_unidade(request)
    quantidade_servidores = len(servidores)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_servidor_lotado(request)
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_servidor_lotado(request, id_unidade)

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    paginator = Paginator(servidores, 15)
    servidores = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    pagina_primeira = 'page=1'
    proxima_pagina = f'page={str(int(page)+1)}'
    pagina_anterior = f'page={str(int(page)-1)}'
    pagina_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        if 'page' not in gets:
            gets = f'page={page}&' + gets

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', pagina_ultima)

    return TemplateResponse(request, template_name, locals())


def servidor_contrato_perfil(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9, 17]):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-contrato-perfil.html'
    user = request.session['username']
    if Permissao.objects.filter(usuario__login= user, servico= 9).exists():
        permissao = Permissao.objects.get(usuario__login= user, servico= 9)
    else:
        lotacao = True

    id_contrato = request.GET.get('id_contrato')
    if id_contrato != None:
        contrato_lotacao = Contrato_lotacao.objects.get(id = id_contrato)
        finalizar_contrato = contrato_lotacao.status
        servidor = contrato_lotacao.servidor
        item = contrato_lotacao.item

        if Servidor_ocorrencia_funcional.objects.filter(contrato__id = id_contrato).exists():
            ocorrencias  = Servidor_ocorrencia_funcional.objects.filter(contrato__id = id_contrato)
            ultima_ocorrencia = ocorrencias.last()

        contrato = item.contrato
        empresa = contrato.empresa

        if Contrato_aditivo.objects.filter(contrato= contrato).exists():
            ultimo_contrato = Contrato_aditivo.objects.filter(contrato= contrato).last()

        if Fonte_contrato.objects.filter(contrato= contrato).exists():
            fontes = Fonte_contrato.objects.filter(contrato= contrato)

        lotacoes = contrato_lotacao = Contrato_lotacao.objects.filter(item__contrato= contrato, servidor= servidor)
        ultima_lotacao = lotacoes.last()
    else:
        return HttpResponseRedirect('/')

    return TemplateResponse(request, template_name, locals())


def servidor_banco(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-banco.html'
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
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-endereco.html'
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
        return HttpResponseRedirect(f'/terceirizacao/servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_base(request):
    if verificar_manutencao() or not verificacao_maxima(request, [9], True):
        return HttpResponseRedirect('/')

    template_name = 'terceirizacao/servidor/servidor-base.html'
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
        return HttpResponseRedirect(f'/terceirizacao/servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def escolaridade(request):
    user = request.session['username']
    template_name = 'terceirizacao/servidor/escolaridade.html'
    usuario = Usuarios.objects.get(login = user)

    id_servidor = request.GET.get('id')
    servidor = Servidor.objects.get(id= id_servidor)

    formacoes = ["Ensino Médio", "Ensino Médio - Magistério", "Tecnólogo", "Bacharelado", "Licenciatura" ,"Doutorado", "Mestrado", "Pós-Graduação"]

    escolas = Escolas.objects.all().values_list('nome', flat= True)
    universidades = Instituicoes.objects.all()
    cursos = Cursos_graduacao.objects.all().values_list('nome', flat= True)

    if request.method == 'POST':
        formulario_escolaridade(request, servidor)
        return HttpResponseRedirect(f'servidor-perfil?id={servidor.id}')

    return TemplateResponse(request, template_name, locals())