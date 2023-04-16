// Script para controlar o comportamento do formulário de contrato aditivo

import {inicializaCampos} from '../../../module/mascaras.js'

(() => {
    // Recebendo o tipo de contrato
    const tipoContrato = document.querySelector('[data-contrato-tipo]').getAttribute('data-contrato-tipo')
    // console.log(tipoContrato)

    // Recebendo o tipo de aditivo
    const tipoAditivo = document.querySelector('[data-aditivo-tipo]').getAttribute('data-aditivo-tipo')
    // console.log(tipoAditivo)

    // Carregando o elemento de seleção da data do atitivo
    const dataAditivo = document.querySelector('[data-final-contrato]')

    // Carregando o elemento de valor global do aditivo
    const campoGlobal = document.querySelector('[data-valor-global]')

    // Carregando o input oculto de vigencia
    const campoVigencia = document.querySelector('[data-contrato-vigencia]')

    // Função que recebe uma String em formato de moeda e converte em um Float
    const converterValor = (str) => {
        if(str.trim() != '')
            return Number.parseFloat(str
            .replace(/\D/g, '')
            .replace(/([0-9]+)(\d{2})/, '$1.$2'))
        else
            return 0.0
    }

    // Função para atualizar o total de um item de acordo com a quantidade e valor digitados
    const atualizaTotalItem = (evento) => {
        const pai = evento.target.parentElement.parentElement.parentElement

        const campoQtd = pai.querySelector('[data-qtd-item]')
        const campoUnitario = pai.querySelector('[data-unitario-item]')
        const campoTotal = pai.querySelector('[data-total-item]')

        if(tipoContrato != 'Postos de trabalho - Limpeza'){
            const qtd = Number.parseInt(campoQtd.value)
            const valorUnitario = converterValor(campoUnitario.value)

            const novoValor = qtd * valorUnitario

            campoTotal.value = novoValor.toFixed(2)
            campoTotal.dispatchEvent(new Event('input'))
        }else{
            // Cálculo do valor total do item
            const campoMetragemContratada = pai.querySelector('[data-metragem-contratada]')
            const campoMetragemMensal = pai.querySelector('[data-metragem-item]')
            
            const metragem = Number.parseInt(campoMetragemMensal.value)
            const valor = converterValor(campoUnitario.value)

            const novoValor = metragem * valor
            
            campoTotal.value = novoValor.toFixed(2)
            campoTotal.dispatchEvent(new Event('input'))

            // Cálculo da quantidade do item
            const metragemContratada = Number.parseInt(campoMetragemContratada.value)

            let novaQtd = metragem / metragemContratada

            if(isNaN(novaQtd))
                novaQtd = 0

            campoQtd.value = novaQtd.toFixed(2)
        }
    }

    // Inicializando os campos necessários para a atualização de total de itens
    const unitarios = document.querySelectorAll('[data-unitario-item]')

    unitarios.forEach((unitario) => {
        unitario.addEventListener('input', atualizaTotalItem)
    })

    if(tipoContrato != 'Postos de trabalho - Limpeza'){
        const quantidades = document.querySelectorAll('[data-qtd-item]')

        quantidades.forEach((quantidade) => {
            quantidade.addEventListener('input', atualizaTotalItem)
        })
    }else{
        const metragens = document.querySelectorAll('[data-metragem-item]')

        metragens.forEach((metragem) => {
            metragem.addEventListener('input', atualizaTotalItem)
        })
    }

    // Função para atualziar o valor global do contrato de acordo com os totais dos itens e a vigencia
    const atualizaGlobal = () => {
        const totais = document.querySelectorAll('[data-total-item]')
        
        let totalAtual = 0.0

        // Percorrendo os grupos de campos para recolher os valores de totais dos itens
        totais.forEach((total) => {
            // Verificando se o item está ativo
            const pai = total.parentElement.parentElement.parentElement

            const radioAtivo = pai.querySelector('[data-radio-ativo]')

            if(radioAtivo != null && radioAtivo.checked )
                totalAtual += converterValor(total.value)
        })

        const vigencia = Number.parseInt(campoVigencia.value)
        const novoGlobal = new String((totalAtual * vigencia).toFixed(2))

        campoGlobal.value = novoGlobal
        campoGlobal.dispatchEvent(new Event('input'))
    }

    // Inicializando os campos de totais
    const totais = document.querySelectorAll('[data-total-item]')

    totais.forEach((total) => {
        total.addEventListener('input', atualizaGlobal)
    })


    // Função para calcular a vigência do aditivo
    const atualizaVigencia = () => {
        let mesInicial, anoInicial
        let mesFinal, anoFinal
        let vigencia

        // Verificação do tipo de aditivo para o calculo da vigencia
        if(tipoAditivo == 'Aditivo'){
            mesInicial = new Date(dataAditivo.min).getMonth() + 1
            anoInicial = new Date(dataAditivo.min).getFullYear()

            mesFinal = new Date(dataAditivo.value).getMonth() + 1
            anoFinal = new Date(dataAditivo.value).getFullYear()
        }else{
            mesInicial = new Date(dataAditivo.value).getMonth() + 1
            anoInicial = new Date(dataAditivo.value).getFullYear()

            mesFinal = new Date(dataAditivo.max).getMonth() + 1
            anoFinal = new Date(dataAditivo.max).getFullYear()
        }

        vigencia = mesFinal - mesInicial

        if(anoFinal - anoInicial > 0)
            vigencia += 12 * (anoFinal - anoInicial)

        campoVigencia.value = vigencia

        // console.log(mesInicial, anoInicial, mesFinal, anoFinal, 'V: '+vigencia)
        atualizaGlobal()
    }

    atualizaVigencia()
    dataAditivo.addEventListener('input', atualizaVigencia)

    // Função para inativar um item desativando o seu grupo de campos
    const intativaItem = (evento) => {
        // Retirando o radio de ativação
        const fieldset = evento.target.parentElement

        const radioAtivar = fieldset.querySelector('[data-radio-ativo]')
        const labelAtivar = fieldset.querySelector('[data-label-ativo]')

        if(radioAtivar != null && labelAtivar != null){
            radioAtivar.remove()
            labelAtivar.remove()  
        }
        
        // Percorrendo o grupo de campos para desabilitá-los
        const pai = evento.target.parentElement.parentElement.parentElement.parentElement

        const inputs = pai.querySelectorAll('input')

        inputs.forEach((input) => {
            input.readOnly = true
        })

        atualizaGlobal()
    }

    // Inicializando os radios de inativação
    const radiosInativar = document.querySelectorAll('[data-inativar-item]')

    if(radiosInativar != null)
        radiosInativar.forEach((radio) => {
            radio.addEventListener('click', intativaItem)
        })
})

()