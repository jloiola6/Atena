from datetime import datetime
from aplicacoes.administracao.models import *

from aplicacoes.core.actions import dict_compare, salvar_historico
from aplicacoes.tecnologia.models import Link, Firewall

import re


def formulario_link(request):
    edicao = False 

    item_id = request.POST.get('item')
    item = Contrato_item.objects.get(id = item_id)
    contrato = Contrato_contrato.objects.get(id = item.contrato.id)

    fornecedor = request.POST.get('fornecedor')
    circuito = request.POST.get('circuito')
    tipo = request.POST.get('tipo')
    unidade_educacional = request.POST.get('unidade')
    departamento = request.POST.get('departamento')
    operadora = request.POST.get('operadora')
    tipo_banda = request.POST.get('tipo_banda')
    velocidade = request.POST.get('velocidade')
    status = request.POST.get('status')
    data_ativo = request.POST.get('data_ativo')
    ip_lan = request.POST.get('iplan')
    ip_wan = request.POST.get('ipwan')
    observacao = request.POST.get('observacao')

    if tipo == 'Unidade Educacional':
        fonte = request.POST.get('fonte_edu')
    else:
        fonte = request.POST.get('fonte_adm')

    posts = request.POST
    c = 1
    firewalls = []
    for i in posts:
        if c > 16:
            firewalls.append(i)
        c += 1
    firewalls.pop()

    fonte_rp = f'{fonte} (RP)'
    if not Fonte_contrato.objects.filter(fonte_recurso = fonte_rp, contrato= item.contrato.id).exists():
        fonte_contrato = Fonte_contrato()
        fonte_contrato.contrato = contrato
        fonte_contrato.fonte_recurso = fonte_rp
        fonte_contrato.save()
        salvar_historico(request, fonte_contrato, edicao, 'administracao_fonte_contrato')

    if not Link.objects.filter(circuito = circuito, data_inativo__isnull= True).exists() and not Link.objects.filter(iplan = ip_lan, data_inativo__isnull= True).exists() and not Link.objects.filter(ipwan = ip_wan, data_inativo__isnull= True).exists():
        link = Link()
        link.tipo = tipo

        if fornecedor == 'SEE':
            link.item = item

        if tipo == 'Unidade Educacional':
            link.unidade_educacional = Endereco.objects.get(id = unidade_educacional)
        else:
            link.departamento = Unidade_administrativa.objects.get(id = departamento)
        
        link.fonte = fonte
        link.fornecedor = fornecedor
        link.circuito = circuito
        link.operadora = operadora
        link.tipo_banda = tipo_banda
        link.velocidade = velocidade
        link.status = status
        link.data_ativo = data_ativo
        link.iplan = ip_lan
        link.ipwan = ip_wan
        link.observacao = observacao
        link.save()
        salvar_historico(request, link, edicao, 'tecnologia_link')

        for name in firewalls:
            firewall = Firewall()
            firewall.link = link
            firewall.ip_firewall = request.POST.get(name)
            firewall.save()
            salvar_historico(request, firewall, edicao, 'tecnologia_firewall')

        if fornecedor == 'SEE':
            vagas = item.qtd_vagas - 1
            if item.contrato.empresa.cnpj == "09.354.828/0001-12":
                contrato = item.contrato
                for item in Contrato_item.objects.filter(contrato = contrato):
                    item.qtd_vagas = vagas
                    item.save()
            else:
                item.qtd_vagas = vagas

            if vagas == 0:
                item.vagas = 0
            else:
                item.vagas = 1
            item.save()


def editar_link(request, edicao):
    
    tipo = request.POST.get('tipo')
    unidade_educacional = request.POST.get('unidade')
    departamento = request.POST.get('departamento')
    fornecedor = request.POST.get('fornecedor')
    operadora = request.POST.get('operadora')
    tipo_banda = request.POST.get('tipo_banda')
    circuito = request.POST.get('circuito')
    data_alteracao = request.POST.get('data_alteracao')
    ip_lan = request.POST.get('iplan')
    ip_wan = request.POST.get('ipwan')
    velocidade = request.POST.get('velocidade')
    observacao = request.POST.get('observacao')
    if tipo == 'Unidade Educacional':
        fonte = request.POST.get('fonte_edu')
    else:
        fonte = request.POST.get('fonte_adm')

    if tipo == 'Unidade Educacional':
        departamento = None
        unidade_educacional = int(unidade_educacional)
    else:
        unidade_educacional = None
        departamento = int(departamento)
        
    link = Link.objects.filter(id= request.GET.get('id'))

    inputs_link = {'data_alteracao': data_alteracao, 'id': link[0].id, 'tipo': tipo, 'unidade_educacional_id': unidade_educacional, 'departamento_id': departamento, 'fonte': fonte, 'fornecedor': fornecedor, 'operadora': operadora, 'tipo_banda': tipo_banda, 
    'circuito': circuito, 'iplan': ip_lan, 'ipwan': ip_wan, 'velocidade': velocidade, 'observacao': observacao}
    modificacoes_links = dict_compare(link.values()[0], inputs_link)
    link = link[0]
    
    contador = 0
    for x in modificacoes_links:
        contador += 1
    if modificacoes_links != {} and contador > 1:
        link.tipo = tipo
        if tipo == 'Unidade Educacional':
            link.departamento = None
            link.unidade_educacional = Endereco.objects.get(id = unidade_educacional)
        else:
            link.unidade_educacional = None
            link.departamento = Unidade_administrativa.objects.get(id = departamento)
        link.fonte = fonte
        link.fornecedor = fornecedor
        link.operadora = operadora
        link.tipo_banda = tipo_banda
        link.data_alteracao = data_alteracao
        link.iplan = ip_lan
        link.ipwan = ip_wan
        link.circuito = circuito
        link.velocidade = velocidade
        link.observacao = observacao
        link.save()
        salvar_historico(request, link, edicao, 'tecnologia_link', modificacoes_links)
    
    posts = request.POST
    c = 1
    firewalls = []
    for i in posts:
        if c > 14:
            firewalls.append(request.POST.get(i))
        c += 1
    firewalls.pop()

    for item in Firewall.objects.filter(link = link):
        if item.ip_firewall not in (firewalls):
            excluir = True
            modificacoes_ip_firewall= {'link': item.link.id, 'ip_firewall': item.ip_firewall}
            salvar_historico(request, item, edicao, 'tecnologia_firewall', modificacoes_ip_firewall, excluir)
            item.delete()
        
    for item in firewalls:
        if not Firewall.objects.filter(link= link, ip_firewall= item).exists():
            modificacoes_ip_firewall = {'link': link.id, 'ip_firewall': item}
            firewall = Firewall()
            firewall.link = link
            firewall.ip_firewall = item
            firewall.save()
            salvar_historico(request, firewall, edicao, 'tecnologia_firewall', modificacoes_ip_firewall)


def adicionar_google(request, escola): #Nova Função
    #Capturando dados
    escola = Endereco.objects.get(escola__cod_inep= escola.cod_inep)
    google_map = request.POST.get('google_map')

    escola.google_map = google_map
    escola.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...
    salvar_historico(request, escola, edicao, 'administracao_endereco')


def link_inativar(request, link_id, user):
    edicao=False

    data_inativo = request.POST.get('data_inativo')
    motivo = request.POST.get('motivo')
 
    link = Link.objects.filter(id = link_id)

    inputs_link = {'id': link[0].id, 'status': 'INATIVO'}
    modificacoes_links = dict_compare(link.values()[0], inputs_link)
    link = link[0]
    item = link.item
 
    link.status = 'INATIVO'
    link.user_inativou = user
    link.data_inativo = data_inativo
    link.motivo = motivo
    link.save()

    vagas = item.qtd_vagas + 1   
    item.qtd_vagas = vagas

    if vagas == 0:
        item.vagas = 0
    else:
        item.vagas = 1

    item.save()

    salvar_historico(request, link, edicao, 'tecnologia_link')