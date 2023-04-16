from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from itertools import chain

from aplicacoes.administracao.models import *
from aplicacoes.usuario.models import Usuarios, Permissao, Logs

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.lotacao.models import *
from aplicacoes.terceirizacao.models import Contrato_lotacao

# def servidores(request):
    # if verificar_manutencao():
    #     return HttpResponseRedirect('/')

    # if not verificacao_maxima(request, [1, 5]):
    #     return HttpResponseRedirect('/')

    # template_name = 'administracao/unidades/servidores/servidores.html'
    # user = request.session['username']

    # endereco_id = request.GET.get('id')
    # if endereco_id in (None, ''):
    #     return HttpResponseRedirect('/administracao/unidades')

    # endereco = Endereco.objects.get(id= endereco_id)
    # escola = endereco.escola

    # diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'
    # if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
    #     diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
    # if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico').exists():
    #     pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico').last().contrato.servidor.nome
    # if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino').exists():
    #     ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino').last().contrato.servidor.nome
    # if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo').exists():
    #     administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo').last().contrato.servidor.nome
    # if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar').exists():
    #     secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar').last().contrato.servidor.nome

    # gestores = ['Diretor(a)', 'Cordenador(a) Pedagogico', 'Coordenador(a) de Ensino', 'Coordenador(a) Administrativo', 'Secretario(a) Escolar']
    # funcoes_alunos = ['Mediador', 'Atendente Pessoal', 'Atendimento Domiciliar', 'Interprete', 'Professor(a) Brailista', 'Professor(a)', 'Professor(a) AEE']

    # servidores_see = Servidor_lotacao.objects.filter(unidade_escolar= endereco, status= 1).exclude(funcao__in= gestores).values('contrato__servidor__nome', 'contrato__digito', 'contrato__cargo__nome', 'funcao', 'contrato__cargo__carga_horaria').distinct()
    # qtd_servidores_see = servidores_see.count()

    # servidores_see_sem_turma = servidores_see.filter(funcao__in= funcoes_alunos)
    # qtd_servidores_see_sem_turma = servidores_see_sem_turma.count()

    # servidores_see_restantes = servidores_see.exclude(funcao__in= funcoes_alunos)
    # qtd_servidores_see_restantes = servidores_see_restantes.count()

    # servidores_terceirizados = Contrato_lotacao.objects.filter(endereco= endereco, status= 1).values('servidor__nome', 'item__descricao')
    # qtd_servidores_terceirizados = servidores_terceirizados.count()

    # professores = []
    # grupo = []
    # dados = []
    # situacao = False
    # quantidade = 0
    # qtd_enturmados = 0
    # for id_professor in Grade.objects.filter(turma__endereco= endereco, professor__isnull= False, status= 1).values('professor').distinct():
    #     situacao = True
    #     quantidade += 1
    #     servidor = (Servidor_lotacao.objects.get(id= id_professor['professor'])).contrato.servidor
    #     qtd_turmas = Grade.objects.filter(professor= id_professor['professor'], status= 1).values('turma').distinct().count()

    #     total = 0
    #     total += sum(int(x) for x in Grade.objects.filter(professor= id_professor['professor']).values_list('carga_horaria', flat= True) if x.isdigit())
    #     dados.append((id_professor['professor'], servidor, qtd_turmas, total))

    # if situacao:
    #     grupo.append('Professor(a)')
    #     grupo.append(dados)
    #     professores.append(grupo)
    #     grupo.append(quantidade)
    #     qtd_enturmados += quantidade

    # for funcao in funcoes_alunos:
    #     dados = []
    #     grupo = []
    #     situacao = False
    #     quantidade = 0
    #     for id_professor in Professor_aluno.objects.filter(professor__in= servidores_see.filter(funcao= funcao).values_list('id', flat= True), status= 1).values('professor').distinct():
    #         situacao = True
    #         quantidade += 1
    #         servidor = (Servidor_lotacao.objects.get(id= id_professor['professor'])).contrato.servidor
    #         qtd_alunos = Professor_aluno.objects.filter(professor= id_professor['professor'], status= 1).values('aluno').distinct().count()

    #         dados.append((id_professor['professor'], servidor, qtd_alunos))
    #     if situacao:
    #         grupo.append(funcao)
    #         grupo.append(dados)
    #         professores.append(grupo)
    #         grupo.append(quantidade)
    #         qtd_enturmados += quantidade

    # return TemplateResponse(request, template_name, locals())


def professor_perfil(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [1, 5]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/unidades/servidores/professor-perfil.html'
    user = request.session['username']

    id_servidor_lotacao = request.GET.get('id_servidor_lotacao')
    endereco_id = request.GET.get('id_endereco')
    endereco = Endereco.objects.get(id= endereco_id)
    escola = endereco.escola

    grades = Grade.objects.filter(turma__endereco= endereco, professor= id_servidor_lotacao)
    servidor = Servidor_lotacao.objects.get(id= id_servidor_lotacao)
    funcao = servidor.funcao
    servidor = servidor.contrato.servidor

    professores = ('Professor(a)', 'Professor(a) AEE')
    if funcao in professores:
        turma_id = []
        turma_nome = []
        turma_total = []
        carga_horaria = []
        turno = []
        for grade in grades:
            if grade.turma.id not in turma_id:
                turma_id.append(grade.turma.id)
                turma_nome.append(grade.turma.nome)
                turma_total.append(grade.turma.total_alunos)
                carga_horaria.append(float(grade.carga_horaria))
                turno.append(grade.turma.turno)
            else:
                valor = turma_id.index(grade.turma.id)
                carga_horaria[valor] += float(grade.carga_horaria)

        turmas = []
        for item in range(len(turma_id)):
            turmas.append((turma_id[item], turma_nome[item], turma_total[item], carga_horaria[item], turno[item]))

        total_turmas = len(turmas)

        disciplinas = grades.values('disciplina__nome').distinct()
        turmas_disciplinas = grades.values('turma__nome', 'disciplina__nome').distinct()
        total_disciplinas = disciplinas.count()
    else:
        alunos = []
        qtd_alunos = 0
        for dado in Professor_aluno.objects.filter(professor= id_servidor_lotacao, status= 1):
            if Aluno_turma.objects.filter(aluno= dado.aluno, status= 1, turma__endereco= endereco).exists():
                detalhes = Aluno_turma.objects.get(aluno= dado.aluno, status= 1, turma__endereco= endereco)
                alunos.append(detalhes)
                qtd_alunos += 1


    return TemplateResponse(request, template_name, locals())