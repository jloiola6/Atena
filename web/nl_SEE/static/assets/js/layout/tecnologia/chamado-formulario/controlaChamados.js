(() => {
    const formContainerChamado = document.querySelector('[data-form-container="chamado"]')
    const containerChamado = formContainerChamado.querySelector('[data-container-chamado]')

    const botaoAdicionarChamado = formContainerChamado.querySelector('[data-adicionar-chamado]')
    const containerBotao = botaoAdicionarChamado.parentElement

    let contadorChamados = 1

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const ContainerChamado = (contador) => {
        const div = document.createElement('div')

        const html = containerChamado.innerHTML

        div.innerHTML = html.replaceAll('1', contador)

        div.innerHTML += `
            <div class="container-botoes">
                <button class="botao botao--vermelho" data-excluir-chamado>Excluir Chamado</button>
            </div>
        `

        return div
    }

    const adicionaChamado = (evento) => {
        evento.preventDefault()

        contadorChamados++

        const hr = document.createElement('hr')
        hr.classList.add('formulario-grupo')

        formContainerChamado.insertBefore(hr, containerBotao)

        const div = ContainerChamado(contadorChamados)

        formContainerChamado.insertBefore(div, containerBotao)

        inicializaBotoesExcluirChamado()
        inicializaSelecoesServico()
    }

    botaoAdicionarChamado.addEventListener('click', adicionaChamado)

    const excluiChamado = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const container = botao.parentElement.parentElement
        const hr = container.previousElementSibling

        hr.remove()
        container.remove()
    }

    const inicializaBotoesExcluirChamado = () => {
        const botoesExcluir = formContainerChamado.querySelectorAll('[data-excluir-chamado]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiChamado)
        })
    }

    const controlaSerivcos = (selecao) => {
        const tipoSelecionado = selecao.value
        const containerPai = selecao.parentElement.parentElement
        const selecoesServico = containerPai.querySelectorAll('[data-selecao-servico]')

        selecoesServico.forEach((selecaoServico) => {
            const atributo = selecaoServico.dataset.selecaoServico

            controlaExibicao(selecaoServico, atributo == tipoSelecionado)
        })
    }

    const inicializaSelecoesServico = () => {
        const selecoesTipoServico = formContainerChamado.querySelectorAll('[data-selecao-tipo-servico]')

        selecoesTipoServico.forEach((selecao) => {
            controlaSerivcos(selecao)

            selecao.addEventListener('change', () => {
                controlaSerivcos(selecao)
            })
        })
    }

    inicializaSelecoesServico()

})

()