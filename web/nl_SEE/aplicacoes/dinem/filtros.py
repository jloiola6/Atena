from aplicacoes.administracao.models import Endereco
from aplicacoes.dinem.models import Escola_Dinem

def filtro_dinem(request):

    escolas = []
    dinem = Escola_Dinem.objects.all()
    for escola in dinem:
        escolas.append(escola.escola.cod_inep)

    enderecos = Endereco.objects.filter(tipo='S', escola__cod_inep__in= escolas).values('escola__cod_inep', 'escola__nome_escola', 'municipio', 'regiao', 'tipo_localizacao').order_by('escola__nome_escola')

    inep = request.GET.get('cod_inep')
    unidade = request.GET.get('nome_unidade')

    if inep != '' and inep != None:
        enderecos = enderecos.filter(escola__cod_inep__icontains= inep)

    if unidade != '' and unidade != None:
        enderecos = enderecos.filter(escola__nome_escola__icontains = unidade)

    return enderecos