from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader
from datetime import datetime
import pytz


def handler404(request, exception):
    return render(request, 'atena/pagina-404.html')

def handler500(request):

    user = request.session['username']
    url = request.get_full_path()
    log = request.session['log']

    tz_RB = pytz.timezone('America/Rio_Branco')
    valor = str(datetime.now(tz_RB)).split()
    data = datetime.strptime(valor[0], '%Y-%m-%d').date()
    hora = valor[1].split('.')[0]

    posts = []
    for post in request.POST:
        posts.append((post, request.POST[post], len(request.POST[post])))
    posts = posts[1:]

    html_message = loader.render_to_string(
                'atena/email.html',
                {
                    'user': user,
                    'url':  url,
                    'log':  log,
                    'data':  data,
                    'hora':  hora,
                    'posts': posts,
                }
            )

    send_mail('Detecção de Erro', 'Usuário: '+ user, 'suporteatena@see.ac.gov.br',['suporteatena@see.ac.gov.br'], fail_silently=False, html_message=html_message)
    return render(request, 'atena/pagina-500.html')