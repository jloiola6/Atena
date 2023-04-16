from imp import new_module
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import xlwt

from aplicacoes.administracao.models import Grade, Professor_aluno, Aluno_turma, Grade_professor_adm, Etapa, Turmas
from aplicacoes.usuario.models import Usuarios
from aplicacoes.lotacao.models import *
from aplicacoes.terceirizacao.models import Contrato_lotacao
from aplicacoes.lotus.models import Servidor_lotacao as Lotacao_lotus, Servidor_lotacao_turma as Turma_lotus, Servidor_ocorrencia as Ocorrencia_lotus, Servidor_contrato as Lotus_contrato, Servidor_contrato_aditivo as Lotus_contrato_aditivo
# from fpdf import FPDF, HTMLMixin

from .filtros import *
from .models import *

from django.shortcuts import render
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from datetime import datetime, date

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


def exportar_excel_servidores(request):
    servidores = filtro_servidores(request)
    names = ['matricula', 'nome', 'cpf']
    colunas = []
    for name in names:
        if request.POST.get(name) == 'on' and name == 'matricula':
            colunas.append('N° Matricula')
        elif request.POST.get(name) == 'on' and name == 'nome':
            colunas.append('Nome')
        elif request.POST.get(name) == 'on' and name == 'cpf':
            colunas.append('CPF')
        # elif request.POST.get(name) == 'on' and name == 'situacao':
        #     colunas.append('Situação')


    model = 'Servidores - Gestão de Pessoas'
    filename = 'Servidores - Gestão de Pessoas.xls'
    lista = []
    queryset = list(servidores)
    for i in queryset:
        valor = []
        for j in colunas:
            if j == 'N° Matricula':
                valor.append(i['matricula'])
            elif j == 'Nome':
                valor.append(i['nome'])
            elif j == 'CPF':
                valor.append(i['cpf'])
            # elif j == 'Situação':
            #     valor.append(i['situacao'])

        lista.append(valor)
    columns = tuple(colunas)
    response = export_xlsx(model, filename, lista, columns)
    return response


def exportar_pdf_servidores(request):
    exportar = filtro_servidores(request)
    template_path = 'lotacao/servidor/partials/_servidor-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/fundiaria-cabecalho.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'exportar': exportar, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Servidores.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response

def exportar_pdf_lotacao(request, id_lotacao, user):
    template_path = 'lotacao/contrato/partials/_lotacao-pdf.html'

    #Imagens do cabeçalho
    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    #Informações do usuario de data atual
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()

    #Pesquisa para trazer o objeto do servidor
    lotacoes = Servidor_lotacao.objects.get(id= id_lotacao)

    #lista para armazenar informações sobre a grade do servidor em cada turma
    grades=[]
    vinculacao_aluno=[]

    #Pesquisa para buscar os turnos que o servidor trabalha.
    

    #Condição para verificar se o servidor é professor de unidade Adm, se for, retorna o objeto com os dados da lotação.
    if Grade_professor_adm.objects.filter(professor= id_lotacao, status=1).exists():
        professor_adm = Grade_professor_adm.objects.get(professor= lotacoes.id)
    else:
        professor_adm = None
    
    if Grade.objects.filter(professor= id_lotacao, disciplina__isnull= False).values_list('turma__turno', flat= True).distinct().exists():
        turnos = Grade.objects.filter(professor= id_lotacao, disciplina__isnull= False).values_list('turma__turno', flat= True).distinct()
    else:
        turnos = Grade.objects.filter(professor= id_lotacao, disciplina__isnull= True).values_list('turma__turno', flat= True).distinct()
    #Busca o ID dos alunos para servir como parametro em outras buscas
    id_alunos = Professor_aluno.objects.filter(professor= id_lotacao).values_list('aluno__id', flat= True).distinct()
    
    #Condição para verificar se o servidor está vinculado a algum aluno, se estiver vinculado é feito uma busca pelo objeto para trazer todos os dados.
    for id_aluno in id_alunos:
        if Professor_aluno.objects.filter(professor= id_lotacao):
            for aluno in Aluno_turma.objects.filter(aluno_id= id_aluno).values('aluno__nome', 'turma__nome', 'turma__turno', 'turma__etapa'):
                for etapa in Etapa.objects.filter(id = aluno['turma__etapa']):
                    nome_aluno = aluno['aluno__nome']
                    turno = aluno['turma__turno']
                    turma= aluno['turma__nome']
                    texto = f'{nome_aluno}, {turma}, {turno}, {etapa}'
                    vinculacao_aluno.append(texto.split(','))
         
    #Busca todas as disciplinas que o servidor ministra.
    disciplinas= Grade.objects.filter(professor= id_lotacao, disciplina__isnull= False).values_list('disciplina__nome', flat= True).distinct()

    #Percorre as disciplinas que o servidor ministra e junta as informações de cada grade (disciplina, turma, serie, etapa)
    for disciplina in disciplinas:
        for turno in turnos:
            if Grade.objects.filter(professor= id_lotacao, disciplina__nome= disciplina, turma__turno= turno).exists():
                for ano_serie in Grade.objects.filter(professor= id_lotacao, disciplina__nome= disciplina, turma__turno= turno).values_list('turma__ano_serie', flat= True).distinct():
                    for turma in Grade.objects.filter(professor= id_lotacao, disciplina__nome= disciplina, turma__turno= turno, turma__ano_serie= ano_serie).values('turma__nome','turma__etapa', 'turma__turno').distinct():
                        for etapa in Etapa.objects.filter(id = turma['turma__etapa']):
                            nome = turma['turma__nome']
                            turno = turma['turma__turno']
                            texto = f'{nome}, {disciplina}, {turno}, {etapa}'
                            grades.append(texto.split(','))

    #Percorre as rotas que o servidor ministra e junta as informações de cada grade (rotas, turma, serie, etapa)
    rotas= Grade.objects.filter(professor= id_lotacao, disciplina__isnull= True).values_list('rota', flat= True).distinct()
    for rota in rotas:
        for turno in turnos:
            if Grade.objects.filter(professor= id_lotacao, rota= rota, turma__turno= turno).exists():
                for ano_serie in Grade.objects.filter(professor= id_lotacao, rota= rota, turma__turno= turno).values_list('turma__ano_serie', flat= True).distinct():
                    for turma in Grade.objects.filter(professor= id_lotacao, rota= rota, turma__turno= turno, turma__ano_serie= ano_serie).values('turma__nome','turma__etapa','turma__turno').distinct():
                        for etapa in Etapa.objects.filter(id = turma['turma__etapa']):
                            nome = turma['turma__nome']
                            turno = turma['turma__turno']

                            if lotacoes.funcao != 'Professor(a) AEE' and lotacoes.funcao != 'Coordenador(a) Pedagógico(a) de Anos':
                                texto = f'{nome}, {rota}, {turno}, {etapa}'
                            else:
                                texto = f'{nome}, {turno}, {etapa}'
                                
                            grades.append(texto.split(','))

    if Lotacao_assinatura.objects.filter(lotacao= lotacoes).exists():
        lotacao_assinatura = Lotacao_assinatura.objects.get(lotacao= lotacoes)
    else:
        lotacao_assinatura = None

    #Gambiarra (Controlar o for de <br>)
    espacos = 7 - (len(grades) + 2)
    espacos = range(espacos)

    #Dados enviados para o pdf
    contexto = {'vinculacao_aluno':vinculacao_aluno,'lotacoes': lotacoes, 'grades': grades, 'nome': nome, 'data': data, 'lotacao_assinatura': lotacao_assinatura, 'professor_adm': professor_adm, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Memorando de Lotação.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response

def exportar_pdf_contrato(request, user, contrato):
    template_path = 'lotacao/contrato/partials/_contrato-pdf.html'
    contratos = Servidor_contrato.objects.get(id= contrato.id)
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()
    contato = Servidor_contato.objects.filter(servidor= contratos.servidor, tipo_contato__in= ['C', 'T'] ).last()
    endereco = Servidor_endereco.objects.get(servidor= contratos.servidor)

    secretario = Servidor_lotacao.objects.filter(contrato__cargo__id= 76).last()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/contrato.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'contratos': contratos, 'data': data, 'contato':contato, 'endereco':endereco, 'secretario':secretario, 'nome': nome, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Contrato.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_declaracao(request, servidor):
    template_path = 'lotacao/servidor/partials/_declaracao-pdf.html'
    servidores = servidor
    data = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'servidores': servidores, 'data':data, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Declaracão.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_aditivo(request, contrato, servidor):
    template_path = 'lotacao/contrato/partials/_contrato-aditivo-pdf.html'
    contratos = Servidor_contrato.objects.get(id= contrato.id)
    aditivos = Servidor_contrato_aditivo.objects.filter(contrato= contrato).last()
    endereco = Servidor_endereco.objects.get(servidor= servidor)
    contato = Servidor_contato.objects.filter(servidor= servidor, tipo_contato__in= ['C', 'T']).last()
    secretario = Servidor_lotacao.objects.filter(contrato__cargo__id= 76).last()
    data = date.today()

    user = request.session['username']
    nome = Usuarios.objects.get(login = user)
    data_hora = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/termo-aditivo.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'contratos': contratos, 'data': data, 'aditivos': aditivos, 'endereco': endereco, 'nome': nome, 'data_hora': data_hora, 'contato': contato, 'secretario':secretario, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Termo Aditivo ao Contrato.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_contratos(request, contratos, quantidade):
    template_path = 'lotacao/contrato/partials/_exportar-contratos-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'
    nome = Usuarios.objects.get(login = request.session['username'])
    data = date.today()


    #Mandar as variaveis pro template
    contexto = {'logo': url_logo, 'atena': url_atena, 'contratos': contratos, 'quantidade': quantidade, 'nome': nome, 'data': data}

    #Mandar exportar
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Contratos.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response

def exportar_pdf_lotacao_tabela(request, quantidade_lotacoes):
    template_path = 'lotacao/lotacao/partials/_lotacoes-pdf.html'

    data = date.today()

    user = request.session['username']

    lotacoes = filtro_lotacao(request)
    nome = Usuarios.objects.get(login = user)
    data_hora = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'data': data, 'data_hora': data_hora, 'nome':nome, 'quantidade_lotacoes':quantidade_lotacoes, 'lotacoes':lotacoes, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Lotações.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_lotacao_lotus(request, user, servidor, id_lotacao):
    template_path = 'lotacao/contrato/partials/_lotacao-lotus-pdf.html'

    nome = Usuarios.objects.get(login = user)
    data = datetime.today()

    lotacoes = Lotacao_lotus.objects.get(id= id_lotacao)
    servidor = Servidor.objects.get(cpf= lotacoes.cpf)
    contrato = Lotus_contrato.objects.get(id= lotacoes.id_contrato)
    # contrato = Lotus_contrato.objects.filter(cpf= lotacoes.cpf).last()
    turma_lotus = Turma_lotus.objects.filter(matricula= lotacoes.matricula, digito= lotacoes.digito)

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    # grades = []
    # for disciplina in Turma_lotus.objects.filter(id_lotacao= lotacoes.id, disciplina__isnull= False).values_list('disciplina', flat= True).distinct():
    #     texto = f'{disciplina} | '
    #     for turno in ['1º turno', '2º turno', '3º turno']:
    #         if Turma_lotus.objects.filter(id_lotacao= lotacoes.id, disciplina= disciplina, turno= turno).exists():
    #             texto += f'{turno} | '
    #             for ano_serie in Turma_lotus.objects.filter(id_lotacao= lotacoes.id, disciplina= disciplina, turno= turno).values_list('turma', flat= True).distinct():
    #                 texto += f'{ano_serie} ('
    #                 for turma in Turma_lotus.objects.filter(id_lotacao= lotacoes.id, disciplina= disciplina, turno= turno, turma= ano_serie).values_list('turma', flat= True).distinct():
    #                     texto += f'{turma[-1]}, '
    #                 texto = texto[:-6]
    #                 texto += ')'
    #                 grades.append(texto)
    #                 texto = f'{disciplina} | {turno} | '

    contexto = {'lotacoes': lotacoes, 'servidor': servidor, 'nome': nome, 'data': data, 'turma_lotus': turma_lotus, 'contrato': contrato, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Memorando de Lotação Lotus.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_lotus_contrato(request, user, contrato, id_contrato_lotus):
    template_path = 'lotacao/contrato/partials/_contrato-lotus-pdf.html'
    contratos = Lotus_contrato.objects.get(id= id_contrato_lotus)
    servidor = Servidor.objects.get(cpf= contratos.cpf)
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()
    contato = Servidor_contato.objects.filter(servidor= servidor, tipo_contato__in= ['C', 'T'] ).last()
    endereco = Servidor_endereco.objects.get(servidor= servidor)

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/contrato.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'contratos': contratos, 'data': data, 'contato':contato, 'endereco':endereco, 'servidor':servidor, 'nome': nome, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Contrato Lotus.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_vdp(request):
    template_path = 'lotacao/vdp/partials/vdp-pdf.html'

    data = date.today()

    user = request.session['username']

    vdps = filtro_vdp(request)
    quantidade_vdp = vdps.count()
    nome = Usuarios.objects.get(login = user)
    data_hora = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = { 'data': data, 'data_hora': data_hora, 'nome':nome, 'quantidade_vdp':quantidade_vdp, 'vdps':vdps, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vdp.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def pdf_contrato_cancelamento(request, user, contrato):
    template_path = 'lotacao/contrato/partials/_contrato-cancelamento-pdf.html'
    contratos = Servidor_contrato.objects.get(id= contrato.id)
    lotacao = Servidor_lotacao.objects.filter(contrato= contratos).values('id', 'unidade_adm__nome', 'unidade_escolar__escola__nome_escola', 'turno_manha', 'turno_tarde', 'turno_noite').last()
    grades = Grade.objects.filter(professor= lotacao['id'])
    nome = Usuarios.objects.get(login = user)
    data = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/contrato.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    data_cancelamento = request.POST.get('data_cancelamento')
    motivo_cancelamento = request.POST.get('motivo_cancelamento')

    cancelamento = Servidor_contrato.objects.get(id=contrato.id)
    cancelamento.data_cancelamento = data_cancelamento
    cancelamento.motivo_cancelamento = motivo_cancelamento
    cancelamento.situacao = 'EXONERADO/RESCISO'
    cancelamento.save()

    data_cancelamento = data_cancelamento.split('-')
    data_cancelamento = f'{data_cancelamento[2]}/{data_cancelamento[1]}/{data_cancelamento[0]}'

    contexto = {'contratos': contratos, 'data': data, 'nome': nome, 'lotacao': lotacao, 'grades': grades, 'url_logo': url_logo, 'url_atena': url_atena, 'data_cancelamento': str(data_cancelamento), 'motivo_cancelamento': motivo_cancelamento}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Cancelamento de Contrato.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response


def exportar_pdf_registro(request):
    template_path = 'lotacao/registro/partials/_registro-pdf.html'
    lotacoes = filtro_registro(request)
    lotacoes1= []
    for lotacao in lotacoes:
        lotacoes_filtro= Historico.objects.filter(tabela= 'lotacao_servidor_lotacao', objeto= lotacao['id']).order_by('-id').values('log__usuario__nome', 'log__usuario__id', 'data', 'objeto')

        if lotacoes_filtro.exists():
            lotacoes1.append((lotacoes_filtro, lotacao['contrato__servidor__nome'], lotacao['unidade_adm__endereco__municipio'], lotacao['unidade_escolar__municipio'], lotacao['unidade_adm__nome'], lotacao['unidade_escolar__escola__nome_escola'], lotacao['numero_memorando']))
        else:
            lotacoes_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
            lotacoes1.append((lotacoes_filtro, lotacao['contrato__servidor__nome'], lotacao['unidade_adm__endereco__municipio'], lotacao['unidade_escolar__municipio'], lotacao['unidade_adm__nome'], lotacao['unidade_escolar__escola__nome_escola'], lotacao['numero_memorando']))

    data = datetime.today()

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/divisao-lotacao.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'registros':lotacoes1, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Registro.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')

    return response


def exportar_registro_contrato(request):
    template_path = 'lotacao/registro/partials/_registro-contrato-pdf.html'
    contratos = filtro_registro_contrato(request)
    contrato1= []
    for contrato in contratos:
        contratos_filtro= Historico.objects.filter(tabela= 'lotacao_servidor_contrato', objeto= contrato['id']).order_by('-id').values('log__usuario__nome', 'log__usuario__id', 'data', 'objeto')
        tecnico = request.GET.get('tecnico')
        if tecnico != None and tecnico != '':
            caux = list(Historico.objects.filter(tabela= 'lotacao_servidor_contrato', objeto= contrato['id']).values('log__usuario__id'))
            if(caux[-1]['log__usuario__id']) == int(tecnico):
                if contratos_filtro.exists():
                    contrato1.append((contratos_filtro, contrato['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))

                else:
                    contratos_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
                    contrato1.append((contratos_filtro['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))
        else:
            if contratos_filtro.exists():
                contrato1.append((contratos_filtro, contrato['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))
            else:
                contratos_filtro = [{'log__usuario__nome': 'Turmalina', 'data': 'Turmalina'}]
                contrato1.append((contratos_filtro, contrato['servidor__nome'], contrato['municipio'], contrato['cargo__nome'], contrato['numero_contrato']))

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/contrato.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    contexto = {'registros':contrato1, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Registro Contrato.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')

    return response


def exportar_relatorio(request):
    template_path = 'lotacao/qualidade/partials/_qualidade-relatorio-pdf.html'

    anomes = request.POST.get('campo-mes')
    mes = anomes.split('-')[-1]

    if mes != '':
        agendamentos = Agendamento.objects.filter(data__contains = anomes, atendimento_id = request.POST.get('servico'))
    else:
        agendamentos = Agendamento.objects.filter(atendimento_id = request.POST.get('servico'))
    
    
    
    data = date.today()

    if len(str(data.month)) != 2:
        mesatual = '0'+str(data.month)
    else:
        mesatual = str(data.month)
    atende = Atendimento.objects.filter(id = request.POST.get('servico')).values('atendente__nome', 'servico__nome')
    meses = {'01':'Janeiro', '02':'Fevereiro', '03':'Março', '04':'Abril', '05':'Maio', '06':'Junho', '07':'Julho', '08':'Agosto', '09':'Setembro', '10':'Outubro', '11':'Novembro', '12':'Dezembro', '': 'Todos'}

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/qualidade.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    if Atendimento.objects.get(id= request.POST.get('servico')).servico.id == 2:
        psicologo = True
        relatorio = {
            'concluidos_interno': agendamentos.filter(atividade = 'Interno', status = 1).count(),
            'concluidos_externo': agendamentos.filter(atividade = 'Externo', status = 1).count(),
            'concluidos_soma': agendamentos.filter(atividade = 'Externo', status = 1).count() + agendamentos.filter(atividade = 'Interno', status = 1).count(),
            
            'cancelados_interno': agendamentos.filter(atividade = 'Interno', status__in = [2]).count(),
            'cancelados_externo': agendamentos.filter(atividade = 'Externo', status__in = [2]).count(),
            'cancelados_soma': agendamentos.filter(atividade = 'Externo', status__in = [2]).count() + agendamentos.filter(atividade = 'Interno', status__in = [2]).count(),
            
            'faltaram_interno': agendamentos.filter(atividade = 'Interno', status__in = [3]).count(),
            'faltaram_externo': agendamentos.filter(atividade = 'Externo', status__in = [3]).count(),
            'faltaram_soma': agendamentos.filter(atividade = 'Externo', status__in = [3]).count() + agendamentos.filter(atividade = 'Interno', status__in = [3]).count(),
            
            'soma_interno': agendamentos.filter(atividade = 'Interno', status__in = [1, 2, 3]).count(),
            'soma_externo': agendamentos.filter(atividade = 'Externo', status__in = [1, 2, 3]).count(),
            'total': agendamentos.filter(atividade = 'Externo', status__in = [1, 2, 3]).count() + agendamentos.filter(atividade = 'Interno', status__in = [1, 2, 3]).count()
        }
    else:
        psicologo = False
        relatorio = {
            'concluidos_interno': agendamentos.filter(atividade = 'Interno', status = 1).count(),
            'concluidos_externo': agendamentos.filter(atividade = 'Externo', status = 1).count(),
            
            'cancelados_interno': agendamentos.filter(atividade = 'Interno', status__in = [2, 3]).count(),
            'cancelados_externo': agendamentos.filter(atividade = 'Externo', status__in = [2, 3]).count(),
            
            'soma_interno': agendamentos.filter(atividade = 'Interno', status__in = [1, 2, 3]).count(),
            'soma_externo': agendamentos.filter(atividade = 'Externo', status__in = [1, 2, 3]).count(),
            
            'soma_concluidos': agendamentos.filter(status = 1).count(),
            'soma_cancelados': agendamentos.filter(status__in = [2, 3]).count(),
            'total': agendamentos.filter(status__in = [1, 2, 3]).count()
        }

    print(psicologo)
    print(psicologo == True)
        
    contexto = {
    'contratos': 'Hello',
    'data': data,
    'atende': atende,
    'mes': meses[mes],
    'mesatual': meses[mesatual],
    'url_logo': url_logo,
    'url_atena': url_atena,
    'relatorio': relatorio,
    'psicologo': psicologo
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Relatório Qualidade de Vida.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response