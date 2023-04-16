// Script para controlar o comportamento dos campos no modal de detalhes do auxilio notebook

(() => {
    const selecoesSituacao = document.querySelectorAll('[data-selecao-situacao]')
    
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }


    const exibeMotivo = (evento) => {
        const selecao = evento.target
        const valor = selecao.value 

        const formulario = selecao.parentElement.parentElement

        const grupoMotivo = formulario.querySelector('[data-grupo-motivo]')

        controlaExibicao(grupoMotivo, valor == 'R')
    }


    selecoesSituacao.forEach((selecao) => {
        selecao.addEventListener('change', exibeMotivo)
    })
})

()