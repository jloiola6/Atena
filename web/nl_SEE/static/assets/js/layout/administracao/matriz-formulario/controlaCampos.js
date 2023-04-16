(() => {
    const containerDisciplina = document.querySelector('[data-container-disciplina]')
    const grupoDisciplina = containerDisciplina.parentElement

    const selecaoDisciplina = document.querySelector('[data-selecao-disciplina]')

    const campoCh = document.querySelector('[data-campo-ch]')

    const botaoAdicionar = document.querySelector('[data-botao-adicionar]')

    let contador = 1

    const removeDisciplina = (evento) => {
        const botao = evento.target

        const pai = botao.parentElement
        pai.remove()
    }

    const adicionarDisciplina = () => {
        contador++

        const novoCampoDisciplina = selecaoDisciplina.cloneNode(true)

        novoCampoDisciplina.setAttribute('name', `disciplina${contador}`)
        novoCampoDisciplina.setAttribute('data-selecao-disciplina', contador)

        const novoCampoCh = campoCh.cloneNode()

        novoCampoCh.setAttribute('name', `ch${contador}`)
        novoCampoCh.setAttribute('data-campo-ch', contador)

        const botaoRemover = document.createElement('button')
        botaoRemover.textContent = 'Remover'
        botaoRemover.classList.add('botao')
        botaoRemover.classList.add('botao--vermelho')
        botaoRemover.type = 'button'

        botaoRemover.addEventListener('click', removeDisciplina)
        botaoRemover.setAttribute('data-remover-disciplina', `${contador}`)

        const novoContainer = document.createElement('div')
        novoContainer.classList.add('formulario-grupo--disciplina')
        novoContainer.appendChild(novoCampoDisciplina)
        novoContainer.appendChild(novoCampoCh)
        novoContainer.appendChild(botaoRemover)


        grupoDisciplina.appendChild(novoContainer)
    }

    botaoAdicionar.addEventListener('click', adicionarDisciplina)

})

()