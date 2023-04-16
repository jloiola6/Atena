from importlib.metadata import requires
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

import hashlib
from datetime import datetime
from pytz import timezone

from aplicacoes.lotacao.models import Servidor_lotacao, Servidor_contrato
from aplicacoes.terceirizacao.models import Contrato_lotacao

from .models import *
from .action import *
from .API import *
from .filtros import *

from aplicacoes.administracao.models import Escola
from aplicacoes.atena.models import Detalhes


#Erro ao chamar função do core então vou criar a verificação aqui
site_manutencao = False
def verificar_manutencao():
    global site_manutencao
    return site_manutencao
# -----------------------------------------

# Create your views here.
def pegar_ip(request):
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        if len(proxies) > 0:
            return proxies[0]
        else:
            return ip

    return ip


def verification(request):
    try:
        if request.session['username']:
            return True
    except KeyError:
        return False

def verificar_permissao(request, servicos):
    for servico in servicos:
        if Permissao.objects.filter(usuario__login= request.session['username'], servico= servico).exists():
            return True

    return False


def verificacao_maxima(request, servicos, formulario= None, servico_extra= None):
    retorno = False

    try:
        if request.session['atualizar-senha']:
            return retorno
    except:
        request.session['atualizar-senha'] = False

    try:
        if request.session['username']:
            pass
    except KeyError:
        return retorno

    if Usuarios.objects.get(login= request.session['username']).status == 'Inativo':
        return False

    if servico_extra and Permissao.objects.filter(usuario__login= request.session['username'], servico= servico_extra).exists():
        if Permissao.objects.get(usuario__login= request.session['username'], servico= servico_extra).editar == 1:
            return True

    for permissao in Permissao.objects.filter(usuario__login= request.session['username'], servico__in= servicos):
        if formulario:
            if permissao.editar == 1:
                retorno = True
        else:
            retorno = True
    return retorno

def logout(request): #Editado!
    try:
        login = request.session['username']
        del request.session['username']
        del request.session['atualizar-senha']

        data = datetime.now().astimezone(timezone('America/Rio_Branco'))
        data = data.strftime("%d/%m/%Y %H:%M:%S")
        log = request.session['log']
        del request.session['log']

        if Logs.objects.filter(id = log).exists():
            log = Logs.objects.filter(id= log).last()
            log.saida = data
            log.save()
    except KeyError:
        pass

    return HttpResponseRedirect('/usuario/login')

def adicionar_permissao_gestor(usuario):
    # # permissoes = Permissao.objects.filter(usuario_pendente__contains= user)
    gestores = ['Diretor(a)', 'Cordenador(a) Pedagogico', 'Coordenador(a) de Ensino', 'Coordenador(a) Administrativo', 'Secretario(a) Escolar']
    if Servidor_lotacao.objects.filter(contrato__servidor__id= usuario.servidor, funcao__in= gestores, unidade_escolar__isnull= False).exists():
        inep = Servidor_lotacao.objects.filter(contrato__servidor__id= usuario.servidor, funcao__in= gestores, unidade_escolar__isnull= False).last().unidade_escolar.escola.cod_inep
        servico = Servico.objects.get(id= 5)

        if not Permissao.objects.filter(usuario= usuario, servico= servico).exists():
            permissao =  Permissao()
            permissao.usuario = usuario
            permissao.servico = servico
            permissao.consultar = 1
            permissao.editar = 1
            permissao.imprimir = 1
            permissao.save()

            gestor =  Gestor_Escolar()
            gestor.inep = inep
            gestor.permissao = permissao
            gestor.save()

            for permissao in Permissao.objects.filter(usuario_pendente__contains= usuario.login):
                usuario_pendente = (permissao.usuario_pendente).split('@')[0]

                permissao.usuario = usuario
                permissao.usuario_pendente = None
                permissao.servico = permissao.servico
                permissao.consultar = permissao.consultar
                permissao.editar = permissao.editar
                permissao.imprimir = permissao.imprimir
                permissao.save()

def adicionar_permissao(usuario):

    # permissoes = Permissao.objects.filter(usuario_pendente__contains= user)
    for permissao in Permissao.objects.filter(usuario_pendente__contains= usuario.login):
        usuario_pendente = (permissao.usuario_pendente).split('@')[0]

        permissao.usuario = usuario
        permissao.usuario_pendente = None
        permissao.servico = permissao.servico
        permissao.consultar = permissao.consultar
        permissao.editar = permissao.editar
        permissao.imprimir = permissao.imprimir
        permissao.save()

def login(request): #Editado!
    # if not 'https://' in request.build_absolute_uri():
    #     return redirect("https://atena.see.ac.gov.br/usuario/login")

    if verification(request):
        return HttpResponseRedirect('/')

    template_name = 'usuario/login.html'
    if request.method == 'POST':
        user = request.POST.get('user').strip()
        password_api = password = request.POST.get('password')

        user = (user.split('@'))[0]

        password = hashlib.md5(password.encode())
        password = password.hexdigest()

        usuario_valido = Usuarios.objects.filter(login= user).exists()
        ip = pegar_ip(request)
        data = datetime.now().astimezone(timezone('America/Rio_Branco'))
        data = data.strftime("%d/%m/%Y %H:%M:%S")

        if usuario_valido:
            if Usuarios.objects.filter(login= user, senha= password, status= 'Inativo').exists():
                return HttpResponseRedirect('/usuario/login')

            senha_valida = Usuarios.objects.filter(login= user, senha= password, status= 'Ativo').exists()
            if senha_valida:
                usuario = Usuarios.objects.get(login= user, senha= password)
                verificar_servidor(usuario)
                adicionar_permissao_gestor(usuario)
                login = usuario.login
                request.session['username'] = login

                cpf = hashlib.md5(usuario.cpf.encode())
                cpf = cpf.hexdigest()
                if password == cpf:
                    request.session['atualizar-senha'] = True
                else:
                    request.session['atualizar-senha'] = False

                log = Logs(usuario= usuario, entrada= data, ip= ip)
                
                log.save()
                request.session['log'] = str(log.id)

                return HttpResponseRedirect('/')
            else:
                dados = autenticarAPI(user, password_api)
                if dados['status']:
                    atualizar_senha(user, password)

                    usuario = Usuarios.objects.get(login= user, senha= password)
                    verificar_servidor(usuario)
                    adicionar_permissao_gestor(usuario)
                    login = usuario.login
                    request.session['username'] = login
                    request.session['atualizar-senha'] = False

                    cpf = hashlib.md5(usuario.cpf.encode())
                    cpf = cpf.hexdigest()
                    if password == cpf:
                        request.session['atualizar-senha'] = True
                    else:
                        request.session['atualizar-senha'] = False

                    log = Logs(usuario= usuario, entrada= data, ip= ip)
                    log.save()
                    request.session['log'] = str(log.id)

                    return HttpResponseRedirect('/')

                erro = 'Senha inválida'
        else:
            dados = autenticarAPI(user, password_api)
            if dados['status']:
                cadastrar_usuario(dados, user, password)

                usuario = Usuarios.objects.get(login= user, senha= password)
                adicionar_permissao(usuario)
                verificar_servidor(usuario)
                adicionar_permissao_gestor(usuario)
                login = usuario.login
                request.session['username'] = login
                request.session['atualizar-senha'] = False

                log = Logs(usuario= usuario, entrada= data, ip= ip)
                log.save()
                request.session['log'] = str(log.id)

                return HttpResponseRedirect('/')
            elif consultar_terceirizado(user, password_api, password):
                usuario = Usuarios.objects.get(login= user, senha= password)
                adicionar_permissao(usuario)
                verificar_servidor(usuario)
                request.session['username'] = user

                cpf = hashlib.md5(usuario.cpf.encode())
                cpf = cpf.hexdigest()
                if password == cpf:
                    request.session['atualizar-senha'] = True
                else:
                    request.session['atualizar-senha'] = False

                log = Logs(usuario= usuario, entrada= data, ip= ip)
                log.save()
                request.session['log'] = str(log.id)

                return HttpResponseRedirect('/dados-cadastrais')

            erro = 'Usuário não encontrado'

    return TemplateResponse(request, template_name, locals())

def new_login(request):
    if verification(request):
        return HttpResponseRedirect('/')

    #Pagina
    template_name = 'usuario/login.html'

    #Manipulando dados do Inputs
    if request.method == 'POST':

        #Variaveis de  Login e senha
        user = request.POST.get('user').strip()
        password_api = password = request.POST.get('password')
        user = (user.split('@'))[0]
        password = hashlib.md5(password.encode())
        password = password.hexdigest()

        #Dados para salvar no log
        ip = pegar_ip(request)
        data = datetime.now().astimezone(timezone('America/Rio_Branco'))
        data = data.strftime("%d/%m/%Y %H:%M:%S")


        #Tratamento de get, caso o usuário exista na tabela "usuario_usuarios"
        try:
            usuario = Usuarios.objects.get(login=user, senha= password, status='Ativo')

            #Manipulando usuário já existente na base
            verificar_servidor(usuario)
            adicionar_permissao_gestor(usuario)

            request.session['username'] = usuario.login

            cpf = hashlib.md5(usuario.cpf.encode())
            cpf = cpf.hexdigest()

            if password == cpf:
                request.session['atualizar-senha'] = True
            else:
                request.session['atualizar-senha'] = False

            log = Logs(usuario= usuario, entrada= data, ip= ip)
            log.save()

            request.session['log'] = str(log.id)

            return HttpResponseRedirect('/')
            
            erro = 'Senha inválida'
        
        #Tratamento de get, caso o usuário não exista na tabela "usuario_usuarios"
        except ObjectDoesNotExist:
            dados = autenticarAPI(user, password_api)

            if dados['status']:
                cadastrar_usuario(dados, user, password)

                usuario = Usuarios.objects.get(cpf=dados['cpf'])
                adicionar_permissao(usuario)
                verificar_servidor(usuario)
                adicionar_permissao_gestor(usuario)
                login = usuario.login
                request.session['username'] = login
                request.session['atualizar-senha'] = False

                log = Logs(usuario= usuario, entrada= data, ip= ip)
                log.save()
                request.session['log'] = str(log.id)

                return HttpResponseRedirect('/')
            
            elif consultar_terceirizado(user, password_api, password):
                usuario = Usuarios.objects.get(login= user, senha= password)
                adicionar_permissao(usuario)
                verificar_servidor(usuario)
                request.session['username'] = user

                cpf = hashlib.md5(usuario.cpf.encode())
                cpf = cpf.hexdigest()
                if password == cpf:
                    request.session['atualizar-senha'] = True
                else:
                    request.session['atualizar-senha'] = False

                log = Logs(usuario= usuario, entrada= data, ip= ip)
                log.save()
                request.session['log'] = str(log.id)

                return HttpResponseRedirect('/dados-cadastrais')
                

    return TemplateResponse(request, template_name, locals())

def index(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/index.html'
    user = request.session['username']

    try:
        meu_usuario = Usuarios.objects.get(login= user)
    except:
        meu_usuario = None

    usuarios = Usuarios.objects.filter(status='Ativo').values('id', 'nome', 'login', 'cpf', 'email').order_by('nome')

    usuarios = filtro_usuarios(request, usuarios)
    if request.GET.get('fieldset-filtro-usuario') == 'Pendente':
        pendente = True

    page = request.GET.get('page')
    if page is None:
        page = '1'

    quantidade_usuarios = len(usuarios)
    paginator = Paginator(usuarios, 15)
    usuarios = paginator.get_page(page)

    return TemplateResponse(request, template_name, locals())

def pre_cadastrados(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/pre-cadastrados.html'
    user = request.session['username']
    # usuarios = Usuarios.objects.filter(status='Ativo').values('id', 'nome', 'login', 'cpf', 'email').order_by('-id')

    usuarios = Permissao.objects.filter(usuario__isnull= True).order_by('-id')

    page = request.GET.get('page')
    if page is None:
        page = '1'

    quantidade_usuarios = len(usuarios)
    paginator = Paginator(usuarios, 15)
    usuarios = paginator.get_page(page)

    return TemplateResponse(request, template_name, locals())

def usuario_formulario(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/usuario_formulario.html'
    user = request.session['username']
    edicao = False

    usuario = request.GET.get('id_usuario')
    if usuario != None:
        try:
            usuario = Usuarios.objects.get(id= int(usuario))
            edicao = True
        except:
            edicao = False

    if request.method == 'POST':
        formulario_usuario(request, edicao)
        return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={usuario.id}')

    return TemplateResponse(request, template_name, locals())

def usuario_perfil(request): #Editado!
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/usuario_perfil.html'
    user = request.session['username']

    usuario = request.GET.get('id_usuario')
    if usuario != None:
        usuario = Usuarios.objects.get(id= int(usuario))

    permissoes = Permissao.objects.filter(usuario= usuario).order_by('servico__aplicacao__id')
    aplicacoes = []
    for permissao in permissoes:
        if permissao.servico.aplicacao not in aplicacoes:
            aplicacoes.append(permissao.servico.aplicacao)


    if request.method == 'POST':
        if request.POST.get('btn-adicionar-tudo') == 'adicionar-tudo':
            todas_permissoes(request, usuario)
        else:
            remover_permissoes(request, usuario)
        return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={usuario.id}')

    return TemplateResponse(request, template_name, locals())

def usuario_permissoes(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/usuario_permissoes.html'
    user = request.session['username']

    id_usuario = request.GET.get('id_usuario')

    if id_usuario != None:
        pendente = False
        usuario = Usuarios.objects.get(id= int(id_usuario))

        servicos_existentes = []
        for permissao in Permissao.objects.filter(usuario= usuario):
            servicos_existentes.append(permissao.servico.id)
            #Tirar permissoes de gestao e adm do DINEM
            if permissao.servico.id == 3:
                    servicos_existentes.append(4)
            elif permissao.servico.id == 4:
                servicos_existentes.append(3)
            #Tirar permissoes de gestao e adm do Administrador
            if permissao.servico.id == 1:
                    servicos_existentes.append(5)
            elif permissao.servico.id == 5:
                servicos_existentes.append(1)

        #Tirar permissoes do ATENA
        servicos_existentes.append(7)

        servicos = Servico.objects.exclude(id__in= servicos_existentes).order_by('aplicacao')
        if servicos.count() > 0:
            aplicacoes = []
            for servico in servicos:
                if not servico.aplicacao in aplicacoes:
                    aplicacoes.append(servico.aplicacao)
        else:
            nova_permissao = True
    else:
        servicos = Servico.objects.all().order_by('aplicacao')
        aplicacoes = Aplicacao.objects.all()

        #Tirar permissoes do ATENA
        servicos = servicos.exclude(id= 7)
        aplicacoes = aplicacoes.exclude(id= 4)

        pendente = True

    # CARREGANDO AS UNIDADES PARA O PREENCHER O FOMULÁRIO DE GRADE
    unidades = Escola.objects.all()

    edicao = False
    if request.method == 'POST':
        #REFATORAR ISSO PELO AMOR DE DEUS!!!!
        if request.POST.get('inep') in ['4', '5']:
            if Escola.objects.filter(cod_inep= request.POST.get('inep')).exists():
                if pendente:
                    email = request.POST.get('email')
                    if not Usuarios.objects.filter(email= email, status= 'Ativo').exists():
                        permissoes_usuario(request, edicao, pendente)
                else:
                    permissoes_usuario(request, edicao, pendente)
                    return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={id_usuario}')
        else:
            if pendente:
                email = request.POST.get('email')
                if not Usuarios.objects.filter(email= email, status= 'Ativo').exists():
                    permissoes_usuario(request, edicao, pendente)
            else:
                permissoes_usuario(request, edicao, pendente)
                return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={id_usuario}')


    return TemplateResponse(request, template_name, locals())

def editar_permissao(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    template_name = 'usuario/editar_permissao.html'
    user = request.session['username']
    edicao = True

    id_permissao = request.GET.get('id_permissao')
    usuario_permissao = Permissao.objects.get(id= id_permissao)
    if usuario_permissao.servico.id in [4, 5]:
        gestor = Gestor_Escolar.objects.get(permissao= usuario_permissao)

    # CARREGANDO AS UNIDADES PARA O PREENCHER O FOMULÁRIO DE GRADE
    unidades = Escola.objects.all()

    if request.method == 'POST':
        excluir = request.POST.get('excluir')
        if excluir == None:
            permissoes_usuario(request, edicao)
        else:
            excluir_permissao(request, usuario_permissao, edicao, True)

        return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={usuario_permissao.usuario.id}')

    return TemplateResponse(request, template_name, locals())

def exluir_permissao(request):

    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [6]):
        return HttpResponseRedirect('/')

    excluir = edicao = True
    id_permissao = request.GET.get('id_permissao')
    permissao = Permissao.objects.get(id= id_permissao)

    excluir_permissao(request, permissao, edicao, excluir)

    return HttpResponseRedirect(f'/usuario/usuario_perfil?id_usuario={permissao.usuario.id}')
