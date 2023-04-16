from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from unidecode import unidecode

from aplicacoes.administracao.exportar import *
from aplicacoes.administracao.models import *
from aplicacoes.coex.models import *
from aplicacoes.core.views_gerais.partials import *
from aplicacoes.core.views import (global_municipios, global_regioes,global_zoneamentos, verificar_manutencao)

from aplicacoes.lotacao.models import Servidor_lotacao
from aplicacoes.usuario.models import Logs, Permissao, Usuarios, Servico
from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.coex.actions.comite import *
from aplicacoes.coex.filtros import filtro_unidades


def unidades_educacionais(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    #Definindo template, usuário e que dados serão mostrados na página
    template_name = 'coex/comite/comites.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    escola_coex = Coex.objects.values_list('escola__id', flat = True)
    enderecos = Endereco.objects.filter(tipo='S', escola__id__in = escola_coex).values('escola__id','escola__cod_inep', 'escola__nome_escola', 'municipio', 'regiao', 'tipo_localizacao').order_by('escola__nome_escola')

    comites= Coex.objects.all().values('nome_empresarial').distinct()
    situacoes= Coex.objects.all().values('status').distinct()
    unidades = Coex.objects.all().values('escola__nome_escola')

    enderecos = filtro_unidades(request, user)

    login = ('ana.marina', 'erick.nascimento', 'fabio.santos', 'franklin.farias', 'joaopedro.passos', 'joaoteixeira.netto', 'josecarlos.souza', 'tharlis.seixas')
    if user not in login:
        enderecos = enderecos.exclude(id__in = [669, 723, 724, 722])

    #Coleta a página atual para atualzar informações na tabela
    page = request.GET.get('page')
    if page is None:
        page = '1'

    #Estabelecendo dados apresentados pela página coletada acima
    quantidade_escolas = enderecos.count()


    paginator = Paginator(enderecos, 15)
    enderecos = paginator.get_page(page)

    #Estabelecendo paginação da tabela
    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():
        #Capturando get da url
        gets = (request.get_full_path().split('?')[1])

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        if "page" not in gets:
            gets = f'page={page}&' + gets

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', f'page={paginator.num_pages}')

    return TemplateResponse(request, template_name, locals())


def comite_perfil(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/comite-perfil.html'

    user = request.session['username']
    aplicacao = 'COEX'

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id = request.GET.get('id')

    try:
        escola = Escola.objects.get(id= id)
    except:
        return HttpResponseRedirect('/coex')

    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    if Coex.objects.filter(escola= escola, status=1).exists():
        coex = Coex.objects.get(escola= escola, status=1)

        if Consorcio.objects.filter(cnpj= coex.cnpj, status=1).exists():
            consorcio = Consorcio.objects.get(cnpj= coex.cnpj, status=1)

    try:
        if id:
            endereco = Endereco.objects.get(escola= escola, id= id)
        else:
            endereco = Endereco.objects.get(escola= escola)
    except:
        return HttpResponseRedirect('/coex')

    contatos = Contato.objects.filter(endereco= endereco)

    diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'

    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
        diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).exists():
        pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
        ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
        administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
        secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    if Consorcio.objects.filter(cnpj= coex.cnpj).exists():
        consorcio = Consorcio.objects.get(cnpj= coex.cnpj)
        equipe = Equipe_comite.objects.filter(consorcio= consorcio).values('servidor__nome', 'cargo', 'nome', 'servidor__id')
        equipe_presidente = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 4').values('nome').last()
    else:
        equipe = Equipe_comite.objects.filter(coex= coex).values('servidor__nome', 'cargo', 'nome', 'servidor__id')
        equipe_presidente = Equipe_comite.objects.filter(coex= coex, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(coex= coex, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 4').values('nome').last()

    qtd_documentos = 0

    if Arquivo.objects.filter(coex = coex).exists():
        qtd_documentos = Arquivo.objects.filter(coex = coex).count()
        qr_documentos = Arquivo.objects.filter(coex = coex)[:3]

        documentos = []
        for documento in qr_documentos:
            formato_documento = str(documento.arquivo).split('.')[1]
            caminho = str(documento.path_arquivo())
            dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
            documentos.append(dict_documento)

    if request.method == 'POST':
        if 'btn-excluir' in request.POST:
            valor = request.POST.get('btn-excluir')
            id_documento = valor.split('-')[-1]
            coex_excluir(request, id_documento)
            return HttpResponseRedirect(f'/coex/comite-perfil?id={id}')

    return TemplateResponse(request, template_name, locals())


def comite_perfil_antigo(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/comite-perfil.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)
    id = request.GET.get('id')
    aplicacao = Servico.objects.get(id= 22).aplicacao.nome

    # coex = Coex.objects.get(escola__id= id)
    escola, coex, contatos, possui_contatos, endereco, diretor, pedagogico, ensino, secretario, administrativo, escola_etapas = dados_unidades(aplicacao, id)

    if Consorcio.objects.filter(cnpj= coex.cnpj).exists():
        consorcio = Consorcio.objects.get(cnpj= coex.cnpj)
        equipe = Equipe_comite.objects.filter(consorcio= consorcio).values('servidor__nome', 'cargo', 'nome', 'servidor__id')
        equipe_presidente = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(consorcio= consorcio, cargo= 'Secretário 4').values('nome').last()
    else:
        equipe = Equipe_comite.objects.filter(coex= coex).values('servidor__nome', 'cargo', 'nome', 'servidor__id')
        equipe_presidente = Equipe_comite.objects.filter(coex= coex, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(coex= coex, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 4').values('nome').last()

    qtd_documentos = 0

    if Arquivo.objects.filter(coex = coex).exists():
        qtd_documentos = Arquivo.objects.filter(coex = coex).count()
        qr_documentos = Arquivo.objects.filter(coex = coex)[:3]

        documentos = []
        for documento in qr_documentos:
            formato_documento = str(documento.arquivo).split('.')[1]
            caminho = str(documento.path_arquivo())
            dict_documento = {'id': documento.id, 'descricao': documento.descricao_simples(), 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
            documentos.append(dict_documento)

    if request.method == 'POST':
        if 'btn-excluir' in request.POST:
            valor = request.POST.get('btn-excluir')
            id_documento = valor.split('-')[-1]
            coex_excluir(request, id_documento)
            return HttpResponseRedirect(f'/coex/comite-perfil?id={id}')

    return TemplateResponse(request, template_name, locals())


def equipe_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/equipe-formulario.html'
    user = request.session['username']
    edicao = False

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_escola = request.GET.get('id')

    escola = Escola.objects.get(id= id_escola)
    endereco = Endereco.objects.get(escola= escola, tipo= 'S')
    coex = Coex.objects.get(escola= escola)

    servidores = list(Servidor_lotacao.objects.filter(unidade_escolar = endereco).values_list('contrato__servidor__id', 'contrato__servidor__nome').order_by('contrato__servidor__nome'))

    if Equipe_comite.objects.filter(coex= coex).exists():
        edicao = True
        equipe_presidente = Equipe_comite.objects.filter(coex= coex, cargo= 'Presidente').values('servidor__id', 'servidor__nome').last()
        equipe_tesoureiro = Equipe_comite.objects.filter(coex= coex, cargo= 'Tesoureiro').values('servidor__id', 'servidor__nome').last()
        equipe_secretario1 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 1').values('nome').last()
        equipe_secretario2 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 2').values('nome').last()
        equipe_secretario3 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 3').values('nome').last()
        equipe_secretario4 = Equipe_comite.objects.filter(coex= coex, cargo= 'Secretário 4').values('nome').last()
        coex_dado = Coex.objects.get(id= coex.id, escola= escola)

        # print(servidores)
        # for gestor in (equipe_presidente, equipe_tesoureiro, equipe_secretario1, equipe_secretario2):
        #     if gestor['servidor__id'] != None:
        #         servidores.append((gestor['servidor__id'], gestor['servidor__nome']))


    if request.method == "POST":
        formulario_equipe(request, edicao)
        return HttpResponseRedirect(f'/coex/comite-perfil?id={escola.id}')

    return TemplateResponse(request, template_name, locals())


def documento_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/documento-formulario.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)
    escolas = Escola.objects.filter()

    id_escola = request.GET.get('id')
    categorias = ["ATA's","Documentos Pessoais","Edital","Estatuto","Lista de presença","Requerimento","Outros"]
    escola = Escola.objects.get(id= id_escola)
    coex = Coex.objects.get(escola= escola, status= 1)
    qr_arquivo = Arquivo.objects.filter(coex = coex).values('id').count()

    if request.method == "POST":
        formulario_documento(request, coex)
        if qr_arquivo < 3 :
            return HttpResponseRedirect(f'/coex/comite-perfil?id={escola.id}')
        else:
            return HttpResponseRedirect(f'/coex/gerenciador-documentos?id={escola.id}')
    return TemplateResponse(request, template_name, locals())


def comite_formulario(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/comite-formulario.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    escola_coex = Coex.objects.values_list('escola__id', flat = True)
    escolas_id = Escola.objects.all().exclude(id__in= escola_coex).values_list('id', flat= True).exclude(id__in=[669, 722, 738, 740])
    escolas = Endereco.objects.filter(id__in= escolas_id, tipo='S').values('escola__id', 'escola__nome_escola', 'municipio', 'escola__cod_inep')

    if request.method == "POST":
        escola_id = formulario_comite(request)
        if escola_id != None:
            return HttpResponseRedirect(f'/coex/comite-perfil?id={escola_id}')
        else:
            return HttpResponseRedirect(f'/coex/comite')

    return TemplateResponse(request, template_name, locals())


def gerenciador_documentos(request):
    if verificar_manutencao() or not verificacao_maxima(request, [22]):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/gerenciador-documentos.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_escola = request.GET.get('id')

    escola = Escola.objects.get(id= id_escola)
    coex = Coex.objects.get(escola= escola)

    qr_documentos = Arquivo.objects.filter(coex = coex)

    documentos = []
    pessoais = []
    ata = []
    estatuto = []
    requerimento = []
    edital = []
    presenca = []
    outros = []

    for documento in qr_documentos:
        formato_documento = str(documento.arquivo).split('.')[1]
        caminho = str(documento.path_arquivo())
        dict_documento = {'id': documento.id, 'descricao': documento.descricao, 'categoria': documento.categoria, 'formato': formato_documento, 'caminho': caminho}
        documentos.append(dict_documento)

        if dict_documento['categoria'] == "ATA's":
            ata.append(dict_documento)
        elif dict_documento['categoria'] == "Documentos Pessoais":
            pessoais.append(dict_documento)
        elif dict_documento['categoria'] == "Edital":
            edital.append(dict_documento)
        elif dict_documento['categoria'] == "Estatuto":
            estatuto.append(dict_documento)
        elif dict_documento['categoria'] == "Lista de presença":
            presenca.append(dict_documento)
        elif dict_documento['categoria'] == "Requerimento":
            requerimento.append(dict_documento)
        elif dict_documento['categoria'] == "Outros":
            outros.append(dict_documento)

    if request.method == 'POST':
        if 'btn-excluir' in request.POST:
            valor = request.POST.get('btn-excluir')
            id_documento = valor.split('-')[-1]
            coex_excluir(request, id_documento)
            return HttpResponseRedirect(f'/coex/gerenciador-documentos?id={id_escola}')

    return TemplateResponse(request, template_name, locals())


def editar_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/editar-endereco.html'
    user = request.session['username']

    municipios = global_municipios
    zoneamentos = global_zoneamentos
    localizacao_diferenciada = ['', 'Terra Indígena', 'Quilombo', 'Área de Assentamento']

    id_endereco = request.GET.get('id')
    if id_endereco in (None, ''):
        return HttpResponseRedirect('/coex/comite/comites')

    endereco = Endereco.objects.get(id= id_endereco)
    if Detalhes_Indigena.objects.filter(escola= endereco.escola.id).exists():
        detalhes_indigenas = Detalhes_Indigena.objects.get(escola= endereco.escola.id)

    name_etnia = []
    etnias = []
    for detalhe in Detalhes_Indigena.objects.all().values('etnia').distinct().order_by('etnia'):
        etnias.append(detalhe['etnia'])

    #Consultando as localizacoes de ensino indigena para filtro
    name_localizacao = []
    localizacoes = []
    for detalhe in Detalhes_Indigena.objects.all().values('localizacao').distinct().order_by('localizacao'):
        localizacoes.append(detalhe['localizacao'])

    #Consultando as aldeias de ensino indigena para filtro
    name_aldeia = []
    aldeias = []
    for detalhe in Detalhes_Indigena.objects.all().values('aldeia').distinct().order_by('aldeia'):
        aldeias.append(detalhe['aldeia'])

    if request.method == 'POST':
        formulario_endereco(request)
        return HttpResponseRedirect(f'/coex/comite-perfil?id={endereco.id}')

    return TemplateResponse(request, template_name, locals())


def editar_contatos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/editar-contatos.html'
    user = request.session['username']
    id_endereco = request.GET.get('id')
    edicao = True

    endereco = Endereco.objects.get(id= id_endereco)
    contatos = Contato.objects.filter(endereco= endereco)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        editar_contato(request, edicao)
        return HttpResponseRedirect(f'/coex/comite-perfil?id={endereco.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    user = request.session['username']
    template_name = 'coex/comite/servidor-perfil.html'
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 22)

    id_endereco = request.GET.get('id')
    id_servidor = request.GET.get('id_servidor')
    id_consorcio = request.GET.get('id_consorcio')

    if id_endereco:
        endereco = Endereco.objects.get(id= id_endereco)
    else:
        consorcio = Consorcio.objects.get(id= id_consorcio)

    servidor = Servidor.objects.get(id= id_servidor)
    historico_base = Atualizacao_cadastral.objects.filter(servidor= servidor.id).last()

    if Servidor_endereco.objects.filter(servidor= servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor= servidor)

    if Servidor_contato.objects.filter(servidor= servidor).exists():
        servidor_contato = Servidor_contato.objects.filter(servidor= servidor)

    if Servidor_banco.objects.filter(servidor= servidor).exists():
        servidor_banco = Servidor_banco.objects.get(servidor= servidor)

    return TemplateResponse(request, template_name, locals())


def servidor_base(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    edicao= True
    template_name = 'coex/comite/servidor-base.html'
    user = request.session['username']

    id_servidor = request.GET.get('id_servidor')
    id_consorcio = request.GET.get('id_consorcio')
    id_endereco = request.GET.get('id')

    if id_endereco:
        endereco = Endereco.objects.get(id= id_endereco)
    else:
        consorcio = Consorcio.objects.get(id= id_consorcio)

    servidor = Servidor.objects.get(id= id_servidor)
    servidor.data_nascimento = str(servidor.data_nascimento)

    generos = ("Masculino", "Feminino", "Não binário", "Outro")
    nacionalidades = ("Brasileiro(a)", "Estrangeiro(a)")

    if request.method == 'POST':
        formulario_servidor_base(request, id_servidor, edicao)
        if id_endereco:
            return HttpResponseRedirect(f'servidor-perfil?id={endereco.id}&id_servidor={servidor.id}')
        else:
            return HttpResponseRedirect(f'servidor-perfil?id_consorcio={ consorcio.id }&id_servidor={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_endereco(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/servidor-endereco.html'
    user = request.session['username']

    id_servidor = request.GET.get('id_servidor')
    id_consorcio = request.GET.get('id_consorcio')
    id_endereco = request.GET.get('id')

    if id_endereco:
        endereco = Endereco.objects.get(id= id_endereco)
    else:
        consorcio = Consorcio.objects.get(id= id_consorcio)

    if Servidor_endereco.objects.filter(servidor = id_servidor).exists():
        servidor_endereco = Servidor_endereco.objects.get(servidor = id_servidor)
    servidor = Servidor.objects.get(id= id_servidor)

    cidades = Cidade.objects.filter(estado__id= 1).order_by('estado__nome')

    if request.method == 'POST':
        formulario_servidor_endereco(request, servidor)
        if id_endereco:
            return HttpResponseRedirect(f'servidor-perfil?id={endereco.id}&id_servidor={servidor.id}')
        else:
            return HttpResponseRedirect(f'servidor-perfil?id_consorcio={ consorcio.id }&id_servidor={servidor.id}')

    return TemplateResponse(request, template_name, locals())


def servidor_contato(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [22], True):
        return HttpResponseRedirect('/')

    template_name = 'coex/comite/servidor-contatos.html'
    user = request.session['username']

    id_servidor = request.GET.get('id_servidor')
    id_consorcio = request.GET.get('id_consorcio')
    id_endereco = request.GET.get('id')

    if id_endereco:
        endereco = Endereco.objects.get(id= id_endereco)
    else:
        consorcio = Consorcio.objects.get(id= id_consorcio)

    servidor = Servidor.objects.get(id= id_servidor)
    contatos = Servidor_contato.objects.filter(servidor= id_servidor)
    qtd_contatos = contatos.count()

    if request.method == 'POST':
        contatos_editar(request, id_servidor)
        if id_endereco:
            return HttpResponseRedirect(f'servidor-perfil?id={endereco.id}&id_servidor={servidor.id}')
        else:
            return HttpResponseRedirect(f'servidor-perfil?id_consorcio={ consorcio.id }&id_servidor={servidor.id}')


    return TemplateResponse(request, template_name, locals())


def inativar_comite(request):
    if not verificacao_maxima(request, [22], True) or verificar_manutencao():
        return HttpResponseRedirect('/usuario/login')

    user = request.session['username']
    template_name = 'coex/comite/inativar-comite.html'

    escola_id = request.GET.get('id')
    comite = Coex.objects.get(escola= escola_id)

    if request.method == 'POST':
        comite_inativar(request, escola_id, user)
        return HttpResponseRedirect(f'comite-perfil?id={escola_id}')

    return TemplateResponse(request, template_name, locals())