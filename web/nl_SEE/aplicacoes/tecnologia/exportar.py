from itertools import chain
from distutils.log import fatal
import imp
from django.http import HttpResponse
from django.template.loader import get_template
import xlwt
from xhtml2pdf import pisa
from datetime import datetime

from .filtros import *
from .models import *
from django.conf import settings
from aplicacoes.core.actions import salvar_historico

def export_xlsx(model, filename, lista, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    for linha in range(len(lista)):
        for col in range(len(lista[linha])):
            val = lista[linha][col]
            ws.write(linha+1, col, val, default_style)

    wb.save(response)
    return response


def exportar_excel_vagas(request):
    vagas = filtro_vagas(request)
    names = ['contrato', 'item', 'lote', 'descricao', 'quantidade', 'disponiveis', 'vagas', 'valor_unitario']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'contrato':
            colunas.append('N° Contrato')
        elif request.POST.get(name) == 'on' and name == 'item':
            colunas.append('Item')
        elif request.POST.get(name) == 'on' and name == 'lote':
            colunas.append('Lote')
        elif request.POST.get(name) == 'on' and name == 'descricao':
            colunas.append('Descricao')
        elif request.POST.get(name) == 'on' and name == 'quantidade':
            colunas.append('Quantidade total')
        elif request.POST.get(name) == 'on' and name == 'disponiveis':
            colunas.append('Disponiveis')
        elif request.POST.get(name) == 'on' and name == 'valor_unitario':
            colunas.append('Valor unitario')

    model = 'vagas tecnologia'
    filename = 'vagas tecnologia.xls'
    lista = []
    queryset = list(vagas)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Contrato':
                valor.append(i.contrato.numero_contrato)
            elif j == 'Item':
                valor.append(i.numero_item)
            elif j == 'Lote':
                valor.append(i.numero_lote)
            elif j == 'Descricao':
                valor.append(i.descricao.upper())
            elif j == 'Quantidade total':
                valor.append(i.quantidade)
            elif j == 'Disponiveis':
                valor.append(i.qtd_vagas)
            elif j == 'Valor unitario':
                valor.append(i.valor_unitario)

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_excel_contratos_tec(request):
    contrato = filtro_contratos(request)
    names = ['contrato', 'empresa', 'data_vigente', 'valor_total', 'situacao']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'contrato':
            colunas.append('N° Contrato')
        elif request.POST.get(name) == 'on' and name == 'empresa':
            colunas.append('Empresa')
        elif request.POST.get(name) == 'on' and name == 'data_vigente':
            colunas.append('Data Vigente')
        elif request.POST.get(name) == 'on' and name == 'valor_total':
            colunas.append('Valor Total')
        elif request.POST.get(name) == 'on' and name == 'situacao':
            colunas.append('Situação')


    model = 'Contratos de Tecnologia'
    filename = 'Contratos de Tecnologia.xls'
    lista = []
    queryset = list(contrato)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Contrato':
                valor.append(i.numero_contrato)
            elif j == 'Empresa':
                valor.append(i.empresa.nome)
            elif j == 'Data Vigente':
                valor.append(i.data_inicio)
            elif j == 'Valor Total':
                valor.append(i.valor_total)
            elif j == 'Situação':
                valor.append(i.situacao)

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_excel_links(request, name_bandas, name_operadoras, name_status, name_fornecedor, name_tipo, name_velocidade):
    links = filtro_links(request, name_bandas, name_operadoras, name_status, name_fornecedor, name_tipo, name_velocidade)
    names = ['circuito', 'unidade', 'tipo', 'fornecedor', 'operadora', 'tipo_banda', 'velocidade', 'status']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'circuito':
            colunas.append('N° Circuito')
        elif request.POST.get(name) == 'on' and name == 'unidade':
            colunas.append('Unidade / Departamento')
        elif request.POST.get(name) == 'on' and name == 'tipo':
            colunas.append('Tipo')
        elif request.POST.get(name) == 'on' and name == 'fornecedor':
            colunas.append('Fornecedor')
        elif request.POST.get(name) == 'on' and name == 'operadora':
            colunas.append('Operadora')
        elif request.POST.get(name) == 'on' and name == 'tipo_banda':
            colunas.append('Tipo de Banda')
        elif request.POST.get(name) == 'on' and name == 'velocidade':
            colunas.append('MB/s')
        elif request.POST.get(name) == 'on' and name == 'status':
            colunas.append('Situação')


    model = 'Links de Tecnologia'
    filename = 'Links de Tecnologia.xls'
    lista = []
    queryset = list(links)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Circuito':
                valor.append(i['circuito'])
            elif j == 'Unidade / Departamento':
                if i['tipo'] == 'Unidade Educacional':
                    valor.append(i['unidade_educacional__escola__nome_escola'])
                else:
                    valor.append(i['departamento__nome'])
            elif j == 'Tipo':
                valor.append(i['tipo'])
            elif j == 'Fornecedor':
                valor.append(i['fornecedor'])
            elif j == 'Operadora':
                valor.append(i['operadora'])
            elif j == 'Tipo de Banda':
                valor.append(i['tipo_banda'])
            elif j == 'MB/s':
                valor.append(i['velocidade'])
            elif j == 'Situação':
                valor.append(i['status'])

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_pdf_contratos_tec(request):
    exportar = filtro_contratos(request)
    template_path = 'tecnologia/contrato/partials/_contrato-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-infraestrutura-redes.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'exportar': exportar, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Contratos de Tecnologia.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_links(request, links, nome, data):
    template_path = 'tecnologia/links/partials/_links-pdf.html'

    link_ips = Firewall.objects.all().values('link__item__contrato__numero_contrato', 'link__unidade_educacional__escola__cod_inep', 'link__unidade_educacional__escola__nome_escola', 'link__departamento__sigla', 'link__departamento__nome', 'link__tipo', 'link__fornecedor', 'link__operadora', 'link__tipo_banda', 'link__circuito', 'link__velocidade', 'link__status', 'link__item', 'link__item__numero_item', 'link__item__valor_unitario', 'link__fonte', 'ip_firewall').order_by('-id')
    ids_link_ips = Firewall.objects.values_list('id', flat= True)

    links = Link.objects.exclude(id__in= ids_link_ips).values('id', 'item__contrato__numero_contrato', 'unidade_educacional__escola__cod_inep', 'unidade_educacional__escola__nome_escola', 'departamento__sigla', 'departamento__nome', 'tipo', 'fornecedor', 'operadora', 'tipo_banda', 'circuito', 'velocidade', 'status', 'item', 'item__numero_item', 'item__valor_unitario', 'fonte').order_by('-id')
    links = list(chain(link_ips, links))
    total = Link.objects.all().count()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-infraestrutura-redes.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'exportar': links, 'nome': nome, 'data': data, 'total': total, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Links de Tecnologia.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_tablets(request, user):
    template_path = 'tecnologia/educacao-conectada/tablets/partials/_tablets-pdf.html'

    exportar = filtro_tablets(request)
    quantidade = exportar.count()
    nome = Usuarios.objects.get(login= user)
    data = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/detei.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'exportar': exportar, 'quantidade': quantidade, 'nome': nome, 'data': data, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Educação Conectada - Tablets.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_tablets_aluno(request, user, dados):
    template_path = 'tecnologia/educacao-conectada/tablets/partials/_tablets-aluno-pdf.html'

    nome = Usuarios.objects.get(login= user)
    data = datetime.today()
    brs = list(range(17))

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/detei.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'dados': dados, 'nome': nome, 'data': data, 'brs': brs, 'url_logo': url_logo, 'url_atena': url_atena }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Educação Conectada - Tablets.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_devolucao_notebook(request, user, dados, auxilio):
    template_path = 'tecnologia/auxilio-notebook/partials/_devolucao-pdf.html'

    descricao =  request.POST.get('descricao_notebook')
    motivo = request.POST.get('motivo_devolucao')
    caixa_notebook = request.POST.get('caixa_notebook')
    nota_notebook = request.POST.get('nota_notebook')
    notebook = request.POST.get('notebook')
    carregador = request.POST.get('carregador')

    nome = Usuarios.objects.get(login= user)
    data = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/detei.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'dados': dados, 'nome': nome, 'data': data, 'auxilio': auxilio, 'url_logo': url_logo, 'url_atena': url_atena, 'descricao': descricao, 'motivo': motivo, 'caixa_notebook': caixa_notebook, 'nota_notebook': nota_notebook, 'notebook': notebook, 'carregador': carregador }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Devolução Notebook - Auxilio.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')

    devolucao = Auxilio_notebook()
    devolucao.auxilio= int(auxilio['id'])
    devolucao.gestor=Servidor.objects.get(cpf = nome.cpf)
    devolucao.data_exportacao= data
    devolucao.descricao_notebook = descricao
    devolucao.motivo_devolucao = motivo
    devolucao.caixa_notebook = caixa_notebook
    devolucao.nota_notebook = nota_notebook
    devolucao.notebook = notebook
    devolucao.carregador = carregador
    devolucao.save()
    salvar_historico(request, devolucao, False, 'tecnologia_auxilio_notebook')

    return response


def exportar_chamados(request, solicitacao, equipamentos, chamados, equipamento_recolhido):
    template_path = 'tecnologia/chamados/partials/_chamados-pdf.html'

    user_solicitante = Servidor.objects.get(id= solicitacao.user_solicitante)

    if Solicitacao_tecnico.objects.filter(solicitacao = solicitacao).exists():
        tecnico = Solicitacao_tecnico.objects.filter(solicitacao = solicitacao).last()
    else:
        tecnico = None

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/detei.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'solicitacao':solicitacao, 'equipamentos': equipamentos, 'chamados': chamados, 'tecnico': tecnico, 'equipamento_recolhido': equipamento_recolhido, 'user_solicitante': user_solicitante, 'url_logo': url_logo, 'url_atena': url_atena }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Relatório de Atendimento.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response
