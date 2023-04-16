# from django.http import HttpResponse
# from nl_SEE.aplicacoes.lotacao.models import *
# from datetime import datetime


# template_path = 'lotacao/lotacao/partials/_lotacoes-pdf.html'


# lotacoes= Servidor_lotacao.objects.all()
# print()

# contexto = { 'data': data, 'data_hora': data_hora}

# response = HttpResponse(content_type='application/pdf')
# response['Content-Disposition'] = 'attachment; filename="Lotações.pdf"'

# template = get_template(template_path)
# html = template.render(contexto)

# pisa_status = pisa.CreatePDF(html, dest=response)
# if pisa_status.err:
#     return HttpResponse('We had some errpors <pre>' + html + '</pre>')
# return response