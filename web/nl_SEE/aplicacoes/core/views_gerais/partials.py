from aplicacoes.administracao.models import *
from aplicacoes.coex.models import *
from aplicacoes.lotacao.models import Servidor_lotacao

def dados_aplicacao(aplicacao, id):
    if aplicacao == 'COEX':
        escola = Escola.objects.get(id= id)
        coex = Coex.objects.get(escola= escola, status=1)
        endereco = Endereco.objects.get(escola= escola, tipo= 'S')
        return escola, coex, endereco


def dados_unidades(aplicacao, id):
    escola, coex, endereco = dados_aplicacao(aplicacao, id)
    possui_contatos = Contato.objects.filter(endereco= endereco).count() > 0
    contatos = None
    if possui_contatos:
        contatos = Contato.objects.filter(endereco= endereco)

    
    escola_etapas = Etapa_escola.objects.filter(escola= escola)

    diretor = pedagogico = ensino = secretario = administrativo = 'Não cadastrado'
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).exists():
        diretor = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Diretor(a)', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).exists():
        pedagogico = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Cordenador(a) Pedagogico', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).exists():
        ensino = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) de Ensino', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).exists():
        administrativo = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Coordenador(a) Administrativo', status= 1).last().contrato.servidor.nome
    if Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).exists():
        secretario = Servidor_lotacao.objects.filter(unidade_escolar= endereco, funcao= 'Secretario(a) Escolar', status= 1).last().contrato.servidor.nome

    return escola, coex, contatos, possui_contatos, endereco, diretor, pedagogico, ensino, secretario, administrativo, escola_etapas

    
    