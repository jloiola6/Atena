from .models import *

import re

def filtro_usuarios(request, usuarios):
    nome =  request.GET.get('nome_usuario')
    cpf =  request.GET.get('cpf')
    email =  request.GET.get('email')
    usuario =  request.GET.get('usuario')

    if request.GET.get('fieldset-filtro-usuario') == 'Ativo':
        usuarios = Usuarios.objects.filter(status='Ativo').values('id', 'nome', 'login', 'cpf', 'email').order_by('-id')
    elif request.GET.get('fieldset-filtro-usuario') == 'Pendente':
        usuarios = Permissao.objects.filter(usuario__isnull= True).order_by('-id')
    elif request.GET.get('fieldset-filtro-usuario') == 'Inativo':
        usuarios = Usuarios.objects.filter(status='Inativo').values('id', 'nome', 'login', 'cpf', 'email').order_by('-id')


    if nome != None and nome != '':
        usuarios = usuarios.filter(nome__icontains= nome)

    if cpf != None and cpf != '':
        cpf = re.sub('\D', '', cpf)
        usuarios = usuarios.filter(cpf__contains= cpf)
    
    if email != None and email != '':
        usuarios = usuarios.filter(email__icontains= email)
    
    if usuario != None and usuario != '':
        usuarios = usuarios.filter(login__icontains= usuario)


    return usuarios