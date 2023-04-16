from imp import new_module
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import xlwt
from xhtml2pdf import pisa
# from fpdf import FPDF, HTMLMixin

from .filtros import *
from .models import *
import datetime
from aplicacoes.core.filtros_gerais.contrato import *
from aplicacoes.terceirizacao.filtros import *

from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings


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


def exportar_excel(request):
    lotacoes = filtro_lotacoes(request)
    names = ['contrato', 'item', 'servidor', 'unidade', 'empresa']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'contrato':
            colunas.append('N° Contrato')
        elif request.POST.get(name) == 'on' and name == 'item':
            colunas.append('N° Item')
        elif request.POST.get(name) == 'on' and name == 'servidor':
            colunas.append('Servidor')
        elif request.POST.get(name) == 'on' and name == 'unidade':
            colunas.append('Unidade')
        elif request.POST.get(name) == 'on' and name == 'empresa':
            colunas.append('Empresa')

    model = 'Lotação de Terceirizados'
    filename = 'Lotação de Terceirizados.xls'
    lista = []
    queryset = list(lotacoes)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Contrato':
                valor.append(i.item.contrato.numero_contrato)
            elif j == 'N° Item':
                valor.append(i.item.numero_item)
            elif j == 'Servidor':
                valor.append(i.servidor.nome.upper())
            elif j == 'Unidade':
                if i.endereco != None:
                    valor.append(i.endereco.escola.nome_escola.upper())
                else:
                    valor.append(i.unidade_administrativa.nome.upper())
            elif j == 'Empresa':
                valor.append(i.item.contrato.empresa.nome.upper().upper())

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
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

    model = 'central de vagas'
    filename = 'central de vagas.xls'
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


def exportar_excel_contratos(request, vinculo):
    contrato = filtro_contratos(request, vinculo)
    names = ['contrato', 'empresa', 'tipo_contrato', 'data_vigente', 'valor_total', 'situacao']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'contrato':
            colunas.append('N° Contrato')
        elif request.POST.get(name) == 'on' and name == 'empresa':
            colunas.append('Empresa')
        elif request.POST.get(name) == 'on' and name == 'tipo_contrato':
            colunas.append('Tipo de Contrato')
        elif request.POST.get(name) == 'on' and name == 'data_vigente':
            colunas.append('Data Vigente')
        elif request.POST.get(name) == 'on' and name == 'valor_total':
            colunas.append('Valor Total')
        elif request.POST.get(name) == 'on' and name == 'situacao':
            colunas.append('Situação')

    model = 'contratos terceirizados'
    filename = 'Contratos Terceirizados.xls'
    lista = []
    queryset = list(contrato)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Contrato':
                valor.append(i.numero_contrato)
            elif j == 'Empresa':
                valor.append(i.empresa.nome.upper())
            elif j == 'Tipo de Contrato':
                valor.append(i.tipo_contrato.upper())
            elif j == 'Data Vigente':
                valor.append(i.data_inicio)
            elif j == 'Valor Total':
                valor.append(i.valor_total)
            elif j == 'Situação':
                valor.append(i.situacao.upper())

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)

    return response


def exportar_excel_servidor_lotado(request):
    queryset = filtro_servidores_unidade(request)
    names = ['nome', 'lotacao', 'cargo', 'tipo']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'nome':
            colunas.append('Nome')
        elif request.POST.get(name) == 'on' and name == 'lotacao':
            colunas.append('Lotação')
        elif request.POST.get(name) == 'on' and name == 'cargo':
            colunas.append('Cargo')
        elif request.POST.get(name) == 'on' and name == 'tipo':
            colunas.append('Tipo')
    model = 'Servidores lotados'
    filename = 'Servidores lotados.xls'
    lista = []
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'Nome':
                if i[3] == 'SEE':
                    valor.append(i[0].nome.upper())
                else:
                    valor.append(i[0])
            elif j == 'Lotação':
                valor.append(i[1].nome.upper())
            elif j == 'Cargo':
                valor.append(i[2].upper())
            elif j == 'Tipo':
                valor.append(i[3])
        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)

    return response


def exportar_excel_servidores(request):
    names = ['nome', 'cpf', 'data_nascimento']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'nome':
            colunas.append('Nome')
        elif request.POST.get(name) == 'on' and name == 'cpf':
            colunas.append('CPF')
        elif request.POST.get(name) == 'on' and name == 'data_nascimento':
            colunas.append('Data de Nascimento')

    queryset = filtro_servidores(request)
    model = 'Servidores'
    filename = 'Servidores.xls'
    lista = []
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'Nome':
                valor.append(i.nome.upper())
            elif j == 'CPF':
                valor.append(i.cpf)
            elif j == 'Data de Nascimento':
                valor.append(str(i.data_nascimento))
        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)

    return response


def exportar_pdf_servidores(request):
    exportar = filtro_servidores(request)
    template_path = 'terceirizacao/servidor/partials/_servidor-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/servidores-lotados.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'exportar': exportar, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Servidores Terceirizados.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')

    return response


def exportar_pdf_lotacoes(request, nome, data):
    template_path = 'terceirizacao/lotacao/partials/_lotacao-pdf.html'

    lotacoes = filtro_lotacoes(request)
    quantidade_lotacoes = lotacoes.count()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/servidores-lotados.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    # listaa1 = []
    # for lotacao in lotacoes:
    #     if lotacao.unidade_administrativa:
    #         lista1.append(lotacao.item.contrato.numero_contrato)
    #         contexto = {'contrato': lotacao.item.contrato.numero_contrato, 'item': lotacao.item.numero_item, 'servidor': lotacao.servidor, "unidade": lotacao.unidade_administrativa}

    #     else:
    #         contexto = {'contrato': lotacao.item.contrato.numero_contrato, 'item': lotacao.item.numero_item, 'servidor': lotacao.servidor, "unidade": lotacao.endereco, 'empresa': lotacao.unidade_administrativa}

    contexto = {'lotacoes': lotacoes, 'quantidade_lotacoes': quantidade_lotacoes, 'nome':nome, 'data':data, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Servidores lotados.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response