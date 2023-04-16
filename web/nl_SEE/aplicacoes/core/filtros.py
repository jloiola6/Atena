from aplicacoes.tecnologia.models import Solicitacao_chamado

def filtro_chamados(request, servidor):
    chamados = Solicitacao_chamado.objects.filter(solicitacao__user_solicitante = servidor.id)

    protocolo = request.GET.get('protocolo')
    servico = request.GET.get('servico')
    status = request.GET.get('status')

    if protocolo != '' and protocolo != None:
        chamados = chamados.filter(solicitacao__id= protocolo)

    if servico != '' and servico != None:
        chamados = chamados.filter(servico= servico)

    if status != '' and status != None:
        chamados = chamados.filter(solicitacao__situacao= status)

    return chamados