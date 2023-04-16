from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from aplicacoes.usuario.views import verificacao_maxima
from aplicacoes.core.views import verificar_manutencao
from aplicacoes.tecnologia.models import * 
from aplicacoes.tecnologia.actions.links import *


def pre_empenho_formulario(request):
    if not verificacao_maxima(request, [12]) or verificar_manutencao():
        return HttpResponseRedirect('/')

    template_name = 'tecnologia/contrato/pre-empenho-formulario.html'
    user = request.session['username']
    permissao = Permissao.objects.get(usuario__login= user, servico__id= 12)

    id_contrato = request.GET.get('id_contrato')
    contrato = Contrato_contrato.objects.get(id= id_contrato)

    fonte = '300'

    itens = []
    for item in Contrato_item.objects.filter(contrato= contrato, status= 1):
        if Link.objects.filter(item= item, status= 'ATIVO', fonte= fonte).exists():
            valor_unitario = item.valor_unitario

            velocidade = item.descricao.split()
            for i in velocidade:
                if 'MB' in i or 'Mb' in i:
                    velocidade = i
                    break
            velocidade = i
            qtd_link = Link.objects.filter(item= item, status= 'ATIVO', fonte= fonte).count()

            if not ',00' in valor_unitario:
                valor = ''
                for i in valor_unitario.split('.'):
                    valor += i
                valor_unitario = valor
                
                valor_mensal = float(valor_unitario.replace('R$', '').replace(',', '.').strip()) * qtd_link
                
                valor_mensal = "{0:,}".format(valor_mensal).replace(',', '.')
                valor_mensal = f'R$ {valor_mensal}'

                if valor_mensal[-2] == '.':
                    valor_mensal = f'R$ {valor_mensal}0'
                else:
                    valor_mensal = f'R$ {valor_mensal}'

                valor_mensal = valor_mensal[:-3] + ',' +valor_mensal[-2:]
            else:
                print('aqui')
                print('R$ 9.500,00'.replace('R$', '').replace(',', '.').strip())
                valor_mensal = int(valor_unitario.replace('R$', '').replace(',00', '').replace('.', '').strip()) * qtd_link
                print(valor_mensal)
                valor_mensal = "R$ {0:,},00".format(valor_mensal).replace(',', '.')
                valor_mensal = f'R$ {valor_mensal}0'
                valor_mensal = valor_mensal[:-4] + ',' +valor_mensal[-2:]

            itens.append((item.numero_item, velocidade, qtd_link, fonte, valor_unitario, valor_mensal, item.descricao))
    for i in itens:
        print(i)
            # print(qtd_link)
    # itens = Link.objects.filter(item__contrato= contrato)
    # tus= 1)

    # lista = 
    # for i in itens:
    #     quantidade =  int(i.item.quantidade) -  int(i.item.qtd_vagas)

    return TemplateResponse(request, template_name, locals())