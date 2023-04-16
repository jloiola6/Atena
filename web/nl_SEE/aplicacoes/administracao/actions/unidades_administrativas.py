from aplicacoes.administracao.models import * 
from aplicacoes.core.actions import dict_compare, salvar_historico

import re


def formulario_departamento(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')        
    telefone = request.POST.get('telefone')
    telefone = re.sub('\D', '', telefone)        
    email = request.POST.get('email')        

    #Salvando no banco dados do departamento
    departamento = Unidade_administrativa()
    diretoria = Unidade_administrativa.objects.get(id= request.GET.get('id'))
    departamento.hierarquia = diretoria.id
    departamento.nome = nome
    departamento.sigla = sigla
    departamento.telefone = telefone
    departamento.email = email
    departamento.categoria = Unidade_administrativa_categoria.objects.get(id= 3)
    departamento.hierarquia = int(request.GET.get('id'))
    departamento.save()

    edicao = False # APagar futuramente pois não contem edicao nesta tela, ainda...
    salvar_historico(request, departamento, edicao, 'administracao_unidade_administrativa')

    localidade_sede = request.POST.get('unidade-formulario-sede')
    if localidade_sede == 'nao':
        municipio = request.POST.get('municipio')
        # regiao = request.POST.get('regiao')        
        regiao = ''    
        cep = request.POST.get('cep')  
        cep = re.sub('\D', '', cep)     
        rua = request.POST.get('rua') 
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')        
        complemento = request.POST.get('complemento')        

        endereco = Unidade_administrativa_endereco()
        endereco.uf = 'AC'
        endereco.municipio = municipio
        endereco.regiao = regiao
    
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.save()

        edicao = False # APagar futuramente pois não contem edicao nesta tela, ainda...
        salvar_historico(request, endereco, edicao, 'administracao_unidade_administrativa_endereco')

        departamento.endereco = endereco

    else:
        departamento.endereco = Unidade_administrativa_endereco.objects.get(id= 1)
    
    departamento.save()


def formulario_divisao(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')
    telefone = request.POST.get('telefone')    
    telefone = re.sub('\D', '', telefone) 
    email = request.POST.get('email')    

    #Salvando no banco dados da divisão
    divisao = Unidade_administrativa()
    departamento = Unidade_administrativa.objects.get(id= request.GET.get('id'))
    divisao.departamento = departamento.id
    divisao.nome = nome
    divisao.sigla = sigla
    divisao.telefone = telefone
    divisao.email = email
    divisao.categoria = Unidade_administrativa_categoria.objects.get(id= 4)
    divisao.hierarquia = int(request.GET.get('id'))
    divisao.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...
    salvar_historico(request, divisao, edicao, 'administracao_unidade_administrativa')

    localidade_sede = request.POST.get('unidade-formulario-sede')
    if localidade_sede == 'nao':
        municipio = request.POST.get('municipio')
        # regiao = request.POST.get('regiao')        
        regiao = ''    
        cep = request.POST.get('cep')
        cep = re.sub('\D', '', cep)        
        rua = request.POST.get('rua') 
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')        
        complemento = request.POST.get('complemento')    

        endereco = Unidade_administrativa_endereco()
        endereco.uf = 'AC'
        endereco.municipio = municipio
        endereco.regiao = regiao
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.save()

        edicao = False # APagar futuramente pois não contem edicao nesta tela, ainda...
        salvar_historico(request, endereco, edicao, 'administracao_unidade_administrativa_endereco')

        divisao.endereco = endereco

    else:
        divisao.endereco = Unidade_administrativa_endereco.objects.get(id= 1)
    
    divisao.save()


def formulario_nucleo(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')
    telefone = request.POST.get('telefone')   
    telefone = re.sub('\D', '', telefone)      
    email = request.POST.get('email')    

    #Salvando no banco dados do nucleo
    nucleo = Unidade_administrativa()
    divisao = Unidade_administrativa.objects.get(id= request.GET.get('id'))
    nucleo.divisao = divisao
    nucleo.nome = nome
    nucleo.sigla = sigla
    nucleo.telefone = telefone
    nucleo.email = email
    nucleo.categoria = Unidade_administrativa_categoria.objects.get(id= 5)
    nucleo.hierarquia = int(request.GET.get('id'))
    nucleo.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...
    salvar_historico(request, nucleo, edicao, 'administracao_unidade_administrativa')

    localidade_sede = request.POST.get('unidade-formulario-sede')
    if localidade_sede == 'nao':
        municipio = request.POST.get('municipio')
        # regiao = request.POST.get('regiao')        
        regiao = ''    
        cep = request.POST.get('cep')
        cep = re.sub('\D', '', cep)        
        rua = request.POST.get('rua') 
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')        
        complemento = request.POST.get('complemento')    

        endereco = Unidade_administrativa_endereco()
        endereco.uf = 'AC'
        endereco.municipio = municipio
        endereco.regiao = regiao
    
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.save()

        edicao = False # APagar futuramente pois não contem edicao nesta tela, ainda...
        salvar_historico(request, endereco, edicao, 'administracao_unidade_administrativa_endereco')

        nucleo.endereco = endereco

    else:
        nucleo.endereco = Unidade_administrativa_endereco.objects.get(id= 1)
    
    nucleo.save()


def formulario_polo_centro(request):
    #Capturando dados 
    nome = request.POST.get('nome')
    sigla = request.POST.get('sigla')
    telefone = request.POST.get('telefone')   
    telefone = re.sub('\D', '', telefone)      
    email = request.POST.get('email')    

    #Salvando no banco dados do nucleo
    polo_centro = Unidade_administrativa()
    polo_centro.nome = nome
    polo_centro.sigla = sigla
    polo_centro.telefone = telefone
    polo_centro.email = email
    polo_centro.categoria = Unidade_administrativa_categoria.objects.get(id= 6)
    polo_centro.hierarquia = int(request.GET.get('id'))
    polo_centro.save()

    edicao = False #APagar futuramente pois não contem edicao nesta tela, ainda...
    salvar_historico(request, polo_centro, edicao, 'administracao_unidade_administrativa')

    localidade_sede = request.POST.get('unidade-formulario-sede')
    if localidade_sede == 'nao':
        municipio = request.POST.get('municipio')
        # regiao = request.POST.get('regiao')        
        regiao = ''    
        cep = request.POST.get('cep')
        cep = re.sub('\D', '', cep)        
        rua = request.POST.get('rua') 
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')        
        complemento = request.POST.get('complemento')    

        endereco = Unidade_administrativa_endereco()
        endereco.uf = 'AC'
        endereco.municipio = municipio
        endereco.regiao = regiao
    
        endereco.cep = cep
        endereco.rua = rua
        endereco.numero = numero
        endereco.bairro = bairro
        endereco.complemento = complemento
        endereco.save()

        edicao = False # APagar futuramente pois não contem edicao nesta tela, ainda...
        salvar_historico(request, endereco, edicao, 'administracao_unidade_administrativa_endereco')

        polo_centro.endereco = endereco

    else:
        polo_centro.endereco = Unidade_administrativa_endereco.objects.get(id= 1)
    
    polo_centro.save()


def endereco_editar(request):
    edicao = False
    municipio =  request.POST.get('municipio')
    regiao =  request.POST.get('regiao')
    zoneamento =  request.POST.get('zoneamento')
    cep = request.POST.get('cep')
    rua =  request.POST.get('rua')
    numero =  request.POST.get('numero')
    bairro =  request.POST.get('bairro')
    complemento =  request.POST.get('complemento')

    print(complemento)
    unidade = Unidade_administrativa.objects.get(id= int(request.GET.get('id')))

    endereco = Unidade_administrativa_endereco()
    endereco.uf = 'AC'
    endereco.municipio = municipio
    endereco.regiao = regiao
    endereco.cep = cep
    endereco.rua = rua
    endereco.numero = numero
    endereco.bairro = bairro
    endereco.complemento = complemento
    endereco.save()
    salvar_historico(request, endereco, edicao, 'administracao_unidade_administrativa_endereco')

    unidade.endereco = endereco
    unidade.save()