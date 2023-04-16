from .models import *

from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.lotacao.models import Servidor
from aplicacoes.terceirizacao.models import *

import re


def formulario_usuario(request, edicao):
    #Dados Usuário
    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    cpf = re.sub('\D', '', cpf)
    email = request.POST.get('email')
    login = request.POST.get('login')
    # senha = request.POST.get('senha')
    status = request.POST.get('fieldset-usuario-situacao')

    #Consultando o banco
    if edicao:
        usuario = Usuarios.objects.filter(id= int(request.GET.get('id_usuario')))
        # inputs = {'id': int(request.GET.get('id_usuario')), 'nome': nome, 'login': login, 'cpf': cpf, 'senha': senha, 'email': email, 'status': 1 }
        inputs = {'id': int(request.GET.get('id_usuario')), 'nome': nome, 'login': login, 'cpf': cpf, 'email': email, 'status': status }
        modificacoes = dict_compare(usuario.values()[0], inputs)

        usuario = usuario[0]

    else:
        modificacoes = None
        usuario = Usuarios()

    #Salvando no banco dados da unidade
    usuario.nome = nome
    usuario.login = login
    usuario.cpf = cpf
    usuario.email = email
    usuario.status = status

    #codificando senha
    # if len(senha) != 0:
    #     senha = hashlib.md5(senha.encode())
    #     senha = senha.hexdigest()
    #     usuario.senha = senha
    # else:
    #     del modificacoes['senha']

    usuario.save()

    salvar_historico(request, usuario, edicao, 'usuario_usuarios', modificacoes)


def permissoes_usuario(request, edicao, pendente= None):
    #Capturando dados
    servico = request.POST.get('servico')
    consultar = request.POST.get('fieldset-consultar')
    editar = request.POST.get('fieldset-editar')
    imprimir = request.POST.get('fieldset-imprimir')
    servico = Servico.objects.get(id= servico)

    if pendente:
        permissao =  Permissao()
        usuario = request.POST.get('email')
        permissao.usuario_pendente = usuario
        modificacoes_permissao = None
    else:
        if edicao:
            id_permissao = request.GET.get('id_permissao')
            permissao = Permissao.objects.filter(id= id_permissao)
            inputs_permissao = {'servico': servico.id, 'consultar': consultar, 'editar': editar, 'imprimir': imprimir }
            modificacoes_permissao = dict_compare(permissao.values()[0], inputs_permissao)

            permissao = permissao[0]
            if permissao.servico.id in [4, 5]:
                Gestor_Escolar.objects.get(permissao= permissao).delete()
        else:
            permissao =  Permissao()
            usuario = Usuarios.objects.get(id= request.GET.get('id_usuario'))
            permissao.usuario = usuario
            modificacoes_permissao = None


    permissao.servico = servico
    permissao.consultar = consultar
    permissao.editar = editar
    permissao.imprimir = imprimir
    permissao.save()

    if servico.id in [4, 5]:
        inep = request.POST.get('inep')
        gestor =  Gestor_Escolar()
        gestor.inep = inep
        gestor.permissao = permissao
        gestor.save()

    salvar_historico(request, permissao, edicao, 'usuario_permissao', modificacoes_permissao)


def cadastrar_usuario(data, user, password):
    if not Usuarios.objects.filter(login= data['username'], senha= password).exists():
        usuario = Usuarios()
        usuario.nome = data['nome']
        usuario.login = data['username']
        usuario.cpf = data['cpf']
        usuario.senha = password
        usuario.email = data['email']
        usuario.status = 'Ativo'

        usuario.save()
    else:
        usuario = Usuarios.objects.get(login= data['username'], senha= password)

    verificar_servidor(usuario)


def atualizar_senha(user, password):
    usuario = Usuarios.objects.get(login= user)
    usuario.senha = password
    usuario.save()


def excluir_permissao(request, permissao, edicao, excluir):
    if Gestor_Escolar.objects.filter(permissao= permissao).exists():
        gestor = Gestor_Escolar.objects.get(permissao= permissao)
        modificacoes_gestor = {'inep': gestor.inep, 'permissao_id': gestor.permissao.id}
        salvar_historico(request, gestor, edicao, 'usuario_gestor_escolar', modificacoes_gestor, excluir)
        gestor.delete()

    modificacoes_permissao = {'servico_id': permissao.servico.id, 'consultar': permissao.consultar, 'editar': permissao.editar, 'imprimir': permissao.imprimir, 'usuario_id': permissao.usuario.id, 'usuario_pendente': permissao.usuario_pendente}
    salvar_historico(request, permissao, edicao, 'usuario_permissao', modificacoes_permissao, excluir)
    permissao.delete()


def verificar_servidor(usuario):
    if Servidor.objects.filter(cpf= usuario.cpf).exists():
        usuario.servidor = Servidor.objects.filter(cpf= usuario.cpf).last().id
        usuario.save()


def consultar_terceirizado(user, password_api, password):
    if Servidor.objects.filter(cpf= password_api).exists():
        servidor = Servidor.objects.get(cpf= password_api)
        if Contrato_lotacao.objects.filter(servidor= servidor, status= 1).exists():
            usuario = Usuarios()
            usuario.nome = servidor.nome
            usuario.login = user
            usuario.cpf = servidor.cpf
            usuario.senha = password
            usuario.email = ''
            usuario.status = 'Ativo'
            usuario.servidor = servidor.id
            usuario.save()

            return True

    return False


def todas_permissoes(request, usuario):
    i = 1
    while i != 39:
        servico= Servico.objects.get(id=i)
        permissoes= Permissao()
        if i != 4 and i != 5:
            if not Permissao.objects.filter(servico= servico, usuario= usuario).last():
                permissoes.servico = servico
                permissoes.consultar = 1
                permissoes.editar = 1
                permissoes.imprimir = 1
                permissoes.usuario = usuario
                permissoes.save()
        i += 1

def remover_permissoes(request, usuario):
    permissoes = Permissao.objects.filter(usuario=usuario)
    if permissoes.exists():
        permissoes.exclude(servico_id=6).delete()