(() => {
    // Função genérica para controlar a exibição de um elemento
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Funções para o comportamento de seleção de ocupacao
    const selecaoConvenio = document.querySelector('[data-selecao-convenio]')
    const selecaoOcupacao = document.querySelector('[data-selecao-ocupacao]')

    const inicializaOcupacao = () => {
        const Ocupacao = selecaoOcupacao.value == 'Cedido'

        controlaExibicao(selecaoConvenio, Ocupacao)
    }

    inicializaOcupacao()

    selecaoOcupacao.addEventListener('input', inicializaOcupacao)

})

()