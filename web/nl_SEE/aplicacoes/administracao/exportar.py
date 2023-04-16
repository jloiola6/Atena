from datetime import date, datetime
from select import select
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import xlwt
# from fpdf import FPDF, HTMLMixin

from .filtros import *
from .models import *
from aplicacoes.core.filtros_gerais.contrato import *
from xhtml2pdf import pisa
from django.shortcuts import render
from aplicacoes.tecnologia.models import Link, Firewall
from aplicacoes.fundiaria.models import Extincao, Arquivo, Energia
from aplicacoes.coex.models import Equipe_comite
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
    # default_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

    for linha in range(len(lista)):
        for col in range(len(lista[linha])):
            val = lista[linha][col]
            if val == 'S':
                val = 'Sede'
            elif val == 'A':
                val = 'Anexo'
            ws.write(linha+1, col, val, default_style)

    wb.save(response)
    return response



# def exportar_excel(request, name_municipios, modalidades, name_regioes, regioes, tipo_localizacao):
def exportar_excel(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes, name_total_alunos):
    enderecos = Endereco.objects.all()
    # enderecos = filtro_unidades(request, enderecos, name_municipios, modalidades, name_regioes, regioes, tipo_localizacao)
    enderecos = filtro_unidades(request, enderecos, name_municipios, name_regioes, regioes, tipo_localizacao, name_etapas, name_etnia, name_localizacao, name_aldeia, name_tipificacoes, name_total_alunos)

    names = ['cod_inep', 'cod_turmalina', 'nome_escola', 'modalidade', 'municipio', 'regiao', 'zoneamento', 'cep', 'rua', 'numero', 'bairro', 'complemento', 'tipo_localizacao', 'latitude', 'longitude', 'tipo', 'total_alunos', 'tipificacao']
    colunas = []
    valores = []
    for name in names:
        if request.POST.get(name):
            name = name.replace('cod_inep', 'Inep').replace('cod_turmalina', 'Turmalina').replace('nome_escola', 'Nome').replace('tipo_localizacao', 'Tipo de Localização').replace('total_alunos', 'Total de Alunos')
            colunas.append(name.title())

    model = 'Unidade Educacionais'
    filename = 'Unidade Educacionais.xls'
    lista = []
    queryset = list(enderecos)
    for item in queryset:
        valor = []
        for j in colunas:
            if j == 'Inep':
                valor.append(item.escola.cod_inep)
            elif j == 'Nome':
                valor.append(item.escola.nome_escola.upper())
            elif j == 'Tipificacao':
                valor.append(item.escola.tipificacao)
            elif j == 'Turmalina':
                valor.append(item.escola.cod_turmalina)
            elif j == 'Total De Alunos':
                valor.append(item.escola.total_alunos)
            elif j == 'Modalidade':
                valor.append(item.escola.modalidade)
            elif j == 'Municipio':
                valor.append(item.municipio.upper())
            elif j == 'Regiao':
                valor.append(item.regiao.upper())
            elif j == 'Zoneamento':
                valor.append(item.zoneamento)
            elif j == 'Cep':
                valor.append(item.cep)
            elif j == 'Rua':
                valor.append(item.rua.upper())
            elif j == 'Numero':
                valor.append(item.numero)
            elif j == 'Bairro':
                valor.append(item.bairro.upper())
            elif j == 'Complemento':
                valor.append(item.complemento.upper())
            elif j == 'Tipo De Localização':
                valor.append(item.tipo_localizacao.upper())
            elif j == 'Latitude':
                valor.append(item.latitude)
            elif j == 'Longitude':
                valor.append(item.longitude)
            elif j == 'Tipo':
                valor.append(item.tipo)
        lista.append(valor)

    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_excel_contratos_adm(request, vinculo, gestor_titular):

    if not gestor_titular:
        ids = Contrato_contrato.objects.values_list('id', flat= True)
        contrato = Contrato_gestor.objects.filter(contrato__in= ids)
    else:
        contrato = filtro_contratos(request, vinculo)

    names = ['contrato', 'empresa', 'tipo_contrato', 'data_vigente', 'valor_total', 'situacao','gestor', 'gestor_substituto', 'fiscal', 'fiscal_substituto']
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
        elif request.POST.get(name) == 'on' and name == 'gestor':
            colunas.append('Gestor Titular')
        elif request.POST.get(name) == 'on' and name == 'gestor_substituto':
            colunas.append('Gestor Substituto')
        elif request.POST.get(name) == 'on' and name == 'fiscal':
            colunas.append('Fiscal Titular')
        elif request.POST.get(name) == 'on' and name == 'fiscal_substituto':
            colunas.append('Fiscal Substituto')

    model = 'contratos administrativos'
    filename = 'Contratos Administrativos.xls'
    lista = []
    queryset = list(contrato)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Contrato':
                valor.append(i.contrato.numero_contrato)
            elif j == 'Empresa':
                valor.append(i.contrato.empresa.nome.upper())
            elif j == 'Tipo de Contrato':
                valor.append(i.contrato.tipo_contrato.upper())
            elif j == 'Data Vigente':
                valor.append(str(i.contrato.data_inicio))
            elif j == 'Valor Total':
                valor.append(i.contrato.valor_total)
            elif j == 'Situação':
                valor.append(i.contrato.situacao.upper())
            elif j == 'Gestor Titular':
                valor.append(i.gestor_titular)
            elif j == 'Gestor Substituto':
                valor.append(i.gestor_substituto)
            elif j == 'Fiscal Titular':
                valor.append(i.fiscal_titular)
            elif j == 'Fiscal Substituto':
                valor.append(i.fiscal_substituto)

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


# def exportar_pdf(request, name_municipios, modalidades, name_regioes, regioes, tipo_localizacao):


def exportar_excel_servidor_lotado(request):
    queryset = filtro_servidores(request)
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
                valor.append(i[3].upper())
        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_pdf_servidor_lotado(request, id_unidade):
    template_path = 'administracao/unidades-administrativas/partials/_servidor-lotado-pdf.html'
    lotados= filtro_servidores(request, id_unidade)

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/servidores-lotados.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'lotados': lotados, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Servidores Lotados.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_contratos(request, vinculo, gestor_titular):
    template_path = 'administracao/contrato/partials/contratos-pdf.html'

    data = date.today()
    user = request.session['username']
    nome = Usuarios.objects.get(login = user)
    data_hora = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/contrato_adm.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    if not gestor_titular:
        ids = Contrato_contrato.objects.values_list('id', flat= True)
        contratos = Contrato_gestor.objects.filter(contrato__in= ids)
        quantidade_contratos = contratos.count()

        contexto = { 'data': data, 'data_hora': data_hora, 'nome':nome, 'quantidade_contratos':quantidade_contratos, 'contratos':contratos, 'url_logo': url_logo, 'url_atena': url_atena}
    else:
        contratos = filtro_contratos(request, vinculo)
        quantidade_contratos = contratos.count()
        contexto = { 'data': data, 'data_hora': data_hora, 'nome':nome, 'quantidade_contratos':quantidade_contratos, 'contratos':contratos, 'gestores': gestor_titular, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Contratos.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_link(request, links, qtd_links, endereco):
    template_path = 'administracao/unidades/partials/_unidade-links-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-infraestrutura-redes.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'links': links, 'qtd_links': qtd_links, 'endereco': endereco, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Links de Tecnologia.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_unidades(request, enderecos):
    template_path = 'administracao/unidades/partials/_unidades-pdf.html'
    unidade= enderecos.exclude(id__in = [669, 723, 724, 722, 741, 738])

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/servidores-lotados.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'enderecos': unidade, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Unidades Educacionais.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_unidades_completo(request, endereco, links, qtd_links, fundiaria, img_frente, img_aerea, coex, consorcio, equipe_presidente, equipe_tesoureiro, equipe_secretario1, equipe_secretario2, equipe_secretario3, equipe_secretario4):
    template_path = 'administracao/unidades/partials/_unidade-pdf-completo.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-infraestrutura-redes.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    if Extincao.objects.filter(fundiaria = fundiaria).exists():
        extincao = Extincao.objects.get(fundiaria = fundiaria)
    else:
        extincao = None

    if Energia.objects.filter(fundiaria = fundiaria).exists():
        energia = Energia.objects.filter(fundiaria = fundiaria)
    else:
        energia = None

    if img_frente != "Não contém imagem":
        img1 = str(settings.BASE_DIR) + '/static/' +  img_frente.path_arquivo()
        # img1 = 'C:/Users/franklin.farias/Documents/Programação/Atena/nl_SEE/static/' +  img_frente
    else:
        img1 = str(settings.BASE_DIR) + '/static/assets/img/nao-cadastrada.png'
        # img1 = 'C:/Users/franklin.farias/Documents/Programação/Atena/nl_SEE/static/assets/img/nao-cadastrada.png'

    if img_aerea != "Não contém imagem":
        img2 = str(settings.BASE_DIR) + '/static/' +  img_aerea.path_arquivo()
        # img2 = 'C:/Users/franklin.farias/Documents/Programação/Atena/nl_SEE/static/' +  img_aerea
    else:
        img2 = str(settings.BASE_DIR) + '/static/assets/img/nao-cadastrada.png'
        # img2 = 'C:/Users/franklin.farias/Documents/Programação/Atena/nl_SEE/static/assets/img/nao-cadastrada.png'

    contexto = {'links': links, 'qtd_links': qtd_links, 'endereco': endereco, 'fundiaria': fundiaria, 'img1': img1, 'img2': img2, 'extincao': extincao, 'energia': energia, 'coex': coex, 'consorcio': consorcio, 'presidente': equipe_presidente, 'tesoureiro': equipe_tesoureiro,
    'secretario1': equipe_secretario1, 'secretario2': equipe_secretario2, 'secretario3': equipe_secretario3, 'secretario4': equipe_secretario4, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Dados Escolas.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_coex(request, coex, consorcio, endereco, equipe_presidente, equipe_tesoureiro, equipe_secretario1, equipe_secretario2, equipe_secretario3, equipe_secretario4):
    template_path = 'administracao/unidades/partials/_unidade-coex-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-infraestrutura-redes.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'coex': coex, 'consorcio': consorcio, 'endereco': endereco, 'presidente': equipe_presidente, 'tesoureiro': equipe_tesoureiro,
    'secretario1': equipe_secretario1, 'secretario2': equipe_secretario2, 'secretario3': equipe_secretario3, 'secretario4': equipe_secretario4, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Coex.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>'+ html + '</pre>')
    return response
