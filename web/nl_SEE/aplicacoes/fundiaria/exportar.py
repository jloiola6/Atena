import imp
from django.http import HttpResponse
from django.template.loader import get_template
import xlwt
from xhtml2pdf import pisa

from .filtros import *
from .models import *

from aplicacoes.administracao.models import *
from django.conf import settings

def exportar_pdf_escola(request, fundiaria, img_frente, img_aerea):
    template_path = 'fundiaria/partials/_escola-pdf.html'

    url_logo = str(settings.BASE_DIR) + '/static/assets/img/fundiaria-cabecalho.png'
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
        img1 = '/home/suporte/Atena/nl_SEE/static/' +  img_frente.path_arquivo()
    else:
        img1 = '/home/suporte/Atena/nl_SEE/static/assets/img/nao-cadastrada.png'

    if img_aerea != "Não contém imagem":
        img2 = '/home/suporte/Atena/nl_SEE/static/' +  img_aerea.path_arquivo()
    else:
        img2 = '/home/suporte/Atena/nl_SEE/static/assets/img/nao-cadastrada.png'

    contexto = {'fundiaria': fundiaria, 'img1': img1, 'extincao': extincao, "img2": img2, 'energia': energia, 'url_logo': url_logo, 'url_atena': url_atena}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Folha da Escola.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response
