from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.usuario.models import Usuarios, Permissao, Logs
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.administracao.models import *
from aplicacoes.administracao.actions.infraestrutura import *

# VIEW DO PERFIRL DE UMA UNIDADE DE ACORDO COM O SEU ENDEREÇO
def infraestrutura_perfil(request, id_endereco):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/infraestrutura/infraestrutura-perfil.html'
    user = request.session['username']

    permissao = Permissao.objects.get(usuario__login= user, servico__id__in= [1, 5])

    try:
        endereco = Endereco.objects.get(id= id_endereco)
    except:
        return HttpResponseRedirect('/administracao')

    escola = endereco.escola
    infraestrutura = endereco.infraestrutura

    if infraestrutura:
        dependencias = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura)

        if dependencias:
            categorias_dependencias = dependencias.values('tipo_dependencia__categoria').distinct()
            tipos_dependencias = dependencias.values('tipo_dependencia__tipo', 'tipo_dependencia__categoria').distinct()

        locais = Infraestrutura_local_funcionamento.objects.filter(infraestrutura= infraestrutura).order_by('local')
        abastecimentos = Infraestrutura_abastecimento_agua.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
        esgotos = Infraestrutura_rede_esgoto.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
        energias = Infraestrutura_fonte_energia.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
        destinacoes = Infraestrutura_destinacao_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
        tratamentos = Infraestrutura_tratamento_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
        recursos = Infraestrutura_recurso_acessibilidade.objects.filter(infraestrutura= infraestrutura).order_by('tipo')


    # id_infraestrutura = request.GET.get('id')
    # infraestrutura = Infraestrutura_geral.objects.get(id= id_infraestrutura)

    # endereco = infraestrutura.endereco
    # escola = endereco.escola

    # quantidade_dependencias = 0
    # quantidade_salas_de_aula = 0

    # dependencias = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura).exclude(tipo__tipo= 'Sala de Aula')
    # quantidade_dependencias = dependencias.count()

    # salas_de_aula = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura, tipo__tipo= 'Sala de Aula')
    # quantidade_salas_de_aula = salas_de_aula.count()

    # locais = Infraestrutura_local_funcionamento.objects.filter(infraestrutura= infraestrutura).order_by('local')
    # abastecimentos = Infraestrutura_abastecimento_agua.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
    # esgotos = Infraestrutura_rede_esgoto.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
    # energias = Infraestrutura_fonte_energia.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
    # destinacoes = Infraestrutura_destinacao_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
    # tratamentos = Infraestrutura_tratamento_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
    # recursos = Infraestrutura_recurso_acessibilidade.objects.filter(infraestrutura= infraestrutura).order_by('tipo')

    return TemplateResponse(request, template_name, locals())

def infraestrutura_formulario(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/infraestrutura/infraestrutura-formulario.html'
    user = request.session['username']

    id_endereco = request.GET.get('id_endereco')
    endereco = Endereco.objects.get(id= id_endereco)
    escola = endereco.escola
    edicao = False

    formas_ocupacoes = ['Próprio', 'Alugado', 'Cedido']

    if Infraestrutura_geral.objects.filter(endereco= endereco).exists():

        infraestrutura = Infraestrutura_geral.objects.get(endereco= endereco)

        local_funcionamento = []
        locais = Infraestrutura_local_funcionamento.objects.filter(infraestrutura= infraestrutura)
        if locais:
            edicao = True

        for local in locais:
            local_funcionamento.append(local.local)

        abastecimento_agua = []
        agua = Infraestrutura_abastecimento_agua.objects.filter(infraestrutura= infraestrutura)
        for abastecimento in agua:
            abastecimento_agua.append(abastecimento.tipo)

        fonte_energia = []
        fontes = Infraestrutura_fonte_energia.objects.filter(infraestrutura= infraestrutura)
        for fonte in fontes:
            fonte_energia.append(fonte.tipo)

        rede_esgoto = []
        redes = Infraestrutura_rede_esgoto.objects.filter(infraestrutura= infraestrutura)
        for rede in redes:
            rede_esgoto.append(rede.tipo)

        destinacao_lixo = []
        destinos = Infraestrutura_destinacao_lixo.objects.filter(infraestrutura= infraestrutura)
        for destino in destinos:
            destinacao_lixo.append(destino.tipo)

        tratamento_lixo = []
        tratamentos = Infraestrutura_tratamento_lixo.objects.filter(infraestrutura= infraestrutura)
        for tratamento in tratamentos:
            tratamento_lixo.append(tratamento.tipo)

        recurso_acessibilidade = []
        recursos = Infraestrutura_recurso_acessibilidade.objects.filter(infraestrutura= infraestrutura)
        for recurso in recursos:
            recurso_acessibilidade.append(recurso.tipo)

    if request.method == 'POST':
        formulario_infraestrutura(request, edicao)
        if edicao:
            return HttpResponseRedirect(f'/administracao/infraestrutura-perfil/{endereco.id}')

        if endereco.tipo == 'S':
            return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={escola.cod_inep}')
        else:
            return HttpResponseRedirect(f'/administracao/unidade_perfil?inep={escola.cod_inep}&id_endereco={endereco.id}')

    return TemplateResponse(request, template_name, locals())

# VIEW DO FORMULÁRIO DE DEPENDENCIA FÍSICA
def dependencia_formulario(request, id_endereco):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5], True):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/infraestrutura/dependencia-formulario.html'
    user = request.session['username']

    # VERIFICANDO SE O ENDEREÇO INFORMADO EXISTE
    try:
        endereco = Endereco.objects.get(id= id_endereco)
        escola = endereco.escola
    except:
        return HttpResponseRedirect('/administracao')

    # LISTANDO OS TIPOS DE DEPENDÊNCIA DISPONÍVEIS PARA CADASTRO
    tipos_dependencia = Infraestrutura_dependencia_tipo.objects.all()

    # SEPARANDO AS CATEGORIAS DE TIPOS DE DEPENDÊNCIA PARA AGRUPAR NA SELEÇÃO
    categorias_tipo = tipos_dependencia.values('categoria').distinct()

    if request.method == 'POST':
        formulario_dependencia(request, endereco, False)

        return HttpResponseRedirect(f'/administracao/infraestrutura-perfil/{endereco.id}')

    return TemplateResponse(request, template_name, locals())


# def dependencia_perfil(request):
#     if verificar_manutencao():
#         return HttpResponseRedirect('/')

#     if not verificacao_maxima(request, [1, 5]):
#         return HttpResponseRedirect('/')

#     template_name = 'administracao/unidades/infraestrutura/infraestrutura-perfil.html'
#     user = request.session['username']

#     permissao = Permissao.objects.get(usuario__login= user, servico__id__in= [1, 5])

#     id_infraestrutura = request.GET.get('id')
#     infraestrutura = Infraestrutura_geral.objects.get(id= id_infraestrutura)

#     endereco = infraestrutura.endereco
#     escola = endereco.escola

#     quantidade_dependencias = 0
#     quantidade_salas_de_aula = 0

#     dependencias = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura).exclude(tipo__tipo= 'Sala de Aula')
#     quantidade_dependencias = dependencias.count()

#     salas_de_aula = Infraestrutura_dependencia.objects.filter(infraestrutura= infraestrutura, tipo__tipo= 'Sala de Aula')
#     quantidade_salas_de_aula = salas_de_aula.count()

#     locais = Infraestrutura_local_funcionamento.objects.filter(infraestrutura= infraestrutura).order_by('local')
#     abastecimentos = Infraestrutura_abastecimento_agua.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
#     esgotos = Infraestrutura_rede_esgoto.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
#     energias = Infraestrutura_fonte_energia.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
#     destinacoes = Infraestrutura_destinacao_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
#     tratamentos = Infraestrutura_tratamento_lixo.objects.filter(infraestrutura= infraestrutura).order_by('tipo')
#     recursos = Infraestrutura_recurso_acessibilidade.objects.filter(infraestrutura= infraestrutura).order_by('tipo')

    # return TemplateResponse(request, template_name, locals())