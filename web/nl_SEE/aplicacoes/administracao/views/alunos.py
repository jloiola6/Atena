from aplicacoes.administracao.models import *
from aplicacoes.coex.models import *
from aplicacoes.tecnologia.models import *
from aplicacoes.fundiaria.models import *
from aplicacoes.core.views import verificar_manutencao

from aplicacoes.lotacao.models import *
from aplicacoes.usuario.models import Logs, Permissao, Usuarios, Servico
from aplicacoes.usuario.views import verificacao_maxima
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from unidecode import unidecode
from aplicacoes.fundiaria.exportar import exportar_pdf_escola

from aplicacoes.administracao.filtros import filtro_alunos

def alunos(request):
    if verificar_manutencao():
        return HttpResponseRedirect('/')

    if not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/alunos/alunos.html'
    user = request.session['username']

    alunos = filtro_alunos(request)
    alunos_aux = alunos
    quantidade_alunos = alunos.count()

    page = request.GET.get('page')
    if page is None:
        page = 1

    valor_paginacao = 15*int(page)

    paginator = Paginator(alunos, 15)
    alunos = paginator.get_page(page)

    gets_primeira = 'page=1'
    gets_proxima = f'page={str(int(page)+1)}'
    gets_anterior = f'page={str(int(page)-1)}'
    gets_ultima = f'page={paginator.num_pages}'

    if '?' in request.get_full_path():

        gets = (request.get_full_path().split('?')[1])

        if 'page' not in gets:
            gets = f'page={page}&' + gets

        proxima_pagina = str(int(page)+1)
        pagina_anterior = str(int(page)-1)

        gets_primeira = gets.replace(f'page={page}', 'page=1')
        gets_proxima = gets.replace(f'page={page}', f'page={proxima_pagina}')
        gets_anterior = gets.replace(f'page={page}', f'page={pagina_anterior}')
        gets_ultima = gets.replace(f'page={page}', gets_ultima)

    # cont_nomes = 0
    # cont_nomes_tratados = 0

    # for aluno in alunos_aux:
    #     cont_nomes += 1
    #     nome = aluno.nome
    #     nome_tratado = nome.strip()

    #     print(f'{cont_nomes}. {nome} - {len(nome)} - {nome_tratado.strip()} - {len(nome_tratado.strip())}')

    #     if(len(nome) != len(nome_tratado)):
    #         print(f'ATUALIZAR NOME')
    #         aluno.nome = nome_tratado
    #         aluno.save()
    #         cont_nomes_tratados += 1
    #     else:
    #         print('NOME CORRETO')

    # print()
    # print(f'{cont_nomes_tratados} NOMES ATUALIZADOS')

    return TemplateResponse(request, template_name, locals())


def aluno_perfil(request, id_aluno):
    if verificar_manutencao() or not verificacao_maxima(request, [7]):
        return HttpResponseRedirect('/')

    template_name = 'administracao/alunos/aluno-perfil.html'
    user = request.session['username']

    try:
        aluno = Aluno.objects.get(id= id_aluno)
    except:
        return HttpResponseRedirect('/administracao')

    # LISTANDO AS ENTURMAÇÕES DO ALUNO
    enturmacoes = Aluno_turma.objects.filter(aluno= aluno)

    escolas = Endereco.objects.all()

    return TemplateResponse(request, template_name, locals())