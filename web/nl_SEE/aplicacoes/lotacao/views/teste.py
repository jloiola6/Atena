# from django.http import *
# from aplicacoes.lotacao.models import *
# from django.template.response import TemplateResponse
# from xhtml2pdf import pisa
# from django.template.loader import get_template, render_to_string

# def teste(request):
#     m = open('doc/lotacoes.pdf', 'rb')

#     print(m)

#     return FileResponse(m)
# def teste(request):
#     template_path = 'lotacao/contrato/partials/_lotacao-pdf.html'
#     lotacoes= Servidor_lotacao.objects.all()
#     print(lotacoes)

#     contexto = { 'lotacoes': lotacoes}

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="Lotações.pdf"'

#     template = get_template(template_path)
#     html = template.render(contexto)

#     pisa_status = pisa.CreatePDF(html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errpors <pre>' + html + '</pre>')
#     return response
