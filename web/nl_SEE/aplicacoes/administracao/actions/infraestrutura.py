from aplicacoes.administracao.models import *
from aplicacoes.core.actions import dict_compare, salvar_historico

def formulario_infraestrutura(request, edicao):
    def pegar_checkbox(inicio, fim):
        lista = []
        for item in range(inicio, fim+1):
            if request.POST.get(f'fieldset-local-{item}') != None:
                lista.append(request.POST.get(f'fieldset-local-{item}'))

        return lista


    def salva_dados(lista):
        tabela = lista[1]
        edicao = lista[2]
        infraestrutura = lista[3]
        lista = lista[0]
        local = False

        infraestrutura = Infraestrutura_geral.objects.get(id= infraestrutura)

        for item in lista:
            if tabela == 'administracao_infraestrutura_local_funcionamento':
                banco = Infraestrutura_local_funcionamento()
                local = True
            elif tabela == 'administracao_infraestrutura_abastecimento_agua':
                banco = Infraestrutura_abastecimento_agua()
            elif tabela == 'administracao_infraestrutura_fonte_energia':
                banco = Infraestrutura_fonte_energia()
            elif tabela == 'administracao_infraestrutura_rede_esgoto':
                banco = Infraestrutura_rede_esgoto()
            elif tabela == 'administracao_infraestrutura_destinacao_lixo':
                banco = Infraestrutura_destinacao_lixo()
            elif tabela == 'administracao_infraestrutura_tratamento_lixo':
                banco = Infraestrutura_tratamento_lixo()
            elif tabela == 'administracao_infraestrutura_recurso_acessibilidade':
                banco = Infraestrutura_recurso_acessibilidade()

            banco.infraestrutura = infraestrutura
            if local:
                banco.local = item
            else:
                banco.tipo = item

            banco.save()
            salvar_historico(request, banco, edicao, tabela)


    #Dados do Item
    endereco = Endereco.objects.get(id= request.GET.get('id_endereco'))
    agua_potavel = request.POST.get('fieldset-agua-potavel')

    local_funcionamento = pegar_checkbox(1, 6)
    abastecimento_agua = pegar_checkbox(7, 11)
    fonte_energia = pegar_checkbox(12, 15)
    esgotamento_sanitario = pegar_checkbox(16, 19)
    destinacao_lixo = pegar_checkbox(20, 24)
    tratamento_lixo = pegar_checkbox(25, 28)
    acessibilidade = pegar_checkbox(29, 37)


    #Salvando no banco dados da infraestrutura Geral
    if edicao:
        infraestrutura = Infraestrutura_geral.objects.filter(endereco= endereco)
        inputs = {'agua_potavel': agua_potavel}
        modificacoes = dict_compare(infraestrutura.values()[0], inputs)

        infraestrutura = infraestrutura[0]
    else:
        infraestrutura = Infraestrutura_geral()
        modificacoes = None

    infraestrutura.agua_potavel = agua_potavel
    infraestrutura.save()
    salvar_historico(request, infraestrutura, edicao, 'administracao_infraestrutura_geral', modificacoes)

    endereco.infraestrutura = infraestrutura
    endereco.save()
    salvar_historico(request, endereco, False, 'administracao_endereco')


    Infraestrutura_local_funcionamento.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_abastecimento_agua.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_fonte_energia.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_rede_esgoto.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_destinacao_lixo.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_tratamento_lixo.objects.filter(infraestrutura= infraestrutura).delete()
    Infraestrutura_recurso_acessibilidade.objects.filter(infraestrutura= infraestrutura).delete()

    id_infraestrutura = infraestrutura.id
    dados = [(local_funcionamento, 'administracao_infraestrutura_local_funcionamento', edicao, id_infraestrutura),
        (abastecimento_agua, 'administracao_infraestrutura_abastecimento_agua', edicao, id_infraestrutura),
        (fonte_energia, 'administracao_infraestrutura_fonte_energia', edicao, id_infraestrutura),
        (esgotamento_sanitario, 'administracao_infraestrutura_rede_esgoto', edicao, id_infraestrutura),
        (destinacao_lixo, 'administracao_infraestrutura_destinacao_lixo', edicao, id_infraestrutura),
        (tratamento_lixo, 'administracao_infraestrutura_tratamento_lixo', edicao, id_infraestrutura),
        (acessibilidade, 'administracao_infraestrutura_recurso_acessibilidade', edicao, id_infraestrutura)]
    list(map(salva_dados,dados))


def formulario_dependencia(request, endereco, edicao):
    infraestrutura = endereco.infraestrutura

    # VERIFICANDO SE O ENDEREÇO PASSADO POSSUI INFRAESTRUTURA CADASTRADA
    if not infraestrutura:
        # CASO NÃO TENHA, A INFRAESTRUTURA É CRIADA E ASSOCIADA AO ENDEREÇO
        infraestrutura = Infraestrutura_geral()
        infraestrutura.save()
        salvar_historico(request, infraestrutura, False, 'administracao_infraestrutura_geral')

        endereco.infraestrutura = infraestrutura
        endereco.save()
        salvar_historico(request, endereco, False, 'administracao_endereco')

    tipo = request.POST.get('tipo')
    descricao = request.POST.get('descricao')
    capacidade = request.POST.get('capacidade')
    status = request.POST.get('status')

    dependencia = Infraestrutura_dependencia()
    dependencia.tipo_dependencia = Infraestrutura_dependencia_tipo.objects.get(id= tipo)
    dependencia.descricao = descricao
    dependencia.capacidade_pessoas = capacidade
    dependencia.status = status
    dependencia.infraestrutura = infraestrutura
    dependencia.save()
    salvar_historico(request, dependencia, False, 'administracao_infraestrutura_dependencia')