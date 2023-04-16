// Script para controlar a adição de alunos na seleção do formulário de lotação
(() => {
    const container = document.querySelector('[data-form-container="alunos-aee"]')

    const mensagemSemAlunos = container.querySelector('[data-sem-alunos]')

    const formGrupoAlunos = container.querySelector('[data-grupo-alunos]')

    const linkFormularioAluno = container.querySelector('[data-link-formulario-aluno]')

    let contador = 1

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const abrirModalAluno = (evento) => {
        const modal = ModalNovoAluno(contador)

        const botaoCancelar = modal.querySelector('[data-cancelar-aluno]')
        botaoCancelar.addEventListener('click', fechaModalAluno)
    
        const botaoSalvar = modal.querySelector('[data-salvar-aluno]')
        botaoSalvar.addEventListener('click', adicionaAluno)

        container.appendChild(modal)

        contador++
    }

    linkFormularioAluno.addEventListener('click', abrirModalAluno)

    const adicionaAluno = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const modal = botao.parentElement.parentElement.parentElement

        const campoNome = modal.querySelector('#campo-nome-aluno')
        const nome = campoNome.value

        adicionaOpcaoAluno(nome)

        const grupoOculto = formGrupoAlunos.classList.contains('oculto')

        if(grupoOculto){
            controlaExibicao(formGrupoAlunos, grupoOculto)
            controlaExibicao(mensagemSemAlunos, !grupoOculto)
        }


        modal.classList.add('oculto')
    }

    // Função que adiciona o aluno preenchido no modal nas opções das seleções
    const adicionaOpcaoAluno = (valor) => {
        const html = `
            <option value="novo_aluno${contador}">${valor}</option>
        `

        const selecoesAlunos = container.querySelectorAll('[data-selecao-alunos]')

        let auxValor

        selecoesAlunos.forEach((selecao) => {
            auxValor = selecao.value
            selecao.innerHTML += html
            selecao.value = auxValor
        })

    }

    const fechaModalAluno = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const modal = botao.parentElement.parentElement.parentElement

        modal.remove()

        contador--
    }
})

()