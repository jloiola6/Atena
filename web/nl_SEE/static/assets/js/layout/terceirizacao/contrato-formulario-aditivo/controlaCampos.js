// Script para controlar o comportamento do formulário de contrato aditivo

(() => {

    // Função que recebe uma String em formato de moeda e converte em um Float
    const converterValor = (str) => {
        if(str.trim() != '')
            return Number.parseFloat(str
            .replace(/\D/g, '')
            .replace(/([0-9]+)(\d{2})/, '$1.$2'))
        else
            return 0.0
    }

    // Função para desativar um grupo de campos
    const desativaGrupo = (grupo) => {
        const campos = grupo.querySelectorAll('input')

        campos.forEach((campo) => {
            if('radioAtivo' in campo.dataset){
                campo.nextElementSibling.remove()
                campo.remove()
            }else{
                campo.readOnly = true
                campo.parentElement.parentElement.parentElement.setAttribute('data-grupo-ativo', 'false')
            }
        })
    }

    // Campo da data final do contrato
    const dataContrato = document.querySelector('[data-final-contrato]')
    // Campo do valor global do contrato 
    const totalGlobal = document.querySelector('[data-valor-global]')

    // Função para atualizar o valor da vigencia do contrato de acordo com a data selecionada 
    const atualizaVigencia = () => {
        const dataInicial = new Date(dataContrato.min)
        const mesInicial = dataInicial.getMonth() + 1
        const anoInicial = dataInicial.getFullYear()

        const valorData = dataContrato.value
        const mesFinal = new Date(valorData).getMonth() + 1
        const anoFinal = new Date(valorData).getFullYear()

        let diferenca = mesFinal- mesInicial

        if(anoFinal - anoInicial > 0)
            diferenca += 12 * (anoFinal - anoInicial)

        totalGlobal.setAttribute('data-valor-global', diferenca)

        document.querySelector('[data-contrato-vigencia]').value = diferenca

        atualizaCampoGlobal()
    }

    dataContrato.addEventListener('input', atualizaVigencia)

    // Função para atualziar o valor global do contrato de acordo com os totais dos itens e a vigencia
    const atualizaCampoGlobal = () => {
        const totais = document.querySelectorAll('[data-total-item]')

        let totalAtual = 0.0

        // Percorrendo os grupos de campos para recolher os valores de totais dos itens
        totais.forEach((total) => {
            const grupoCampos = total.parentElement.parentElement
            const radioInativar = grupoCampos.querySelector('[data-inativar-item]')

            // Verifica a existencia do radio de inativação do produto
            if(radioInativar != null)
                if(radioInativar.checked)
                    desativaGrupo(grupoCampos)
                else
                    radioInativar.addEventListener('click', atualizaCampoGlobal)

            const grupoAtivo = grupoCampos.getAttribute('data-grupo-ativo') == 'true'

            if(grupoAtivo)
                totalAtual += converterValor(total.value)
        })

        const vigencia = Number.parseInt(totalGlobal.getAttribute('data-valor-global'))
        const novoGlobal = new String((totalAtual * vigencia).toFixed(2))

        totalGlobal.value = novoGlobal
        totalGlobal.dispatchEvent(new Event('input'))
    }

    // Função para inicializar os escutadores nos campos de totais dos itens
    const inicializaTotais = () => {
        const totais = document.querySelectorAll('[data-total-item]')

        totais.forEach((total) => {
            total.addEventListener('input', atualizaCampoGlobal)
        })
    }

    // Função para atualizar o total de um item de acordo com a quantidade e valor digitados
    const atualizaTotalItem = (evento) => {
        const pai = evento.target.parentElement.parentElement

        const grupoQtd = pai.children[3]
        const campoQtd = grupoQtd.lastElementChild

        const grupoUnitario = pai.children[4]
        const campoUnitario = grupoUnitario.lastElementChild

        const grupoTotal = pai.children[5]
        const campoTotal = grupoTotal.lastElementChild

        const qtd = Number.parseFloat(campoQtd.value)
        const valor = converterValor(campoUnitario.value)

        const novoValor = qtd * valor
        
        campoTotal.value = novoValor.toFixed(2)
        campoTotal.dispatchEvent(new Event('input'))
    }

    // Função para inicializar os escutadores nos campos de quantidade e valores dos itens
    const inicializaTotaisItens = () => {
        const quantidades = document.querySelectorAll('[data-qtd-item]')
        const unitarios = document.querySelectorAll('[data-unitario-item]')

        quantidades.forEach((quantidade) => {
            quantidade.addEventListener('input', atualizaTotalItem)
        })

        unitarios.forEach((unitario) => {
            unitario.addEventListener('input', atualizaTotalItem)
        })
    }

    atualizaVigencia()
    atualizaCampoGlobal()
    inicializaTotais()
    inicializaTotaisItens()
})

()