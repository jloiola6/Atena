import re

from aplicacoes.administracao.models import *
from aplicacoes.core.actions import dict_compare, salvar_historico

# ACTION DO FORMULÁRIO DE MATRIZ
def formulario_matriz(request):
    post = request.POST

    nome = post['nome']
    etapa = post['etapa']

    matriz_etapa = Etapa.objects.get(id= etapa)

    nova_matriz = Matriz()
    nova_matriz.nome = nome
    nova_matriz.etapa = matriz_etapa
    nova_matriz.save()

    for campo in post:
        if 'disciplina' in campo:
            disciplina = post[campo]
            matriz_disciplina = Disciplinas.objects.get(id= disciplina)

            contador = re.sub('\D', '', campo)

            ch = post[f'ch{contador}']

            nova_matriz_disciplina = Matriz_disciplina()
            nova_matriz_disciplina.matriz = nova_matriz
            nova_matriz_disciplina.disciplina = matriz_disciplina
            nova_matriz_disciplina.carga_horaria = ch

            nova_matriz_disciplina.save()
