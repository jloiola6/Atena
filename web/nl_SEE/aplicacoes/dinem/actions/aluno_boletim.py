from aplicacoes.dinem.models import *
from aplicacoes.core.views import salvar_historico, dict_compare
from aplicacoes.dinem.action import formulario_relatorio_aluno

def situacao_aluno(request, aluno, etapa):
    portugues = '-'
    artes = '-'
    ingles = '-'
    ed_fisica = '-'
    matematica = '-'
    fisica = '-'
    quimica = '-'
    biologia = '-'
    historia = '-'
    geografia = '-'
    filosofia = '-'
    sociologia = '-'
    eletiva = '-'
    espanhol = '-'
    estudo_orientado = '-'
    praticas_experimentais = '-'
    projeto_vida = '-'
    oficina_linguagens = '-'
    oficina_matematica = '-'
    oficina_natureza = '-'
    oficina_humanas = '-'
    pos_medio = '-'
    ciencias_natureza = '-'
    ciencias_humanas = '-'
    matematica_tecnologias = '-'
    linguagens_tecnologias = '-'
    formacao_tecnica = '-'
    lt_ch = '-'
    mt_cn = '-'
    investigacao = '-'
    criativos = '-'
    sociocultural = '-'
    empreendedorismo = '-'
    area_conhecimento = '-'
    protagonismo = '-'

    if request.POST.get('aluno-fieldset-situacao') == 'transferido':
        resultado = 'TRANSFERIDO'
    else:
        resultado = 'DESISTENTE'

    aluno_situacao = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)
    aluno_situacao.portugues = portugues
    aluno_situacao.arte = artes
    aluno_situacao.ingles = ingles
    aluno_situacao.ed_fisica = ed_fisica
    aluno_situacao.matematica = matematica
    aluno_situacao.fisica = fisica
    aluno_situacao.quimica = quimica
    aluno_situacao.biologia = biologia
    aluno_situacao.historia = historia
    aluno_situacao.geografia = geografia
    aluno_situacao.filosofia = filosofia
    aluno_situacao.sociologia = sociologia
    aluno_situacao.eletiva = eletiva
    aluno_situacao.espanhol = espanhol
    aluno_situacao.estudo_orientado = estudo_orientado
    aluno_situacao.praticas_experimentais = praticas_experimentais
    aluno_situacao.protagonismo = protagonismo
    aluno_situacao.projeto_vida = projeto_vida
    aluno_situacao.oficina_linguagens = oficina_linguagens
    aluno_situacao.oficina_matematica = oficina_matematica
    aluno_situacao.oficina_natureza = oficina_natureza
    aluno_situacao.oficina_humanas = oficina_humanas
    aluno_situacao.pos_medio = pos_medio
    aluno_situacao.ciencias_natureza = ciencias_natureza
    aluno_situacao.ciencias_humanas = ciencias_humanas
    aluno_situacao.matematica_tecnologias = matematica_tecnologias
    aluno_situacao.linguagens_tecnologias = linguagens_tecnologias
    aluno_situacao.formacao_tecnica = formacao_tecnica
    aluno_situacao.lt_ch = lt_ch
    aluno_situacao.mt_cn = mt_cn
    aluno_situacao.investigacao = investigacao
    aluno_situacao.criativos = criativos
    aluno_situacao.sociocultural = sociocultural
    aluno_situacao.empreendedorismo = empreendedorismo
    aluno_situacao.area_conhecimento = area_conhecimento
    aluno_situacao.resultado = resultado
    aluno_situacao.save()

def itinerario_formativo_integral(request, aluno, turma, etapa, edicao):
    eletiva = request.POST.get('eletiva')
    estudo_orientado = request.POST.get('estudo_orientado')
    praticas_experimentais = request.POST.get('praticas_experimentais')
    protagonismo = request.POST.get('protagonismo')
    pos_medio = request.POST.get('pos_medio')
    projeto_vida = request.POST.get('projeto_vida')
    espanhol = request.POST.get('espanhol')
    oficina_linguagens = request.POST.get('oficina_linguagens')
    oficina_matematica = request.POST.get('oficina_matematica')
    oficina_natureza = request.POST.get('oficina_natureza')
    oficina_humanas = request.POST.get('oficina_humanas')
    fildset_rota = request.POST.get('aluno-fieldset-rota-integral')
    if fildset_rota == 'propedeutica':
        area_natureza = request.POST.get('area_natureza')
        area_humanas = request.POST.get('area_humanas')
        area_matematica = request.POST.get('area_matematica')
        area_linguagens = request.POST.get('area_linguagem')
        ciencias_natureza = request.POST.get('media_natureza')
        ciencias_humanas = request.POST.get('media_humanas')
        matematica_tecnologias = request.POST.get('media_matematica')
        linguagens_tecnologias = request.POST.get('media_linguagens')
    else:
        formacao_tecnica = request.POST.get('formacao_tecnica')
    resultado = request.POST.get('resultado')

    if edicao:
        itinerario_integral = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa)
        if fildset_rota == 'propedeutica':
            lista_aux = []
            if area_natureza != None:
                lista_aux.append(ciencias_natureza)
            else:
                lista_aux.append('-')

            if area_humanas != None:
                lista_aux.append(ciencias_humanas)
            else:
                lista_aux.append('-')

            if area_matematica != None:
                lista_aux.append(matematica_tecnologias)
            else:
                lista_aux.append('-')

            if area_linguagens != None:
                lista_aux.append(linguagens_tecnologias)
            else:
                lista_aux.append('-')

            inputs_relatorio = {'id': itinerario_integral[0].id, 'eletiva': eletiva, 'estudo_orientado': estudo_orientado, 'praticas_experimentais': praticas_experimentais, 'protagonismo': protagonismo, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'oficina_linguagens': oficina_linguagens, 'oficina_matematica': oficina_matematica, 'oficina_humanas': oficina_humanas, 'oficina_humanas': oficina_natureza, 'ciencias_natureza': lista_aux[0], 'ciencias_humanas': lista_aux[1], 'matematica_tecnologias': lista_aux[2], 'linguagens_tecnologias': lista_aux[3],  'formacao_tecnica': '-', 'resultado': resultado}
        else:
            inputs_relatorio = {'id': itinerario_integral[0].id, 'eletiva': eletiva, 'estudo_orientado': estudo_orientado, 'praticas_experimentais': praticas_experimentais, 'protagonismo': protagonismo, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'oficina_linguagens': oficina_linguagens, 'oficina_matematica': oficina_matematica, 'oficina_humanas': oficina_humanas, 'oficina_humanas': oficina_natureza, 'ciencias_natureza': '-', 'ciencias_humanas': '-', 'matematica_tecnologias': '-', 'linguagens_tecnologias': '-',  'formacao_tecnica': formacao_tecnica, 'resultado': resultado}

        modificacoes_relatorioFinal = dict_compare(itinerario_integral.values()[0], inputs_relatorio)
        itinerario_integral = itinerario_integral[0]
    else:
        modificacoes_relatorioFinal = None
        itinerario_integral = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)

    if etapa == '1ª Série':
        if turma.etapa.id == 6 and turma.ano_serie == '1ª Série' and turma.ano_letivo == '2022':
            itinerario_integral.protagonismo = protagonismo
        else:
            itinerario_integral.protagonismo = '-'

        itinerario_integral.eletiva = eletiva
        itinerario_integral.oficina_linguagens = oficina_linguagens
        itinerario_integral.oficina_matematica = oficina_matematica
        itinerario_integral.oficina_natureza = oficina_natureza
        itinerario_integral.oficina_humanas = oficina_humanas
    else:
        itinerario_integral.protagonismo = '-'
        itinerario_integral.eletiva = '-'
        itinerario_integral.oficina_linguagens = '-'
        itinerario_integral.oficina_matematica = '-'
        itinerario_integral.oficina_natureza = '-'
        itinerario_integral.oficina_humanas = '-'

    itinerario_integral.estudo_orientado = estudo_orientado
    itinerario_integral.praticas_experimentais = praticas_experimentais

    if etapa == '1ª Série' or etapa == '2ª Série':
        itinerario_integral.projeto_vida = projeto_vida
    else:
        itinerario_integral.projeto_vida = '-'

    if etapa == '3ª Série':
        itinerario_integral.pos_medio = pos_medio
    else:
        itinerario_integral.pos_medio = '-'

    if etapa == '2ª Série':
        itinerario_integral.espanhol = espanhol
    else:
        itinerario_integral.espanhol = '-'

    if etapa == '2ª Série' or etapa == '3ª Série':
        if fildset_rota == 'propedeutica':
            if ciencias_natureza != '':
                if edicao:
                    itinerario_integral.ciencias_natureza = lista_aux[0]
                else:
                    itinerario_integral.ciencias_natureza = ciencias_natureza
            else:
                itinerario_integral.ciencias_natureza = '-'

            if ciencias_humanas != '':
                if edicao:
                    itinerario_integral.ciencias_humanas = lista_aux[1]
                else:
                    itinerario_integral.ciencias_humanas = ciencias_humanas
            else:
                itinerario_integral.ciencias_humanas = '-'

            if matematica_tecnologias != '':
                if edicao:
                    itinerario_integral.matematica_tecnologias = lista_aux[2]
                else:
                    itinerario_integral.matematica_tecnologias = matematica_tecnologias
            else:
                itinerario_integral.matematica_tecnologias = '-'

            if linguagens_tecnologias != '':
                if edicao:
                    itinerario_integral.linguagens_tecnologias = lista_aux[3]
                else:
                    itinerario_integral.linguagens_tecnologias = linguagens_tecnologias
            else:
                itinerario_integral.linguagens_tecnologias = '-'

            itinerario_integral.formacao_tecnica = '-'
        else:
            itinerario_integral.formacao_tecnica = formacao_tecnica
            itinerario_integral.ciencias_natureza = '-'
            itinerario_integral.ciencias_humanas = '-'
            itinerario_integral.matematica_tecnologias = '-'
            itinerario_integral.linguagens_tecnologias = '-'
    else:
        if fildset_rota == 'propedeutica':
            if ciencias_natureza != '':
                itinerario_integral.ciencias_natureza = '-'
            if ciencias_humanas != '':
                itinerario_integral.ciencias_humanas = '-'
            if matematica_tecnologias != '':
                itinerario_integral.matematica_tecnologias = '-'
            if linguagens_tecnologias != '':
                itinerario_integral.linguagens_tecnologias = '-'
        else:
            itinerario_integral.formacao_tecnica = '-'

    itinerario_integral.resultado = resultado
    itinerario_integral.save()

def itinerario_formativo_parcial(request, aluno, etapa, edicao):
    espanhol = request.POST.get('espanhol')
    eletiva = request.POST.get('eletiva')
    projeto_vida = request.POST.get('projeto_vida')
    pos_medio = request.POST.get('pos_medio')
    fildset_rota = request.POST.get('aluno-fieldset-rota-parcial')
    if fildset_rota == 'propedeutica':
        area_conhecimento = request.POST.get('area_conhecimento')
        media_rota = request.POST.get('media_rota')
    else:
        formacao_tecnica = request.POST.get('formacao_tecnica')
    resultado = request.POST.get('resultado')

    if edicao:
        itinerario_parcial = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa)
        if fildset_rota == 'propedeutica':
            if itinerario_parcial[0].ciencias_natureza != '-':
                inputs_relatorio = {'id': itinerario_parcial[0].id, 'eletiva': eletiva, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'ciencias_natureza': media_rota, 'ciencias_humanas': '-', 'matematica_tecnologias': '-', 'linguagens_tecnologias': '-', 'formacao_tecnica': '-', 'resultado': resultado}
            elif itinerario_parcial[0].ciencias_humanas != '-':
                inputs_relatorio = {'id': itinerario_parcial[0].id, 'eletiva': eletiva, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'ciencias_natureza': '-', 'ciencias_humanas': media_rota, 'matematica_tecnologias': '-', 'linguagens_tecnologias': '-', 'formacao_tecnica': '-', 'resultado': resultado}
            elif itinerario_parcial[0].matematica_tecnologias != '-':
                inputs_relatorio = {'id': itinerario_parcial[0].id, 'eletiva': eletiva, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'ciencias_natureza': '-', 'ciencias_humanas': '-', 'matematica_tecnologias': media_rota, 'linguagens_tecnologias': '-', 'formacao_tecnica': '-', 'resultado': resultado}
            elif itinerario_parcial[0].linguagens_tecnologias:
                inputs_relatorio = {'id': itinerario_parcial[0].id, 'eletiva': eletiva, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'ciencias_natureza': '-', 'ciencias_humanas': '-', 'matematica_tecnologias': '-', 'linguagens_tecnologias': media_rota, 'formacao_tecnica': '-', 'resultado': resultado}
        else:
            inputs_relatorio = {'id': itinerario_parcial[0].id, 'eletiva': eletiva, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'espanhol': espanhol, 'ciencias_natureza': '-', 'ciencias_humanas': '-', 'matematica_tecnologias': '-', 'linguagens_tecnologias': '-', 'formacao_tecnica': formacao_tecnica, 'resultado': resultado}

        modificacoes_relatorioFinal = dict_compare(itinerario_parcial.values()[0], inputs_relatorio)

        itinerario_parcial = itinerario_parcial[0]
    else:
        modificacoes_relatorioFinal = None
        itinerario_parcial = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)

    if etapa == '2ª Série':
        itinerario_parcial.espanhol = espanhol
    else:
        itinerario_parcial.espanhol = '-'

    if etapa == '1ª Série':
        itinerario_parcial.eletiva = eletiva
    else:
        itinerario_parcial.eletiva = '-'

    if etapa == '1ª Série' or etapa == '2ª Série':
        itinerario_parcial.projeto_vida = projeto_vida
    else:
        itinerario_parcial.projeto_vida = '-'

    if etapa == '3ª Série':
        itinerario_parcial.pos_medio = pos_medio
    else:
        itinerario_parcial.pos_medio = '-'

    if etapa == '2ª Série' or etapa == '3ª Série':
        if fildset_rota == 'propedeutica':
            if area_conhecimento == 'Linguagens e suas tecnologias':
                itinerario_parcial.linguagens_tecnologias = media_rota
                itinerario_parcial.matematica_tecnologias = '-'
                itinerario_parcial.ciencias_natureza = '-'
                itinerario_parcial.ciencias_humanas = '-'
            elif area_conhecimento == 'Matemática e suas tecnologias':
                itinerario_parcial.matematica_tecnologias = media_rota
                itinerario_parcial.linguagens_tecnologias = '-'
                itinerario_parcial.ciencias_natureza = '-'
                itinerario_parcial.ciencias_humanas = '-'
            elif area_conhecimento == 'Ciências da natureza e suas tecnologias':
                itinerario_parcial.ciencias_natureza = media_rota
                itinerario_parcial.matematica_tecnologias = '-'
                itinerario_parcial.linguagens_tecnologias = '-'
                itinerario_parcial.ciencias_humanas = '-'
            elif area_conhecimento == 'Ciências humanas e suas tecnologias':
                itinerario_parcial.ciencias_humanas = media_rota
                itinerario_parcial.linguagens_tecnologias = '-'
                itinerario_parcial.matematica_tecnologias = '-'
                itinerario_parcial.ciencias_natureza = '-'
            itinerario_parcial.formacao_tecnica = '-'
        else:
            itinerario_parcial.formacao_tecnica = formacao_tecnica
            itinerario_parcial.ciencias_humanas = '-'
            itinerario_parcial.linguagens_tecnologias = '-'
            itinerario_parcial.matematica_tecnologias = '-'
            itinerario_parcial.ciencias_natureza = '-'
    else:
        if fildset_rota == 'propedeutica':
            itinerario_parcial.linguagens_tecnologias = '-'
            itinerario_parcial.matematica_tecnologias = '-'
            itinerario_parcial.ciencias_natureza = '-'
            itinerario_parcial.ciencias_humanas = '-'
            itinerario_parcial.area_conhecimento = '-'
        else:
            itinerario_parcial.formacao_tecnica = '-'

    itinerario_parcial.resultado = resultado
    itinerario_parcial.save()

def itinerario_formativo_profissionalizante(request, aluno, etapa, edicao):
    eletiva = request.POST.get('eletiva')
    estudo_orientado = request.POST.get('estudo_orientado')
    praticas_experimentais = request.POST.get('praticas_experimentais')
    espanhol = request.POST.get('espanhol')
    projeto_vida = request.POST.get('projeto_vida')
    pos_medio = request.POST.get('pos_medio')
    formacao_tecnica = request.POST.get('formacao_tecnica')
    resultado = request.POST.get('resultado')

    if edicao:
        itinerario_profissionalizante = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa)
        inputs_relatorio = {'id': itinerario_profissionalizante[0].id, 'eletiva': eletiva, 'estudo_orientado': estudo_orientado, 'praticas_experimentais': praticas_experimentais, 'espanhol': espanhol, 'projeto_vida': projeto_vida, 'pos_medio': pos_medio, 'formacao_tecnica': formacao_tecnica, 'resultado': resultado}
        modificacoes_relatorioFinal = dict_compare(itinerario_profissionalizante.values()[0], inputs_relatorio)

        itinerario_profissionalizante = itinerario_profissionalizante[0]
    else:
        modificacoes_relatorioFinal = None
        itinerario_profissionalizante = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)

    if etapa == '1ª Série':
        itinerario_profissionalizante.eletiva = eletiva
    else:
        itinerario_profissionalizante.eletiva = '-'

    itinerario_profissionalizante.estudo_orientado = estudo_orientado
    itinerario_profissionalizante.praticas_experimentais = praticas_experimentais

    if etapa == '2ª Série':
        itinerario_profissionalizante.espanhol = espanhol
    else:
        itinerario_profissionalizante.espanhol = '-'

    if etapa == '1ª Série' or etapa == '2ª Série':
        itinerario_profissionalizante.projeto_vida = projeto_vida
    else:
        itinerario_profissionalizante.projeto_vida = '-'

    if etapa == '3ª Série':
        itinerario_profissionalizante.pos_medio = pos_medio
    else:
        itinerario_profissionalizante.pos_medio = '-'

    itinerario_profissionalizante.formacao_tecnica = formacao_tecnica
    itinerario_profissionalizante.resultado = resultado
    itinerario_profissionalizante.save()


def parte_diversificada(request, aluno, etapa, edicao):
    #Capturando dados
    if  etapa == '3ª Série':
        espanhol = '-'
        projeto_vida = request.POST.get('projeto_vida')
        lt_ch = '-'
        mt_cn = '-'
        if request.POST.get('aluno-fieldset-rota') == 'propedeutica':
            area_conhecimento = request.POST.get('aluno-fieldset-areas')
            investigacao = request.POST.get('investigacao')
            criativos = request.POST.get('criativos')
            sociocultural = request.POST.get('sociocultural')
            empreendedorismo = request.POST.get('empreendedorismo')
        else:
            area_conhecimento = '-'
            investigacao = '-'
            criativos = '-'
            sociocultural = '-'
            empreendedorismo = '-'

        resultado = request.POST.get('resultado')

    else:
        espanhol = request.POST.get('espanhol')
        projeto_vida = request.POST.get('projeto_vida')
        lt_ch = request.POST.get('lt_ch')
        mt_cn = request.POST.get('mt_cn')
        area_conhecimento = '-'
        investigacao = '-'
        criativos = '-'
        sociocultural = '-'
        empreendedorismo = '-'

        resultado = request.POST.get('resultado')

    if edicao:
        relatorio = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa)
        inputs_relatorio = {'id': relatorio[0].id, 'espanhol': espanhol, 'projeto_vida': projeto_vida,  'lt_ch': lt_ch,  'mt_cn': mt_cn,  'investigacao': investigacao,  'criativos': criativos,  'sociocultural': sociocultural,  'empreendedorismo': empreendedorismo, 'area_conhecimento': area_conhecimento, 'resultado': resultado}
        modificacoes_relatorioFinal = dict_compare(relatorio.values()[0], inputs_relatorio)

        relatorio = relatorio[0]

    else:
        relatorio = RelatorioFinal.objects.get(aluno= aluno, etapa= etapa)
        modificacoes_relatorioFinal = None
        relatorio.aluno = aluno
        relatorio.etapa = etapa

    #Salvando no banco dados do departamento
    relatorio.espanhol = espanhol
    relatorio.projeto_vida = projeto_vida
    relatorio.lt_ch = lt_ch
    relatorio.mt_cn = mt_cn
    relatorio.area_conhecimento = area_conhecimento
    relatorio.investigacao = investigacao
    relatorio.criativos = criativos
    relatorio.sociocultural = sociocultural
    relatorio.empreendedorismo = empreendedorismo
    relatorio.resultado = resultado
    relatorio.save()

    salvar_historico(request, relatorio, edicao, 'dinem_relatorioFinal', modificacoes_relatorioFinal)

def formulario_aluno_boletim(request, turma, aluno, etapa, edicao):
    portugues = request.POST.get('portugues')
    artes = request.POST.get('arte')
    ingles = request.POST.get('ingles')
    ed_fisica = request.POST.get('ed_fisica')
    matematica = request.POST.get('matematica')
    fisica = request.POST.get('fisica')
    quimica = request.POST.get('quimica')
    biologia = request.POST.get('biologia')
    historia = request.POST.get('historia')
    geografia = request.POST.get('geografia')
    filosofia = request.POST.get('filosofia')
    sociologia = request.POST.get('sociologia')

    if edicao:
        formacao_basica = RelatorioFinal.objects.filter(aluno= aluno, etapa= etapa)
        inputs_relatorio = {'id': formacao_basica[0].id, 'portugues': portugues, 'arte': artes, 'ingles': ingles, 'ed_fisica': ed_fisica, 'matematica': matematica, 'fisica': fisica, 'quimica': quimica,  'biologia': biologia,  'historia': historia,  'geografia': geografia,  'filosofia': filosofia,  'sociologia': sociologia, 'etapa': etapa}
        modificacoes_relatorioFinal = dict_compare(formacao_basica.values()[0], inputs_relatorio)

        formacao_basica = formacao_basica[0]
    else:
        modificacoes_relatorioFinal = None
        formacao_basica = RelatorioFinal()
        formacao_basica.aluno = aluno
        formacao_basica.turma = turma
        formacao_basica.etapa = etapa

    if turma.ano_letivo == '2022':
        formacao_basica.portugues = portugues

        if etapa == '1ª Série':
            formacao_basica.arte = artes
            formacao_basica.ingles = ingles
        else:
            formacao_basica.arte = '-'
            formacao_basica.ingles = '-'

        formacao_basica.ed_fisica = ed_fisica
        formacao_basica.matematica = matematica

        if etapa == '1ª Série' or etapa == '2ª Série':
            formacao_basica.fisica = fisica
            formacao_basica.quimica = quimica
            formacao_basica.biologia = biologia
            formacao_basica.historia = historia
            formacao_basica.geografia = geografia
            formacao_basica.filosofia = filosofia
            formacao_basica.sociologia = sociologia
        else:
            formacao_basica.fisica = '-'
            formacao_basica.quimica = '-'
            formacao_basica.biologia = '-'
            formacao_basica.historia = '-'
            formacao_basica.geografia = '-'
            formacao_basica.filosofia = '-'
            formacao_basica.sociologia = '-'
    else:
        formacao_basica.portugues = portugues
        formacao_basica.matematica = matematica

        if etapa != '3ª Série':
            formacao_basica.arte = artes
            formacao_basica.ingles = ingles
            formacao_basica.ed_fisica = ed_fisica
            formacao_basica.fisica = fisica
            formacao_basica.quimica = quimica
            formacao_basica.biologia = biologia
            formacao_basica.historia = historia
            formacao_basica.geografia = geografia
            formacao_basica.filosofia = filosofia
            formacao_basica.sociologia = sociologia
        else:
            formacao_basica.arte = '-'
            formacao_basica.ingles = '-'
            formacao_basica.ed_fisica = '-'
            formacao_basica.fisica = '-'
            formacao_basica.quimica = '-'
            formacao_basica.biologia = '-'
            formacao_basica.historia = '-'
            formacao_basica.geografia = '-'
            formacao_basica.filosofia = '-'
            formacao_basica.sociologia = '-'
    formacao_basica.save()

    situacao = request.POST.get('aluno-fieldset-situacao')
    if situacao in ('transferido', 'desistente'):
        situacao_aluno(request, aluno, etapa)
    elif turma.etapa.id == 6 and turma.ano_letivo == '2022':
        itinerario_formativo_integral(request, aluno, turma, etapa, edicao)
    elif turma.etapa.id == 5 and turma.ano_letivo == '2022':
        itinerario_formativo_parcial(request, aluno, etapa, edicao)
    elif turma.etapa.id == 18 and turma.ano_letivo == '2022':
        itinerario_formativo_profissionalizante(request, aluno, etapa, edicao)
    elif turma.ano_letivo == '2021':
        parte_diversificada(request, aluno, etapa, edicao)