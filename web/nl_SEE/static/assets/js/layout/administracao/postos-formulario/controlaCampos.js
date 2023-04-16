// Script para controlar a exibição de campos no formulário postos de trabalho

(() => {
    const selecaoEscola = document.querySelector('[data-selecao-escola]')
    const selecaoAdministrativa = document.querySelector('[data-selecao-administrativa]')

    const radiosUnidade = document.querySelectorAll('[data-radio-unidade]')
    const radioAdm = radiosUnidade[0]
    const radioEscola = radiosUnidade[1]

    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const inicializaCampos = () => {
        const operador = radioEscola.checked

        controlaExibicao(selecaoEscola, operador)
        controlaExibicao(selecaoAdministrativa, !operador)
    }

    radioEscola.addEventListener('click', inicializaCampos)
    radioAdm.addEventListener('click', inicializaCampos)

    inicializaCampos()
})

()