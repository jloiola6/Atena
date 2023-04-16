from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from aplicacoes.core.models import Confirmacao_lotacao
from aplicacoes.administracao.models import Endereco, Unidade_administrativa_endereco

def exportar_atualizacao_lotacao(request, id_lotacao, servidor_contrato_terceirizado):
    template_path = 'core/servidor/partials/_atualizacao-lotacao-pdf.html'
    url_logo = str(settings.BASE_DIR) + '/static/assets/img/detei.png'
    url_atena = str(settings.BASE_DIR) + '/static/assets/img/ATENA-AZUL.svg'

    municipio = 'a'
    data = datetime.now()
    if not servidor_contrato_terceirizado:
        atualizacao = Confirmacao_lotacao.objects.get(lotacao= id_lotacao)
    else:
        atualizacao = Confirmacao_lotacao.objects.get(terceirizado= id_lotacao)
        if atualizacao.unidade_escolar is not None:
            municipio = Endereco.objects.get(escola_id = atualizacao.unidade_escolar.id).municipio
            print(municipio)
    contexto = {'atualizacao': atualizacao, 'data': data, 'url_logo':url_logo, 'url_atena':url_atena, 'muni': municipio}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Atualização de Lotação.pdf"'

    template = get_template(template_path)
    html = template.render(contexto)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errpors <pre>' + html + '</pre>')
    return response
