from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from unidecode import unidecode

from aplicacoes.tecnologia.models import *
from aplicacoes.administracao.models import Contato
from aplicacoes.lotacao.models import Servidor_lotacao
from aplicacoes.tecnologia.actions.links import *
from aplicacoes.coex.models import *

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao

from aplicacoes.core.views import global_municipios, global_zoneamentos, global_regioes
from aplicacoes.tecnologia.filtros import *
from aplicacoes.tecnologia.exportar import exportar_pdf_links, exportar_excel_links

from aplicacoes.core.models import *
from datetime import date

def links_tabela(request):
    if not verificacao_maxima(request, [12]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/links/links_tabela.html'
    user = request.session['username']
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()

    name_tipo = []
    tipos = []
    for tipo in Link.objects.all().values('tipo').distinct().order_by('tipo'):
        name = (tipo['tipo'])
        tipos.append((f'id-{name}', name, tipo['tipo']))
        name_tipo.append(name)

    name_fornecedor = []
    fornecedores = []
    for fornecedor in Link.objects.all().values('fornecedor').distinct().order_by('fornecedor'):
        name = (fornecedor['fornecedor'])
        fornecedores.append((f'id-{name}', name, fornecedor['fornecedor']))
        name_fornecedor.append(name)

    name_bandas = []
    bandas = []
    for banda in Link.objects.all().values('tipo_banda').distinct().order_by('tipo_banda'):
        name = (banda['tipo_banda'])
        bandas.append((f'id-{name}', name, banda['tipo_banda']))
        name_bandas.append(name)

    name_operadoras = []
    operadoras = []
    for operadora in Link.objects.all().exclude(operadora= None).values('operadora').distinct().order_by('operadora'):
        name = (operadora['operadora'])
        operadoras.append((f'id-{name}', name, operadora['operadora']))
        name_operadoras.append(name)

    name_status = []
    status = []
    for situacao in Link.objects.all().values('status').distinct().order_by('status'):
        name = (situacao['status'])
        status.append((f'id-{name}', name, situacao['status']))
        name_status.append(name)

    name_fontes = []
    fontes = []
    for fonte in Link.objects.all().exclude(fonte= None).values('fonte').distinct().order_by('fonte'):
        name = (fonte['fonte'])
        fontes.append((f'id-{name}', name, fonte['fonte']))
        name_fontes.append(name)

    lista_velocidades = ['2 MB/s', '4 MB/s', '6 MB/s', '10 MB/s', '20 MB/s', '30 MB/s', '50 MB/s', '100 MB/s', '200 MB/s', '300 MB/s', '500 MB/s', '1000 MB/s']
    name_velocidade = []
    velocidades = []
    for velocidade in lista_velocidades:
        if Link.objects.filter(velocidade= velocidade).exists():
            name = (velocidade)
            velocidades.append((f'id-{name}', name, velocidade))
            name_velocidade.append(name)

    links = filtro_links(request, name_bandas, name_operadoras, name_status, name_fornecedor, name_tipo, name_velocidade, name_fontes)
    exportar_links = links

    total = 0
    for item in links:
        if item['fornecedor'] == "SEE":
            valor = item['item__valor_unitario'].replace('R$', '').strip()
            valor = valor.split(',')
            valor = float(valor[0].replace('.', '') + '.' + valor[1])
            total += valor

    total = "{0:,}".format(total).replace(',', '.')
    valor_total = ''
    total = str(total).split('.')
    for i in range(len(total)):
        if i  == len(total) - 1:
            valor_total = valor_total[:-1] + f',{total[i][:2]}'
        else:
            valor_total += f'{total[i]}.'

    id_endereco = []
    id_unidade_adm = []
    id_item = []
    for i in Link.objects.filter(status= 'ATIVO').values('unidade_educacional__id', 'departamento__id', 'item__id', 'status'):
        if i['unidade_educacional__id'] != None:
            id_endereco.append(i['unidade_educacional__id'])
        else:
            id_unidade_adm.append(i['departamento__id'])
        id_item.append(i['item__id'])

    enderecos = Endereco.objects.filter(id__in= id_endereco).values('id', 'escola__cod_inep', 'escola__nome_escola' ).order_by('escola__nome_escola')
    departamentos = Unidade_administrativa.objects.filter(id__in= id_unidade_adm).values('id', 'sigla', 'nome').order_by('nome')
    itens = Contrato_item.objects.filter(id__in = id_item).values('id', 'contrato__numero_contrato', 'numero_item', 'descricao')

    municipios = []
    for i in Link.objects.all().values('departamento__endereco__municipio', 'unidade_educacional__municipio').distinct():
        if i['departamento__endereco__municipio'] != None:
            municipios.append(i['departamento__endereco__municipio'])
        else:
            municipios.append(i['unidade_educacional__municipio'])

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'excel':
            return exportar_excel_links(request, name_bandas, name_operadoras, name_status, name_fornecedor, name_tipo, name_velocidade)

    if request.method == 'POST':
        if request.POST.get('exportar-fieldset-formatos') == 'pdf':
            return exportar_pdf_links(request, links, nome, data)

    page = request.GET.get('page')
    if page is None:
        page = '1'

    quantidade_links = links.count()
    paginator = Paginator(links, 15)
    links = paginator.get_page(page)

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

        if not 'page' in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')


        filtros_tipo = []
        filtros_fornecedor = []
        filtros_banda = []
        filtros_operadora = []
        filtros_status = []
        filtros_velocidade = []
        filtros_fonte = []

        for item in gets.split('&'):
            item = item.split('=')
            valor = item[0].replace('+', ' ').replace('+', ' ').replace('%2F', '/')

            if valor in name_tipo:
                filtros_tipo.append(valor)
            elif valor in name_fornecedor:
                filtros_fornecedor.append(valor)
            elif valor in name_bandas:
                filtros_banda.append(valor)
            elif valor in name_operadoras:
                filtros_operadora.append(valor)
            elif valor in name_status:
                filtros_status.append(valor)
            elif valor in name_velocidade:
                filtros_velocidade.append(valor)
            elif valor in name_fontes:
                filtros_fonte.append(valor)

    return TemplateResponse(request, template_name, locals())


def link_formulario(request):
    if not verificacao_maxima(request, [12], True) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/links/link_formulario.html'
    user = request.session['username']
    edicao = False

    id_contratos = []
    for id in Vinculacao_contrato.objects.filter(unidade_administrativa= 11).values('contrato'):
        id_contratos.append(id['contrato'])
    itens = Contrato_item.objects.filter(contrato__id__in= id_contratos, contrato__tipo_contrato= 'Serviços', vagas='1', descricao__icontains= 'Link').values('id', 'contrato__numero_contrato', 'numero_item', 'descricao')

    enderecos = Endereco.objects.all().values('id', 'escola__cod_inep', 'escola__nome_escola' ).order_by('escola__nome_escola')
    departamentos = Unidade_administrativa.objects.all().values('id', 'sigla', 'nome').order_by('nome')
    operadoras = ['Claro', 'Global Age', 'Oi', 'Sem Fronteiras', 'Vivo']
    tipo_bandas = ['ADSL', 'ADSL Empresarial', 'Circuito de Dados', 'Circuito de Dados - Satélite', 'GESAC', 'Oi Fibra - GPON']
    velocidades = ['2 MB/s', '4 MB/s', '6 MB/s', '10 MB/s', '20 MB/s', '30 MB/s', '50 MB/s', '100 MB/s', '200 MB/s', '300 MB/s', '500 MB/s', '1000 MB/s']

    link = request.GET.get('id')
    firewalls = Firewall.objects.filter(link= link)


    if link != None:
        link = Link.objects.get(id= int(link))

        if link.status == 'INATIVO':
            return HttpResponseRedirect(f'link_perfil?id={link.id}')

        edicao = True
        if request.method == 'POST':
            editar_link(request, edicao)
            return HttpResponseRedirect(f'link_perfil?id={link.id}')
    else:
        edicao = False
        if request.method == 'POST':
            formulario_link(request)
            return HttpResponseRedirect(f'links_tabela')

    return TemplateResponse(request, template_name, locals())


def link_perfil(request):
    if not verificacao_maxima(request, [12]) or verificar_manutencao():
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'tecnologia/links/link-perfil.html'

    link_id = request.GET.get('id')

    link = Link.objects.get(id= link_id)
    firewalls = Firewall.objects.filter(link= link)

    if link.unidade_educacional != None:
        escola = link.unidade_educacional.escola
        try:
            escola = Escola.objects.get(cod_inep= escola.cod_inep)
        except:
            return HttpResponseRedirect('/tecnologia')

        id_endereco = link.unidade_educacional.id
        try:
            if id_endereco:
                endereco = Endereco.objects.get(escola= escola, id= id_endereco)
            else:
                endereco = Endereco.objects.get(escola= escola)
        except:
            return HttpResponseRedirect('/tecnologia')

        if Coex.objects.filter(escola= escola, status=1).exists():
            coex = Coex.objects.get(escola= escola, status=1)

            if Consorcio.objects.filter(cnpj= coex.cnpj, status=1).exists():
                consorcio = Consorcio.objects.get(cnpj= coex.cnpj, status=1)

        contatos = Contato.objects.filter(endereco = endereco)
        escola_etapas = Etapa_escola.objects.filter(escola= escola)

        diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
            diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).exists():
            pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
            ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
            administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
            secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    else:
        departamento = link.departamento
        if Unidade_administrativa.objects.filter(id= departamento.id).exists():
            contem_endereco = True
            endereco = Unidade_administrativa.objects.get(id= departamento.id)

    if link.fornecedor == 'SEE':
        contrato = link.item.contrato
        empresa = contrato.empresa
        if request.method == 'POST':
            adicionar_google(request, escola)
            return HttpResponseRedirect(f'/tecnologia/link_perfil?id={link_id}')

    c = 1
    mudancas = []
    links_mudancas = []
    for i in Historico.objects.filter(objeto= link_id, tabela= 'tecnologia_link', acao= 'E').values('modificacao', 'data', 'log_id'):
        modificacoes = i['modificacao']
        if '(datetime.date(' in modificacoes:
            modificacoes = i['modificacao'].split('(datetime.date(')
            modificacoes = modificacoes[0] + '(None' +modificacoes[1][11:]
            modificacoes = modificacoes.replace('(None)', '(None')
        modificacoes = (modificacoes.replace('{', '').replace('}', '').replace("':", '').replace('_id', '').replace('"', '').replace("'", "").replace('(', '')).split("), ")

        usuario = Logs.objects.get(id= i['log_id']).usuario.nome
        valor = []
        for x in modificacoes:
            nome = x.split()[0]
            x = x.replace(f'{nome} ', '').replace(')', '').replace('None', 'vazio').replace('(', '')
            nome = nome.replace('_', ' ').title()
            x = x.split(', ')
            if nome == 'Data Alteracao':
                frase_novo = x[1]
            else:
                frase_antigo = x[0]
                frase_novo = x[1]

                if 'Departamento:' in frase_antigo:
                    id_departamento_antigo = x.split()[1]
                    id_departamento_novo = x.split()[3]

                    if id_departamento_antigo != 'vazio':
                        departamento_antigo = Unidade_administrativa.objects.get(id= id_departamento_antigo).nome
                        frase_antigo = frase_antigo.replace(id_departamento_antigo, departamento_antigo)
                        frase_novo = frase_novo.replace(id_departamento_antigo, departamento_antigo)

                    if id_departamento_novo != 'vazio':
                        departamento_novo = Unidade_administrativa.objects.get(id= id_departamento_novo).nome
                        frase_antigo = frase_antigo.replace(id_departamento_novo, departamento_novo)
                        frase_novo = frase_novo.replace(id_departamento_novo, departamento_novo)

                elif 'Unidade Educacional:' in frase_antigo:
                    id_endereco_antigo = x.split()[1]
                    id_endereco_novo = x.split()[3]

                    if id_endereco_antigo != 'vazio':
                        endereco_antigo = Endereco.objects.get(id= id_endereco_antigo).escola.nome_escola
                        frase_antigo = frase_antigo.replace(id_endereco_antigo, endereco_antigo)
                        frase_novo = frase_novo.replace(id_endereco_antigo, endereco_antigo)

                    if id_endereco_novo != 'vazio':
                        endereco_novo = Endereco.objects.get(id= id_endereco_antigo).escola.nome_escola
                        frase_antigo = frase_antigo.replace(id_endereco_novo, endereco_novo)
                        frase_novo = frase_novo.replace(id_endereco_novo, endereco_novo)
            if nome == 'Data Alteracao':
                data = (frase_novo.replace(' ', '')).split('-')
                data_alteracao = f"{data[2]}/{data[1]}/{data[0]}"
            else:
                valor.append((frase_antigo, frase_novo, nome))
        mudancas.append((c, valor))
        links_mudancas.append((c, valor, i['data'].replace(' ', ' as '), usuario, data_alteracao))
        c += 1

    return TemplateResponse(request, template_name, locals())


def link_perfil_antigo(request):
    if not verificacao_maxima(request, [12]) or verificar_manutencao():
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'tecnologia/links/link-perfil.html'

    link_id = request.GET.get('id')

    link = Link.objects.get(id= link_id)
    firewalls = Firewall.objects.filter(link= link)

    departamento = link.departamento
    if link.fornecedor == 'SEE':
        contrato = link.item.contrato
        empresa = contrato.empresa

    if link.unidade_educacional != None:
        endereco = link.unidade_educacional
        escola = endereco.escola
        if Coex.objects.filter(escola= escola, status=1).exists():
            coex = Coex.objects.get(escola= escola, status=1)
        contatos = Contato.objects.filter(endereco = endereco)
        escola_etapas = Etapa_escola.objects.filter(escola= escola)

        diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
            diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).exists():
            pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
            ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
            administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
        if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
            secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

        if request.method == 'POST':
            adicionar_google(request, escola)
            return HttpResponseRedirect(f'/tecnologia/link_perfil?id={link_id}')

    elif Unidade_administrativa.objects.filter(id= departamento.id).exists():
        contem_endereco = True
        endereco = Unidade_administrativa.objects.get(id= departamento.id)

    c = 1
    mudancas = []
    links_mudancas = []
    for i in Historico.objects.filter(objeto= link_id, tabela= 'tecnologia_link', acao= 'E').values('modificacao', 'data', 'log_id'):
        modificacoes = i['modificacao']
        if '(datetime.date(' in modificacoes:
            modificacoes = i['modificacao'].split('(datetime.date(')
            modificacoes = modificacoes[0] + '(None' +modificacoes[1][11:]
            modificacoes = modificacoes.replace('(None)', '(None')
        modificacoes = (modificacoes.replace('{', '').replace('}', '').replace("':", '').replace('_id', '').replace('"', '').replace("'", "").replace('(', '')).split("), ")

        usuario = Logs.objects.get(id= i['log_id']).usuario.nome
        valor = []
        for x in modificacoes:
            nome = x.split()[0]
            x = x.replace(f'{nome} ', '').replace(')', '').replace('None', 'vazio').replace('(', '')
            nome = nome.replace('_', ' ').title()
            x = x.split(', ')
            if nome == 'Data Alteracao':
                frase_novo = x[1]
            else:
                frase_antigo = x[0]
                frase_novo = x[1]

                if 'Departamento:' in frase_antigo:
                    id_departamento_antigo = x.split()[1]
                    id_departamento_novo = x.split()[3]

                    if id_departamento_antigo != 'vazio':
                        departamento_antigo = Unidade_administrativa.objects.get(id= id_departamento_antigo).nome
                        frase_antigo = frase_antigo.replace(id_departamento_antigo, departamento_antigo)
                        frase_novo = frase_novo.replace(id_departamento_antigo, departamento_antigo)

                    if id_departamento_novo != 'vazio':
                        departamento_novo = Unidade_administrativa.objects.get(id= id_departamento_novo).nome
                        frase_antigo = frase_antigo.replace(id_departamento_novo, departamento_novo)
                        frase_novo = frase_novo.replace(id_departamento_novo, departamento_novo)

                elif 'Unidade Educacional:' in frase_antigo:
                    id_endereco_antigo = x.split()[1]
                    id_endereco_novo = x.split()[3]

                    if id_endereco_antigo != 'vazio':
                        endereco_antigo = Endereco.objects.get(id= id_endereco_antigo).escola.nome_escola
                        frase_antigo = frase_antigo.replace(id_endereco_antigo, endereco_antigo)
                        frase_novo = frase_novo.replace(id_endereco_antigo, endereco_antigo)

                    if id_endereco_novo != 'vazio':
                        endereco_novo = Endereco.objects.get(id= id_endereco_antigo).escola.nome_escola
                        frase_antigo = frase_antigo.replace(id_endereco_novo, endereco_novo)
                        frase_novo = frase_novo.replace(id_endereco_novo, endereco_novo)
            if nome == 'Data Alteracao':
                data = (frase_novo.replace(' ', '')).split('-')
                data_alteracao = f"{data[2]}/{data[1]}/{data[0]}"
            else:
                valor.append((frase_antigo, frase_novo, nome))
        mudancas.append((c, valor))
        links_mudancas.append((c, valor, i['data'].replace(' ', ' as '), usuario, data_alteracao))
        c += 1

    return TemplateResponse(request, template_name, locals())


def inativar_link(request):
    if not verificacao_maxima(request, [12], True) or verificar_manutencao():
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'tecnologia/links/inativar-link.html'

    link_id = request.GET.get('id')
    link = Link.objects.get(id= link_id)

    contrato = link.item.contrato

    if link.tipo == 'Unidade Educacional':
        unidade_educacional = link.unidade_educacional.escola
    else:
        departamento = link.departamento

    if request.method == 'POST':
        link_inativar(request, link_id, user)
        return HttpResponseRedirect(f'/tecnologia/link_perfil?id={link_id}')

    return TemplateResponse(request, template_name, locals())