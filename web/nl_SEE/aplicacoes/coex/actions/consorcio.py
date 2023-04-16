import re
from aplicacoes.coex.models import *
from aplicacoes.administracao.models import Escola
from aplicacoes.lotacao.models import Servidor_lotacao
from aplicacoes.core.uploads import handle_uploaded_file
from aplicacoes.core.actions import salvar_historico

def remove_non_ascii(text):
    text = text.lower()
    return text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ã', 'a').replace('õ', 'o').replace('ê', 'e').replace('â', 'a').replace('ô', 'o')

def consultar_servidor(servidor, cpf= None):
    if servidor in ('None', ''):
        return None

    if cpf != None and Servidor.objects.filter(cpf= servidor).exists():
        servidor = Servidor.objects.filter(cpf= servidor).last()
    elif Servidor.objects.filter(id= servidor).exists():
        servidor = Servidor.objects.get(id= servidor)
    else:
        servidor = None
    return servidor

def vinculo_escola(request, consorcio=None, escola=None):
    edicao = False

    if not consorcio:
        id_consorcio = request.GET.get('id')
        id_escola = request.POST.get('unidade')

        consorcio = Consorcio.objects.get(id= id_consorcio)
        escola = Escola.objects.get(id= id_escola)

    if not Escola_consorcio.objects.filter(consorcio= consorcio, escola= escola).exists():
        vinculo = Escola_consorcio()
        vinculo.consorcio = consorcio
        vinculo.escola = escola
        vinculo.status = 1
        vinculo.save()
        salvar_historico(request, vinculo, edicao, 'coex_escola_consorcio')

        coex = Coex()
        coex.escola = escola
        coex.cnpj = consorcio.cnpj
        coex.status = 1
        coex.save()
        salvar_historico(request, coex, edicao, 'coex_coex')
    else:
        escola_consorcio = Escola_consorcio.objects.get(consorcio= consorcio, escola= escola)
        escola_consorcio.status = 1
        escola_consorcio.save()
        salvar_historico(request, escola_consorcio, edicao, 'coex_escola_consorcio')

        escola_coex = Coex.objects.get(escola= escola, cnpj= consorcio.cnpj)
        escola_coex.status = 1
        escola_coex.save()
        salvar_historico(request, escola_coex, edicao, 'coex_coex')

        for documento in Arquivo.objects.filter(coex= escola_coex, status=1):
            documento.status = 1
            documento.save()
            salvar_historico(request, documento, edicao, 'coex_arquivo')





def formulario_consorcio(request, edicao):

    id_consorcio = request.GET.get('id')
    nome_consorcio = request.POST.get('nome-consorcio')
    cnpj = request.POST.get('cnpj-consorcio')

    presidente_id = request.POST.get('comite-presidente')
    presidente = consultar_servidor(presidente_id)

    tesoureiro_id = request.POST.get('comite-tesoureiro')
    tesoureiro = consultar_servidor(tesoureiro_id)
    # secretario2_id = request.POST.get('comite-secretario2')
    # secretario2 = consultar_servidor(secretario2_id)

    if request.POST.get('secretario1') != None:
        if len(request.POST.get('secretario1')) > 1:
            secretario1 = request.POST.get('secretario1')
        else:
            secretario1 = None
    else:
        secretario1 = request.POST.get('secretario1')

    if request.POST.get('secretario2') != None:
        if len(request.POST.get('secretario2')) > 1:
            secretario2 = request.POST.get('secretario2')
        else:
            secretario2 = None
    else:
        secretario2 = request.POST.get('secretario2')

    if request.POST.get('secretario3') != None:
        if len(request.POST.get('secretario3')) > 1:
            secretario3 = request.POST.get('secretario3')
        else:
            secretario3 = None
    else:
        secretario3 = request.POST.get('secretario3')

    if request.POST.get('secretario4') != None:
        if len(request.POST.get('secretario4')) > 1:
            secretario4 = request.POST.get('secretario4')
        else:
            secretario4 = None
    else:
        secretario4 = request.POST.get('secretario3')

    if not Consorcio.objects.filter(cnpj= cnpj).exists():
        consorcio = Consorcio()
        consorcio.nome_consorcio = nome_consorcio
        consorcio.cnpj = cnpj
        consorcio.status = 1
        consorcio.save()

        lista_unidades = ['1', '2', '3', '4', '5']
        for i in lista_unidades:
            escola_id = request.POST.get(f'unidade{i}')
            if escola_id != '' and escola_id != None:
                escola = Escola.objects.get(id= escola_id)

                vinculo_escola(request, consorcio, escola)

        salvar_historico(request, consorcio, edicao, 'coex_consorcio')
    else:
        consorcio = Consorcio.objects.get(id = id_consorcio)

        if consorcio.nome_consorcio != nome_consorcio or consorcio.cnpj != cnpj:
            consorcio.nome_consorcio = nome_consorcio
            consorcio.cnpj = cnpj
            consorcio.save()

            salvar_historico(request, consorcio, edicao, 'coex_consorcio')


    dados_equipe = ((presidente, 'Presidente'), (tesoureiro, 'Tesoureiro'), (secretario1, 'Secretário 1'), (secretario2, 'Secretário 2'), (secretario3, 'Secretário 3'), (secretario4, 'Secretário 4'))
    for dado in dados_equipe:
        if dado[0] != None:
            # print(dado[0])
            if '1' in dado[1] or '2' in dado[1] or '3' in dado[1] or '4' in dado[1]:
                if Equipe_comite.objects.filter(consorcio= consorcio, cargo= dado[1]).exists():
                    equipe = Equipe_comite.objects.get(consorcio= consorcio, cargo= dado[1])
                    equipe.nome = dado[0]
                else:
                    equipe = Equipe_comite()
                    equipe.nome = dado[0]
            else:
                if Equipe_comite.objects.filter(consorcio= consorcio, cargo= dado[1]).exists():
                    equipe = Equipe_comite.objects.get(consorcio= consorcio, cargo= dado[1])
                    equipe.servidor = dado[0]
                else:
                    equipe = Equipe_comite()
                    equipe.servidor = dado[0]

            equipe.consorcio = consorcio
            equipe.cargo = dado[1]
            equipe.save()
            salvar_historico(request, equipe, edicao, 'coex_equipe_comite')

    return consorcio.id


def desvinculo_escola(request, consorcio):
    edicao= False
    escola_id = request.POST.get('unidade')
    escola = Escola.objects.get(id= escola_id)
    coex = Coex.objects.get(escola= escola, status=1)



    if Escola_consorcio.objects.filter(consorcio= consorcio, escola= escola_id, status=1).exists():
        escola_consorcio = Escola_consorcio.objects.get(consorcio= consorcio, escola= escola_id, status=1)
        escola_consorcio.status = 0
        escola_consorcio.save()
        salvar_historico(request, escola_consorcio, edicao, 'coex_escola_consorcio')

        for documento in Arquivo.objects.filter(coex= coex, status=1):
            documento.status = 0
            documento.save()
            salvar_historico(request, documento, edicao, 'coex_arquivo')

        coex.status= 0
        coex.save()
        salvar_historico(request, coex, edicao, 'coex_coex')


def consorcio_documento(request, consorcio):
    edicao = False

    qr_arquivo = Arquivo_consorcio.objects.filter(consorcio = consorcio)

    descricao = request.POST.get('descricao')
    documento = request.FILES.get('arquivo')

    versao = qr_arquivo.count() + 1
    if versao > 1:
        nome = f'Documento({versao}).' + str(documento).split('.')[-1]
    else:
        nome = 'Documento.' + str(documento).split('.')[-1]

    categorias = request.POST.get('categorias')
    nome_consorcio = remove_non_ascii(consorcio.nome_consorcio)

    arquivo = Arquivo_consorcio()
    arquivo.consorcio = Consorcio.objects.get(id=consorcio.id)
    arquivo.descricao = descricao
    arquivo.arquivo = handle_uploaded_file(documento, nome, 'Consorcio/', nome_consorcio.upper())
    arquivo.categoria = categorias
    arquivo.status = 1
    arquivo.save()
    salvar_historico(request, arquivo, edicao, 'coex_arquivo_consorcio')


def coex_excluir_consorcio(request, id_documento):
    documento = Arquivo_consorcio.objects.get(id = id_documento)
    documento.delete()
