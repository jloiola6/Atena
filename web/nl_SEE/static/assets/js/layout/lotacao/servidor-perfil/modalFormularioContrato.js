// Script para controlar o comportamento do modal que encaminha para o formulário de cadastro de contrato
(() => {
    const selecaoTipoContrato = document.querySelector('[data-selecao-tipo]')
    const grupoCargo = document.querySelector('[data-grupo-cargo]')
    const selecoesCargo = document.querySelectorAll('[data-cargo]')

    // Função genérica para controlar a exibição de elementos na tela
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaTipoContrato = () => {
        const tipoSelecionado = selecaoTipoContrato.value
        const validaCargo = tipoSelecionado != 'ESTAGIÁRIO'

        controlaExibicao(grupoCargo, validaCargo)

        selecoesCargo.forEach((selecao) => {
            const atributo = selecao.getAttribute('data-cargo')

            controlaExibicao(selecao, atributo == tipoSelecionado)
        })

    }

    controlaTipoContrato()
    selecaoTipoContrato.addEventListener('change', controlaTipoContrato)
})

()