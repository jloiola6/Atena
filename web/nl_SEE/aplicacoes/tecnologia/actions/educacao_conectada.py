from aplicacoes.administracao.models import *
from aplicacoes.tecnologia.models import *



def formulario_tablet(request, alunos):
    for aluno in alunos:

        tablet=Ec_tablet()
        if request.POST.get(f'tablet_serial-{aluno.id}') and request.POST.get(f'tablet_imei-{ aluno.id }') and request.POST.get(f'chip_serial-{ aluno.id }'):
            tablet.serial_tablet = request.POST.get(f'tablet_serial-{aluno.id}')
            tablet.imei_tablet = request.POST.get(f'tablet_imei-{ aluno.id }')
            tablet.serial_chip = request.POST.get(f'chip_serial-{ aluno.id }')
            tablet.cad_unico = aluno.aluno.bolsa_familia
            tablet.status = 0
            tablet.aluno_turma = aluno
            tablet.endereco_escola= None
            tablet.save()

def editar_dados(request, aluno_turma):
    tablet = Ec_tablet.objects.get(aluno_turma = aluno_turma)
    tablet.imei_tablet = request.POST.get('patrimonio')
    tablet.serial_chip = request.POST.get('chip')
    tablet.serial_tablet = request.POST.get('imei-tablet')
    if 'status' in request.POST:
        if request.POST.get('status') == '0':
            tablet.status = 0
        elif request.POST.get('status') == '1':
            tablet.status = 1
        elif request.POST.get('status') == '2':
            tablet.status = 2
    tablet.save()


def entregar_tablets(tablets):
    for tablet in tablets:
        tablet.status = 1
        tablet.save()
