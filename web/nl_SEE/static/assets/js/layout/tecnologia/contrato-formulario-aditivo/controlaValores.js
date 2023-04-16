// Script para controlar os valores exibidos na página de cadastro de contrato aditivo

(() => {
    const dataContrato = document.querySelector('[data-final-contrato]')
    const totalGlobal = document.querySelector('[data-valor-global]')

    const converterValor = (str) => {
        if(str.trim() != '')
            return Number.parseFloat(str
            .replace(/\D/g, '')
            .replace(/([0-9]+)(\d{2})/, '$1.$2'))
        else
            return 0.0
    }

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

    const atualizaCampoGlobal = () => {
        const totais = document.querySelectorAll('[data-total-item]')

        let totalAtual = 0.0

        totais.forEach((total) => {
            totalAtual += converterValor(total.value)
        })

        const vigencia = Number.parseInt(totalGlobal.getAttribute('data-valor-global'))
        const novoGlobal = new String((totalAtual * vigencia).toFixed(2))

        totalGlobal.value = novoGlobal
        totalGlobal.dispatchEvent(new Event('input'))
    }

    const inicializaTotais = () => {
        const totais = document.querySelectorAll('[data-total-item]')

        totais.forEach((total) => {
            total.addEventListener('input', atualizaCampoGlobal)
        })
    }

    const atualizaVigencia = () => {
        const dataInicial = new Date(dataContrato.min)
        const mesInicial = dataInicial.getMonth() + 1
        const anoInicial = dataInicial.getFullYear()


        const valorData = dataContrato.value
        const mesFinal = new Date(valorData).getMonth() + 1
        const anoFinal = new Date(valorData).getFullYear()

        let diferenca = mesFinal - mesInicial

        if(anoFinal - anoInicial > 0){
            diferenca += 12 * (anoFinal - anoInicial)
        }

        totalGlobal.setAttribute('data-valor-global', diferenca) 

        atualizaCampoGlobal()
    }

    dataContrato.addEventListener('input', atualizaVigencia)

    atualizaVigencia()
    atualizaCampoGlobal()
    inicializaTotais()
    inicializaTotaisItens()
})

()