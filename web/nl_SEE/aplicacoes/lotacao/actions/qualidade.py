from aplicacoes.lotacao.models import Agendamento, Servidor, Servico, Atendimento, Atendimento_dia
from aplicacoes.core.views import salvar_historico
from datetime import date

def formulario_agendamento(request):
    edicao = False
    id_servidor = request.POST.get('servidor')
    contato = request.POST.get('contato')
    fieldset_horario = request.POST.get('fieldset-horarios').split(' ')
    atividade = request.POST.get('radio-atividade')


    servidor = Servidor.objects.get(id= id_servidor)
    servico = int(request.build_absolute_uri().split('/')[-1])
    data_formatada = fieldset_horario[0].split('/')
    hora = str(fieldset_horario[-1])+":00"
    data = date(int(data_formatada[2]), int(data_formatada[1]), int(data_formatada[0]))
    atendimento = Atendimento.objects.filter(id = servico)

    try:
        novo_agendamento = Agendamento()
        novo_agendamento.servidor = servidor
        novo_agendamento.data = data
        novo_agendamento.hora_atendimento = hora
        novo_agendamento.contato = contato
        novo_agendamento.atendimento = Atendimento.objects.get(id = servico)
        novo_agendamento.status = 0
        novo_agendamento.atividade = atividade
        if not Agendamento.objects.filter(servidor = servidor, data = data, hora_atendimento = hora, contato = contato, atendimento = Atendimento.objects.get(id = servico), status = 0, atividade = atividade).exists():
            novo_agendamento.save()
            salvar_historico(request, novo_agendamento, edicao, 'lotacao_agendamento')
            return True
        else:
            return False

    except:
        return False

def formulario_atendimento(request):
    edicao = False

    tipo_servico = request.POST.get('tipo-servico')
    printa = request.POST.get('atendente')
    try:
        if tipo_servico == 'novo':
            nome = request.POST.get('servico-novo')

            novo_servico = Servico()
            novo_servico.nome = nome
            novo_servico.save()
            salvar_historico(request, novo_servico, edicao, 'lotacao_servico')

        elif tipo_servico == 'existente':
            servico_existente = Servico.objects.get(id= request.POST.get('servico-existente'))
            atendente = Servidor.objects.get(id= request.POST.get('atendente'))

            novo_atendimento = Atendimento()
            novo_atendimento.servico = servico_existente
            novo_atendimento.atendente = atendente
            novo_atendimento.save()
            salvar_historico(request, novo_atendimento, edicao, 'lotacao_atendimento')
    except:
        print('ruim')

def formulario_atendimento_dia(request, atendimento):

    edicao = False

    dia = request.POST.get('dia')
    hora = request.POST.get('hora')

    if not Atendimento_dia.objects.filter(atendimento= atendimento, dia= dia, hora= hora).exists():
        novo_atendimento_dia = Atendimento_dia()
        novo_atendimento_dia.atendimento = atendimento
        novo_atendimento_dia.dia = dia
        novo_atendimento_dia.hora = hora
        novo_atendimento_dia.save()
        salvar_historico(request, novo_atendimento_dia, edicao, 'lotacao_atendimento_dia')

def alterar_status_agendamento(request):
    agendamento = request.POST.get('agendamento')
    status = request.POST.get('status')
    agenda = Agendamento.objects.get(id = agendamento)

    if status in ['1', '2', '3']:
        agenda.status = status
        agenda.save()

    elif not Agendamento.objects.filter(atendimento = agenda.atendimento, data = agenda.data, hora_atendimento = agenda.hora_atendimento, status = '0').exists():
        agenda.status = status
        agenda.save()

    else:
        print('Deu Ruim!')
    
def lista_espera_act(request):
    lista = Agendamento()
    try:
        lista.servidor = Servidor.objects.get(id= request.POST.get('servidor'))
        lista.atendimento = Atendimento.objects.get(id= request.POST.get('servico'))
        lista.contato = request.POST.get('telefone')
        lista.status = 4
        lista.atividade = 'Espera'
        
        lista.data = None
        lista.hora_atendimento = None
        
        lista.save()
    
    except:
        print('Deu ruim')

def formulario_agendamento_lista(request, objeto):
    fieldset_horario = request.POST.get('fieldset-horarios').split(' ')
    data_formatada = fieldset_horario[0].split('/')
    
    agendamento = Agendamento.objects.get(id = objeto)
    agendamento.data = date(int(data_formatada[2]), int(data_formatada[1]), int(data_formatada[0]))
    agendamento.hora_atendimento = str(fieldset_horario[-1])+":00"
    agendamento.status = 0
    agendamento.save()