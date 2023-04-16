(() => {
    const selecaoTipo = document.querySelector('[data-selecao-tipo]')
    const containers = document.querySelectorAll('[data-container]')
    
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    
    const controlaSelecao = () => {
        const opcaoSelecionada = selecaoTipo.options[selecaoTipo.selectedIndex]
        const atributoOpcao = opcaoSelecionada.dataset.opcao

        let atributoContainer

        containers.forEach((container) => {
            atributoContainer = container.dataset.container
            
            const validaExibicao = atributoOpcao == atributoContainer

            controlaExibicao(container, validaExibicao)
        })

    }

    controlaSelecao()
    selecaoTipo.addEventListener('input', controlaSelecao)



})

()