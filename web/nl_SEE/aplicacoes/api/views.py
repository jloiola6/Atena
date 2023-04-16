from django.http import JsonResponse

from aplicacoes.administracao.models import *
from aplicacoes.tecnologia.models import *
from aplicacoes.lotacao.models import *
from aplicacoes.core.views import verificar_manutencao

# Create your views here.

def verification(request):
    try:
        if request.session['username']:
            return True
    except KeyError:
        return False


def dados_escola(request):
    data = list(Escola.objects.values())

    return JsonResponse(data, safe=False)


def turma_escola(request):
    if verificar_manutencao() or not verification(request):
        return JsonResponse({'status': 'Sem permissão'}, safe=False)

    endereco_id = request.GET.get('id')
    mediador = request.GET.get('mediador')
    if mediador:
        data = []
        for turma in Turmas.objects.filter(endereco= endereco_id, ano_letivo= '2022').order_by('nome').values():
            mediadores = Professor_aluno.objects.filter(aluno__turma__id= int(turma['id']), status= 1).values_list('professor').distinct().count()
            if mediador == '1' and mediadores < 2:
                data.append(turma)
    else:
        data = list(Turmas.objects.filter(endereco= endereco_id, ano_letivo= '2022').order_by('nome').values())

    return JsonResponse(data, safe=False)


def servidor(request):
    if verificar_manutencao() or not verification(request):
        return JsonResponse({'status': 'Sem permissão'}, safe=False)

    valor = request.GET.get('valor')
    data = list(Servidor.objects.filter(nome__icontains= valor).order_by('nome').values('id', 'nome'))

    return JsonResponse(data, safe=False)


def aluno_turma(request):
    if verificar_manutencao() or not verification(request):
        return JsonResponse({'status': 'Sem permissão'}, safe=False)

    id_turma = request.GET.get('id')
    data = list(Aluno_turma.objects.filter(turma= id_turma, status= 1).order_by('aluno__nome').values('aluno__id', 'aluno__nome', 'status'))

    return JsonResponse(data, safe=False)

# API utilizada para a consulta do Programa Educação Conectada
def aluno_turma_EC(request):
    if verificar_manutencao() or not verification(request):
        return JsonResponse({'status': 'Sem permissão'}, safe=False)

    id_turma = request.GET.get('id')

    aluno_solicitacao = list(EC_solicitacao.objects.values_list('aluno_turma__aluno__id', flat= True))
    data = list(Aluno_turma.objects.filter(turma= id_turma).distinct().exclude(aluno__id__in= aluno_solicitacao).order_by('-aluno__bolsa_familia').values('aluno__id', 'aluno__nome', 'aluno__bolsa_familia'))

    return JsonResponse(data, safe=False)