// Script para controlar o comportamento do formulário de documentos
(() => {
    const selecaoCategoria = document.querySelector('[data-selecao-categoria]')

    const campoDescricao = document.querySelector('[data-campo-descricao]')
    const grupoDescricao = campoDescricao.parentElement

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaDescricao = () => {
        const valor = selecaoCategoria.value

        const validaValor = valor == 'Outros'

        controlaExibicao(grupoDescricao, validaValor)
        campoDescricao.required = validaValor
    }

    controlaDescricao()
    selecaoCategoria.addEventListener('change', controlaDescricao)
})

()