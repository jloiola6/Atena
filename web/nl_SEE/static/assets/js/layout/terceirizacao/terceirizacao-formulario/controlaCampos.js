// Script para controlar a exibição de campos no formulário de lotação

(() => {
    const vigilanciadiv = document.querySelector('[data-vigilancia]')
    const postodiv = document.querySelector('[data-posto]')

    const radiocontrato = document.querySelectorAll('[data-radio-contrato]')
    const radioposto = radiocontrato[0]
    const radiovigilancia = radiocontrato[1]
    
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

    const inicializadivs = () => {
        const operador = radiovigilancia.checked

        controlaExibicao(vigilanciadiv, operador)
        controlaExibicao(postodiv, !operador)
    }

    radioEscola.addEventListener('click', inicializaCampos)
    radioAdm.addEventListener('click', inicializaCampos)

    radiovigilancia.addEventListener('click', inicializadivs)
    radioposto.addEventListener('click', inicializadivs)

    inicializadivs()
    inicializaCampos()
})


()