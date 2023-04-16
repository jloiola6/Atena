import os

def handle_uploaded_file(arquivo, nome, caminho, titulo=None):
    titulo = titulo.replace(' ', '_').replace('/', '-')
    
    caminho = caminho  + titulo
    if not os.path.exists('static/media/'+caminho): #Local
        os.makedirs('static/media/'+caminho)
    # if not os.path.exists('Atena/nl_SEE/static/media/'+caminho): #Produção/Homologação
    #     os.makedirs('Atena/nl_SEE/static/media/'+caminho)

    nome = caminho+'/'+nome
    destination = open('static/media/'+nome, 'wb+') #Local
    # destination = open('Atena/nl_SEE/static/media/'+nome, 'wb+') #Produção/Homologação
    for chunk in arquivo.chunks():
        destination.write(chunk)
    destination.close()

    return nome