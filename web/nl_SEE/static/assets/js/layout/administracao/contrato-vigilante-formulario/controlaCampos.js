// Script para controlar os campos do formulario de contratos

import {inicializaCampos} from '../../../module/mascaras.js'
import {FormularioGrupo} from './FormularioGrupo.js'

(() => {
    // Função genérica para converter o valor de montetário para um float
    const converteValor = (str) => {
        if(str.trim() != '')
            return Number.parseFloat(str
            .replace(/\D/g, '')
            .replace(/([0-9]+)(\d{2})/, '$1.$2'))
        else
            return 0.0
    }

    // Controlando a navegação do formulário de acordo com a seleção de uma data
    const inicializaNavegacao = () => {
        const controlaBotaoAvancar = document.querySelector('[data-form-botao="itens"]')
        const dataInicioVigencia = document.querySelector('[data-inicio-vigencia]')
        const dataTerminoVigencia = document.querySelector('[data-termino-vigencia]')

        // Habilita o campo de termino da vigência de acordo com a data selecionada no campo de início
        const inicializaDataTermino = () => {
            dataTerminoVigencia.disabled = dataInicioVigencia.value.length == 0 
            dataTerminoVigencia.value = dataInicioVigencia.value
            dataTerminoVigencia.min = dataInicioVigencia.value
        }

        // Inicializa o atributo no campo de valor global de acordo com as datas selecionadas
        const verificaDatas = () => {
            const dataInicio = dataInicioVigencia.value
            const dataFim = dataTerminoVigencia.value

            const verificacaoStrings = dataInicio.trim() != '' && dataFim.trim() != ''

            controlaBotaoAvancar.disabled = !verificacaoStrings

            if(verificacaoStrings){
                const inicioDate = new Date(dataInicio)
                const fimDate = new Date(dataFim)

                const anoInicio = inicioDate.getFullYear()
                const anoFim = fimDate.getFullYear()

                const mesInicio = inicioDate.getMonth() + 1
                const mesFim = fimDate.getMonth() + 1

                let diferenca = mesFim - mesInicio

                if(anoFim - anoInicio > 0){
                    diferenca += 12 * (anoFim - anoInicio)
                }
                    
                document.querySelector('[data-global-contrato]').setAttribute('data-global-contrato', diferenca)

                const totais = document.querySelectorAll('[data-total-item]')
        
                totais.forEach((total) => {
                    total.dispatchEvent(new Event('input'))
                })

                document.querySelector('[data-campo-vigencia]').value = diferenca
            }
        }

        dataInicioVigencia.addEventListener('input', inicializaDataTermino)
        dataInicioVigencia.addEventListener('input', verificaDatas)
        dataTerminoVigencia.addEventListener('input', verificaDatas)
    }

    inicializaNavegacao()
    
    // Atualiza o total de um item de acordo com os valores inseridos
    const atualizaTotalItem = (evento) => {
        const pai = evento.target.parentElement.parentElement

        const grupoQtd = pai.children[2]
        const campoQtd = grupoQtd.lastElementChild

        const grupoUnitario = pai.children[4]
        const campoUnitario = grupoUnitario.lastElementChild

        const grupoTotal = pai.children[5]
        const campoTotal = grupoTotal.lastElementChild

        // Cálculo do valor total do item
        const qtd = Number.parseFloat(campoQtd.value)
        const valor = converteValor(campoUnitario.value)

        const novoValor = qtd * valor
        
        campoTotal.value = novoValor.toFixed(2)
        campoTotal.dispatchEvent(new Event('input'))

    }

    // Inicializa os campos dos itens
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

    const totalContrato = document.querySelector('[data-total-contrato]')
    
    // Atualiza o total do contrato de acordo com os totais dos itens
    const atualizaTotalContrato = (evento) => {
        const campo = evento.target
        const valor = converteValor(campo.value)

        const totais = document.querySelectorAll('[data-total-item]')

        let totalAtual = 0.0

        totais.forEach((total) => {
            if(total !== campo){
                const valor = converteValor(total.value)
                totalAtual += valor
            }
        })

        const novoTotal = new String((totalAtual + valor).toFixed(2))

        totalContrato.value = novoTotal
        totalContrato.dispatchEvent(new Event('input'))

        const campoGlobal = document.querySelector('[data-global-contrato]')
        const vigencia = Number.parseInt(campoGlobal.getAttribute('data-global-contrato'))

        const novoGlobal = new String ((vigencia * (totalAtual + valor)).toFixed(2))

        campoGlobal.value = novoGlobal
        campoGlobal.dispatchEvent(new Event('input'))
    }

    // Inicializa os campos de total dos itens com a função de atualização
    const inicializaTotais = () => {
        const totais = document.querySelectorAll('[data-total-item]')
        
        totais.forEach((total) => {
            total.addEventListener('input', atualizaTotalContrato)
        })
    }

    const inicializaCamposItem = () => {
        let contador = 2

        const excluiItem = (evento) => {
            evento.preventDefault()
            evento.target.parentElement.parentElement.remove()
        }

        const adicionaItem = (evento) => {
            evento.preventDefault()

            const containerItens = evento.target.parentElement.parentElement

            containerItens.insertBefore(FormularioGrupo(contador), containerItens.lastElementChild)
            contador++

            inicializaCampos()
            inicializaTotais()
            inicializaTotaisItens()
            inicializaBotoes()
        }

        const inicializaBotoes = () => {
            const botaoAdicionar = document.querySelector('[data-botao-adicionar-item]')
            botaoAdicionar.addEventListener('click', adicionaItem)

            const botoesExcluir = document.querySelectorAll('[data-botao-excluir-item]')

            botoesExcluir.forEach((botao) => {
                botao.addEventListener('click', excluiItem)
            })
        }

        inicializaBotoes()
    }
    
    inicializaCamposItem()
    inicializaTotais()
    inicializaTotaisItens()
})

()