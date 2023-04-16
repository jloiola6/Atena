// Script para controlar a exibição de campos no modal de autorização de lotação

(() => {
    const selecoesStatus = document.querySelectorAll('[data-selecao-status]')

    const controlaCampos = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaMotivo = (evento) => {
        const selecao = evento.target
        const valor = selecao.value

        const form = selecao.parentElement.parentElement
        const campoMotivo = form.querySelector('[data-campo-motivo]')

        const validaMotivo = valor == '3'

        controlaCampos(campoMotivo, validaMotivo)
    }

    selecoesStatus.forEach((selecao) => {
        selecao.addEventListener('change', controlaMotivo)
    })
})

()