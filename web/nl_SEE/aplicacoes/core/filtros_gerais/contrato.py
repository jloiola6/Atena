from aplicacoes.administracao.models import Vinculacao_contrato, Contrato_contrato, Contrato_gestor

def filtro_contratos(request, vinculo):
    if vinculo != None:
        id_contratos = [] 
        for id in Vinculacao_contrato.objects.filter(unidade_administrativa= vinculo).values('contrato'):
            id_contratos.append(id['contrato'])

        contratos = Contrato_contrato.objects.filter(id__in= id_contratos).order_by('empresa__nome')
    else:
        contratos = Contrato_contrato.objects.all().order_by('empresa__nome')

    ids = Contrato_contrato.objects.values_list('id', flat= True)
    equipes = Contrato_gestor.objects.filter(contrato__in= ids)

    numero_contrato = request.GET.get('numero_contrato')
    numero_sei = request.GET.get('numero_sei')
    empresa = request.GET.get('empresa')
    situacao = request.GET.get('situacao')
    gestor_titular = request.GET.get('gestor')

    if numero_contrato != None and numero_contrato != '':
        contratos = contratos.filter(numero_contrato__contains= numero_contrato)
        
    if numero_sei != None and numero_sei != '':
        contratos = contratos.filter(numero_sei__contains= numero_sei)
    
    if empresa != None and empresa != '':
        contratos = contratos.filter(empresa__id= empresa)

    if situacao != None and situacao != '':
        contratos = contratos.filter(situacao= situacao)

    if gestor_titular != None and gestor_titular != '':
       
        contratos = equipes.filter(gestor_titular__icontains= gestor_titular)
  
        if not contratos:
            contratos = equipes.filter(gestor_substituto__icontains= gestor_titular)

        if not contratos:
            contratos = equipes.filter(fiscal_titular__icontains= gestor_titular)
  
        if not contratos:
            contratos = equipes.filter(fiscal_substituto__icontains= gestor_titular)
     
    return contratos