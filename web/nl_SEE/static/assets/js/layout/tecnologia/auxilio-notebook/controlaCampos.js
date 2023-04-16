// Script para controlar o comportamento dos campos no modal de detalhes do auxilio notebook

(() => {
    const selecaoTipo = document.querySelectorAll('[data-selecao-situacao]')
    const divCampos = document.querySelector('[data-selecao-motivo]')


    // Função genérica para controlar a exibição dos elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaTipo = () => {
        const valor = selecaoTipo.value


        // Comportamento para caso a situaçao seja reprovado
        const validaSituacao = valor == 'R'
        console.log(validaSituacao);
        controlaExibicao(divCampos, validaSituacao)
    }
    

    controlaTipo()
    selecaoTipo.addEventListener('change', controlaTipo)
})

()