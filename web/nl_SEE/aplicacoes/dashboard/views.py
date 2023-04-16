from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count

from aplicacoes.core.views import verificar_manutencao
from aplicacoes.usuario.views import verificacao_maxima

from aplicacoes.administracao.models import *
from aplicacoes.lotacao.models import *


# Create your views here.

def pontuacao(valor):
    return "{0:,}".format(valor).replace(',', '.')


def index(request):
    if verificar_manutencao() or not verificacao_maxima(request, [11]):
        return HttpResponseRedirect('/')

    template_name = 'dashboard/index.html'

    # Totais para os quantitativos
    # total_alunos = pontuacao(Escola.objects.aggregate(Sum('total_alunos'))['total_alunos__sum'])
    total_alunos = pontuacao(Aluno.objects.all().count())
    total_escolas = pontuacao(Escola.objects.all().count())
    total_professores = pontuacao(Servidor_lotacao.objects.filter(status= 1, funcao__icontains= 'professor').count())

    # Escolas por tipo de localização
    escolas_urbanas = Endereco.objects.filter(tipo_localizacao= 'Urbano').count()
    escolas_rurais = Endereco.objects.filter(tipo_localizacao= 'Rural').count()
    escolas_indigenas = Endereco.objects.filter(tipo_localizacao= 'Indígena').count()
    escolas_ni = Endereco.objects.filter(tipo_localizacao= 'Não informado').count()

    # Escolas por regional
    alto_acre = Endereco.objects.filter(regiao= 'Alto Acre').count()
    baixo_acre = Endereco.objects.filter(regiao= 'Baixo Acre').count()
    jurua = Endereco.objects.filter(regiao= 'Juruá').count()
    purus = Endereco.objects.filter(regiao= 'Purus').count()
    tarauaca = Endereco.objects.filter(regiao= 'Tarauacá / Envira').count()

    # Escolas por tificação
    escolas_a = Escola.objects.filter(tipificacao= 'A').count()
    escolas_b = Escola.objects.filter(tipificacao= 'B').count()
    escolas_c = Escola.objects.filter(tipificacao= 'C').count()
    escolas_d = Escola.objects.filter(tipificacao= 'D').count()
    escolas_e = Escola.objects.filter(tipificacao= 'E').count()

    # Escolas com SIMAED
    escolas_com_simaed = Detalhes_escola.objects.filter(simaed= 1).count()
    escolas_sem_simaed = Detalhes_escola.objects.filter(simaed= 0).count()

    # Escolas com energia elétrica
    escolas_com_energia = Detalhes_escola.objects.filter(energia_eletrica= 1).count()
    escolas_sem_energia = Detalhes_escola.objects.filter(energia_eletrica= 0).count()

    # Alunos por sexo
    alunos_masculino = Aluno.objects.filter(sexo= 'M').count()
    alunos_feminino = Aluno.objects.filter(sexo= 'F').count()

    # Alunos com transporte
    alunos_com_transporte = Aluno.objects.filter(transporte= 1).count()
    alunos_sem_transporte = Aluno.objects.filter(transporte= 0).count()

    # Alunos com Bolsa Família
    alunos_com_bolsa = Aluno.objects.filter(bolsa_familia= 1).count()
    alunos_sem_bolsa = Aluno.objects.filter(bolsa_familia= 0).count()

    # Deficiencias mais recorrentes
    deficiencias = Aluno.objects.exclude(deficiencia= '').values('deficiencia').annotate(Count('deficiencia')).order_by('-deficiencia__count')[:5]
 
    # Aunos por etapa de ensino
    alunos_fundamental_iniciais = Aluno.objects.filter(turma__etapa__id__in= [3] ).count()
    alunos_fundamental_finais = Aluno.objects.filter(turma__etapa__id__in= [4] ).count()
    alunos_medio = Aluno.objects.filter(turma__etapa__id__in= [5, 6] ).count()
    alunos_aee = Aluno.objects.filter(turma__etapa__id__in= [10] ).count()
    alunos_eja = Aluno.objects.filter(turma__etapa__id__in= [7, 8, 9] ).count()

    # Alunos por ano
    # Ensino Fundamental
    alunos_fundamental1 = Aluno.objects.filter(turma__ano_serie= '1º Ano').count()
    alunos_fundamental2 = Aluno.objects.filter(turma__ano_serie= '2º Ano').count()
    alunos_fundamental3 = Aluno.objects.filter(turma__ano_serie= '3º Ano').count()
    alunos_fundamental4 = Aluno.objects.filter(turma__ano_serie= '4º Ano').count()
    alunos_fundamental5 = Aluno.objects.filter(turma__ano_serie= '5º Ano').count()
    alunos_fundamental6 = Aluno.objects.filter(turma__ano_serie= '6º Ano').count()
    alunos_fundamental7 = Aluno.objects.filter(turma__ano_serie= '7º Ano').count()
    alunos_fundamental8 = Aluno.objects.filter(turma__ano_serie= '8º Ano').count()
    alunos_fundamental9 = Aluno.objects.filter(turma__ano_serie= '9º Ano').count()

    # Ensino Médio
    alunos_medio1 = Aluno.objects.filter(turma__ano_serie= '1ª Série').count()
    alunos_medio2 = Aluno.objects.filter(turma__ano_serie= '2ª Série').count()
    alunos_medio3 = Aluno.objects.filter(turma__ano_serie= '3ª Série').count()

    # EJA
    alunos_eja1 = Aluno.objects.filter(turma__ano_serie= 'Módulo I').count()
    alunos_eja3 = Aluno.objects.filter(turma__ano_serie= 'Módulo III').count()
    alunos_eja5 = Aluno.objects.filter(turma__ano_serie= 'Módulo V').count()

    return TemplateResponse(request, template_name, locals())
    