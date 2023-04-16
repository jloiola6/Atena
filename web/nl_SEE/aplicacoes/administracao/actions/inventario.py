from aplicacoes.administracao.models import *
from aplicacoes.atena.models import *
from aplicacoes.core.actions import dict_compare, salvar_historico

def formulario_controle_inventario(request):
    print(request.POST, 'categoria-tipo' in request.POST)

    nome_categoria = request.POST.get('categoria-tipo')

    if nome_categoria:
        if not Inventario_item_categoria.objects.filter(nome= nome_categoria).exists():
            nova_categoria = Inventario_item_categoria()
            nova_categoria.nome = nome_categoria
            nova_categoria.save()

            salvar_historico(request, nova_categoria, False, 'administracao_inventario_item_categoria')
    else:
        id_categoria_tipo = request.POST.get('categoria')
        categoria_tipo = Inventario_item_categoria.objects.get(id= id_categoria_tipo)

        nome_tipo = request.POST.get('tipo-nome')

        if not Inventario_item_tipo.objects.filter(nome= nome_tipo, categoria= categoria_tipo).exists():
            novo_tipo = Inventario_item_tipo()
            novo_tipo.categoria = categoria_tipo
            novo_tipo.nome = nome_tipo
            novo_tipo.save()

            salvar_historico(request, novo_tipo, False, 'administracao_inventario_item_tipo')


def formulario_inventario(request, edicao):
    def pegar_dados(inicio, fim):
        lista = []
        for item in range(inicio, fim+1):
            if request.POST.get(f'fieldset-local-{item}') != None:
                lista.append(request.POST.get(f'fieldset-local-{item}'))

        return lista

    def salvar_detalhes(equipamento, inventario, edicao):
        modificacoes = None
        if equipamento == 1:
            detalhes_computador = pegar_dados(1, 7)
            tabela = 'aux_computador'

            if edicao:
                banco = Computador.objects.filter(inventario_eletronico= inventario)
                inputs_inventario = {'processador': detalhes_computador[0], 'ram': detalhes_computador[1], 'disco': detalhes_computador[2], 'ssd': detalhes_computador[3], 'placa_video': detalhes_computador[4], 'cor': detalhes_computador[5], 'tipo':detalhes_computador[6]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Computador()

            banco.inventario_eletronico = inventario
            banco.processador = detalhes_computador[0]
            banco.ram = detalhes_computador[1]
            banco.disco = detalhes_computador[2]
            banco.ssd = detalhes_computador[3]
            banco.placa_video = detalhes_computador[4]
            banco.cor = detalhes_computador[5]
            banco.tipo = detalhes_computador[6]

        elif equipamento == 2:
            detalhes_nobreak = pegar_dados(8, 9)
            tabela = 'aux_nobreak'

            if edicao:
                banco = Nobreak.objects.filter(inventario_eletronico= inventario)
                inputs_inventario = {'qtd_tomadas': detalhes_nobreak[0], 'estabilizador': detalhes_nobreak[1]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Nobreak()

            banco.inventario_eletronico = inventario
            banco.qtd_tomadas = detalhes_nobreak[0]
            banco.estabilizador = detalhes_nobreak[1]

        elif equipamento == 3:
            detalhes_projetor = pegar_dados(10, 12)
            tabela = 'aux_projetor'

            if edicao:
                banco = Projetor.objects.filter(inventario_eletronico= inventario)
                inputs_inventario = {'resolucao': detalhes_projetor[0], 'potencia': detalhes_projetor[1], 'lumens': detalhes_projetor[2]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Projetor()

            banco.inventario_eletronico = inventario
            banco.resolucao = detalhes_projetor[0]
            banco.potencia = detalhes_projetor[1]
            banco.lumens = detalhes_projetor[2]

        elif equipamento == 4:
            detalhes_impressora = pegar_dados(13, 14)
            tabela = 'aux_impressora'

            if edicao:
                banco = Impressora.objects.filter(inventario_eletronico= inventario)
                inputs_inventario = {'tipo_impressao': detalhes_impressora[0], 'conectividade': detalhes_impressora[1]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Impressora()

            banco.inventario_eletronico = inventario
            banco.tipo_impressao = detalhes_impressora[0]
            banco.conectividade = detalhes_impressora[1]

        elif equipamento == 5:
            detalhes_switch = pegar_dados(16, 19)
            tabela = 'aux_switch'

            if edicao:
                banco = Switch.objects.filter(inventario_eletronico= inventario)
                inputs_inventario = {'qtd_RJ45': detalhes_switch[0], 'qtd_SFP': detalhes_switch[1], 'fonte_integrada': detalhes_switch[2], 'potencia': detalhes_switch[3]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Switch()

            banco.inventario_eletronico = inventario
            banco.qtd_RJ45 = detalhes_switch[0]
            banco.qtd_SFP = detalhes_switch[1]
            banco.fonte_integrada = detalhes_switch[2]
            banco.potencia = detalhes_switch[3]

        elif equipamento in (6, 8):
            detalhes_geladeira_freezer = pegar_dados(20, 22)

            if equipamento == 6:
                tabela = 'aux_geladeira'
                if edicao:
                    banco = Geladeira.objects.filter(inventario_eletrodomestico= inventario)
                    inputs_inventario = {'cor': detalhes_geladeira_freezer[0], 'capacidade': detalhes_geladeira_freezer[1], 'voltagem': detalhes_geladeira_freezer[2]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Geladeira()
            else:
                tabela = 'aux_freezer'
                if edicao:
                    banco = Freezer.objects.filter(inventario_eletrodomestico= inventario)
                    inputs_inventario = {'cor': detalhes_geladeira_freezer[0], 'capacidade': detalhes_geladeira_freezer[1], 'voltagem': detalhes_geladeira_freezer[2]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Freezer()

            banco.inventario_eletrodomestico = inventario
            banco.cor = detalhes_geladeira_freezer[0]
            banco.capacidade = detalhes_geladeira_freezer[1]
            banco.voltagem = detalhes_geladeira_freezer[2]

        elif equipamento == 7:
            detalhes_ac = pegar_dados(23, 25)
            tabela = 'aux_A/C'

            if edicao:
                banco = Ar_condicionado.objects.filter(inventario_eletrodomestico= inventario)
                inputs_inventario = {'qtd_RJ45': detalhes_ac[0], 'qtd_SFP': detalhes_ac[1], 'fonte_integrada': detalhes_ac[2], 'potencia': detalhes_ac[3]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Ar_condicionado()

            banco.inventario_eletrodomestico = inventario
            banco.capacidade = detalhes_ac[0]
            banco.cor = detalhes_ac[1]
            banco.voltagem = detalhes_ac[2]

        elif equipamento == 9:
            detalhes_liquidificador = pegar_dados(26, 29)
            tabela = 'aux_liquidificador'

            if edicao:
                banco = Liquidificador.objects.filter(inventario_eletrodomestico= inventario)
                inputs_inventario = {'capacidade': detalhes_liquidificador[0], 'potencia': detalhes_liquidificador[1], 'cor': detalhes_liquidificador[2], 'voltagem': detalhes_liquidificador[3]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Liquidificador()

            banco.inventario_eletrodomestico = inventario
            banco.capacidade = detalhes_liquidificador[0]
            banco.potencia = detalhes_liquidificador[1]
            banco.cor = detalhes_liquidificador[2]
            banco.voltagem = detalhes_liquidificador[3]

        elif equipamento == 10:
            detalhes_fogao = pegar_dados(30, 33)
            tabela = 'aux_fogao'

            if edicao:
                banco = Fogao.objects.filter(inventario_eletrodomestico= inventario)
                inputs_inventario = {'capacidade': detalhes_fogao[0], 'cor': detalhes_fogao[1], 'voltagem': detalhes_fogao[2], 'industrial': detalhes_fogao[3]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Fogao()

            banco.inventario_eletrodomestico = inventario
            banco.capacidade = detalhes_fogao[0]
            banco.cor = detalhes_fogao[1]
            banco.voltagem = detalhes_fogao[2]
            banco.industrial = detalhes_fogao[3]

        elif equipamento in (11, 12, 13, 14):
            if equipamento == 11:
                detalhes_mobilia = pegar_dados(37, 37)
            elif equipamento == 12:
                detalhes_mobilia = pegar_dados(39, 39)
            elif equipamento == 13:
                detalhes_mobilia = pegar_dados(36, 36)
            elif equipamento == 14:
                detalhes_mobilia = pegar_dados(38, 38)

            if equipamento == 11:
                tabela = 'aux_cadeira'
                if edicao:
                    banco = Cadeira.objects.filter(inventario_mobilia= inventario)
                    inputs_inventario = {'tipo': detalhes_mobilia[0]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Cadeira()

            elif equipamento == 12:
                tabela = 'aux_mesa'
                if edicao:
                    banco = Mesa.objects.filter(inventario_mobilia= inventario)
                    inputs_inventario = {'tipo': detalhes_mobilia[0]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Mesa()

            elif equipamento == 13:
                tabela = 'aux_armario'
                if edicao:
                    banco = Armario.objects.filter(inventario_mobilia= inventario)
                    inputs_inventario = {'tipo': detalhes_mobilia[0]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Armario()

            elif equipamento == 14:
                tabela = 'aux_estante'
                if edicao:
                    banco = Estante.objects.filter(inventario_mobilia= inventario)
                    inputs_inventario = {'tipo': detalhes_mobilia[0]}
                    modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                    banco = banco[0]
                else:
                    banco = Estante()

            banco.inventario_mobilia = inventario
            banco.tipo = detalhes_mobilia[0]

        elif equipamento == 15:
            tabela = 'aux_quadro'
            detalhes_quadro = pegar_dados(34, 35)

            if edicao:
                banco = Quadro.objects.filter(inventario_mobilia= inventario)
                inputs_inventario = {'tipo': detalhes_quadro[0], 'tamanho': detalhes_quadro[1]}
                modificacoes = dict_compare(banco.values()[0], inputs_inventario)
                banco = banco[0]
            else:
                banco = Quadro()

            banco.inventario_mobilia = inventario
            banco.tipo = detalhes_quadro[0]
            banco.tamanho = detalhes_quadro[1]

        banco.save()
        salvar_historico(request, banco, edicao, tabela, modificacoes)

    #Dados do Item
    dependencia = int(request.POST.get('dependencia'))
    tipo = request.POST.get('tipo-item')
    equipamento = int(request.POST.get('equipamento'))
    patrimonio = request.POST.get('patrimonio')
    marca = request.POST.get('marca')
    modelo = request.POST.get('modelo')
    descricao = request.POST.get('descricao')
    quantidade = request.POST.get('quantidade')
    insumo = False
    modificacoes = None

    if equipamento in (1, 2, 3, 4, 5):
        if edicao:
            id_item = request.GET.get('id_item')
            inventario = Inventario_Eletronico.objects.filter(id= id_item)
            inputs_inventario = {'patrimonio': patrimonio, 'marca': marca, 'modelo': modelo}
            modificacoes = dict_compare(inventario.values()[0], inputs_inventario)
            inventario = inventario[0]
        else:
            inventario = Inventario_Eletronico()

        tabela = 'administracao_inventario_eletronico'

    elif equipamento in (6, 7, 8, 9, 10):
        if edicao:
            id_item = request.GET.get('id_item')
            inventario = Inventario_Eletrodomestico.objects.filter(id= id_item)
            inputs_inventario = {'patrimonio': patrimonio, 'marca': marca, 'modelo': modelo}
            modificacoes = dict_compare(inventario.values()[0], inputs_inventario)
            inventario = inventario[0]
        else:
            inventario = Inventario_Eletrodomestico()

        tabela = 'administracao_inventario_eletrodomestico'

    elif equipamento in (11, 12, 13, 14, 15):
        if edicao:
            id_item = request.GET.get('id_item')
            inventario = Inventario_Mobilia.objects.filter(id= id_item)
            inputs_inventario = {'patrimonio': patrimonio, 'marca': marca, 'modelo': modelo}
            modificacoes = dict_compare(inventario.values()[0], inputs_inventario)
            inventario = inventario[0]
        else:
            inventario = Inventario_Mobilia()

        tabela = 'administracao_inventario_mobilia'

    elif equipamento in (16, 17):
        if edicao:
            id_item = request.GET.get('id_item')
            inventario = Inventario_Insumo.objects.filter(id= id_item)
            inputs_inventario = {'descricao': descricao, 'quantidade': quantidade}
            modificacoes = dict_compare(inventario.values()[0], inputs_inventario)
            inventario = inventario[0]
        else:
            inventario = Inventario_Insumo()

        tabela = 'administracao_inventario_insumo'
        insumo = True

    inventario.equipamento = Equipamento.objects.get(id= equipamento)
    inventario.dependencia = Infraestrutura_tipo_dependencia.objects.get(id= dependencia)

    if insumo:
        inventario.descricao = descricao
        inventario.quantidade = quantidade
    else:
        inventario.patrimonio = patrimonio
        inventario.marca = marca
        inventario.modelo = modelo

    inventario.save()
    salvar_historico(request, inventario, edicao, tabela, modificacoes)

    if not insumo:
        salvar_detalhes(equipamento, inventario, edicao)


def formulario_item(request, tipo, dependencia):
    print(request.POST)

    novo_item = Inventario_item()
    novo_item.dependencia = dependencia
    novo_item.tipo = tipo

    if request.POST.get('patrimonio'):
        novo_item.patrimonio = request.POST.get('patrimonio')

    novo_item.save()

    if request.POST.get('cor'):
        cor = Inventario_item_detalhes()
        cor.campo = 'Cor'
        cor.valor = request.POST.get('cor')
        cor.item = novo_item

        cor.save()

    if request.POST.get('capacidade'):
        capacidade = Inventario_item_detalhes()
        capacidade.campo = 'Capacidade'
        capacidade.valor = request.POST.get('capacidade')
        capacidade.item = novo_item

        capacidade.save()

    if request.POST.get('voltagem'):
        voltagem = Inventario_item_detalhes()
        voltagem.campo = 'Voltagem'
        voltagem.valor = request.POST.get('voltagem')
        voltagem.item = novo_item

        voltagem.save()

    if request.POST.get('industrial'):
        industrial = Inventario_item_detalhes()
        industrial.campo = 'Industrial'
        industrial.valor = request.POST.get('industrial')
        industrial.item = novo_item

        industrial.save()

    if request.POST.get('watts'):
        watts = Inventario_item_detalhes()
        watts.campo = 'Potência (watts)'
        watts.valor = request.POST.get('watts')
        watts.item = novo_item

        watts.save()

    if request.POST.get('processador'):
        processador = Inventario_item_detalhes()
        processador.campo = 'Processador'
        processador.valor = request.POST.get('processador')
        processador.item = novo_item

        processador.save()

    if request.POST.get('ram'):
        ram = Inventario_item_detalhes()
        ram.campo = 'RAM (GB)'
        ram.valor = request.POST.get('ram')
        ram.item = novo_item

        ram.save()

    if request.POST.get('disco'):
        disco = Inventario_item_detalhes()
        disco.campo = 'Memória em disco (GB)'
        disco.valor = request.POST.get('disco')
        disco.item = novo_item

        disco.save()

    if request.POST.get('ssd'):
        ssd = Inventario_item_detalhes()
        ssd.campo = 'Memória em SSD (GB)'
        ssd.valor = request.POST.get('ssd')
        ssd.item = novo_item

        ssd.save()

    if request.POST.get('video'):
        video = Inventario_item_detalhes()
        video.campo = 'Placa de vídeo'
        video.valor = request.POST.get('video')
        video.item = novo_item

        video.save()

    if request.POST.get('tipo-computador'):
        tipo_computador = Inventario_item_detalhes()
        tipo_computador.campo = 'Tipo'
        tipo_computador.valor = request.POST.get('tipo-computador')
        tipo_computador.item = novo_item

        tipo_computador.save()

    if request.POST.get('impressao'):
        impressao = Inventario_item_detalhes()
        impressao.campo = 'Tipo de impressão'
        impressao.valor = request.POST.get('impressao')
        impressao.item = novo_item

        impressao.save()

    if request.POST.get('conectividade'):
        valores = request.POST.getlist('conectividade')

        for valor in valores:
            conectividade = Inventario_item_detalhes()
            conectividade.campo = 'Conectividade'
            conectividade.valor = valor
            conectividade.item = novo_item

            conectividade.save()

    if request.POST.get('tomadas'):
        tomadas = Inventario_item_detalhes()
        tomadas.campo = 'Quantidade de tomadas'
        tomadas.valor = request.POST.get('tomadas')
        tomadas.item = novo_item

        tomadas.save()

    if request.POST.get('estabilizador'):
        estabilizador = Inventario_item_detalhes()
        estabilizador.campo = 'Estabilizador'
        estabilizador.valor = request.POST.get('estabilizador')
        estabilizador.item = novo_item

        estabilizador.save()

    if request.POST.get('resolucao'):
        resolucao = Inventario_item_detalhes()
        resolucao.campo = 'Resolução'
        resolucao.valor = request.POST.get('resolucao')
        resolucao.item = novo_item

        resolucao.save()

    if request.POST.get('lumens'):
        lumens = Inventario_item_detalhes()
        lumens.campo = 'Potência (lumens)'
        lumens.valor = request.POST.get('lumens')
        lumens.item = novo_item

        lumens.save()

    if request.POST.get('rj45'):
        rj45 = Inventario_item_detalhes()
        rj45.campo = 'Quantidade de portas RJ-45'
        rj45.valor = request.POST.get('rj45')
        rj45.item = novo_item

        rj45.save()

    if request.POST.get('sfp'):
        sfp = Inventario_item_detalhes()
        sfp.campo = 'Quantidade de portas SFP'
        sfp.valor = request.POST.get('sfp')
        sfp.item = novo_item

        sfp.save()

    if request.POST.get('fonte'):
        fonte = Inventario_item_detalhes()
        fonte.campo = 'Fonte integrada'
        fonte.valor = request.POST.get('fonte')
        fonte.item = novo_item

        fonte.save()

    if request.POST.get('tipo-estante'):
        tipo_estante = Inventario_item_detalhes()
        tipo_estante.campo = 'Tipo'
        tipo_estante.valor = request.POST.get('tipo-estante')
        tipo_estante.item = novo_item

        tipo_estante.save()

    if request.POST.get('tipo-armario'):
        tipo_armario = Inventario_item_detalhes()
        tipo_armario.campo = 'Tipo'
        tipo_armario.valor = request.POST.get('tipo-armario')
        tipo_armario.item = novo_item

        tipo_armario.save()

    if request.POST.get('tipo-mesa'):
        tipo_mesa = Inventario_item_detalhes()
        tipo_mesa.campo = 'Tipo'
        tipo_mesa.valor = request.POST.get('tipo-mesa')
        tipo_mesa.item = novo_item

        tipo_mesa.save()

    if request.POST.get('tipo-quadro'):
        tipo_quadro = Inventario_item_detalhes()
        tipo_quadro.campo = 'Tipo'
        tipo_quadro.valor = request.POST.get('tipo-quadro')
        tipo_quadro.item = novo_item

        tipo_quadro.save()

    if request.POST.get('tamanho'):
        tamanho = Inventario_item_detalhes()
        tamanho.campo = 'Tamanho'
        tamanho.valor = request.POST.get('tamanho')
        tamanho.item = novo_item

        tamanho.save()