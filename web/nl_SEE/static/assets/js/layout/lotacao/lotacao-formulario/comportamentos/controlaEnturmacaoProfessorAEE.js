// Script para controlar a adição e exclusão de enturmações no formulário de lotação caso a função do servidor seja Professor(a) AEE

(() => {
    const containerEnturmacao = document.querySelector('[data-form-container="professor-aee"]')
    const botaoAdicionar = containerEnturmacao.querySelector('[data-botao-adicionar-turma]')

    let contadorTurma = 1

    // Função que retorna um container com uma nova seleção de turma
    const ContainerTurma = (contadorTurma) => {
        const div = document.createElement('div')


        const html = `
            <select id="campo-turma-escola${contadorTurma}" class="campo-texto campo-medio" name="turma_escola${contadorTurma}" data-selecao-turma></select>
            <button class="botao botao--vermelho" data-botao-excluir-turma>Excluir turma</button>
        `

        div.innerHTML = html

        const selecaoTurma = containerEnturmacao.querySelector('[data-selecao-turma]')
        const novaSelecao = div.querySelector('[data-selecao-turma]')

        novaSelecao.innerHTML = selecaoTurma.innerHTML

        return div
    }


    // Função que adiciona uma selecao de turma dentro de uma enturmação
    const adicionaSelecaoTurma = (evento) => {
        evento.preventDefault()
        const botao = evento.target
        const selecao = botao.previousElementSibling

        const contador = selecao.name.split('_')[1].replace('escolar', '')

        contadorTurma++

        const container = botao.parentElement
        const formularioGrupo = container.parentElement

        formularioGrupo.appendChild(ContainerTurma(contadorTurma, contador))

        inicializaBotoesExcluirTurma()
    }

    botaoAdicionar.addEventListener('click', adicionaSelecaoTurma)

    // Função que exclui uma selecao de turma dentro de uma enturmação
    const excluiTurma = (evento) => {
        evento.preventDefault()
        const botao = evento.target

        const container = botao.parentElement
        container.remove()
    }

    // Função para inicializar os botões de excluir uma seleção de turma dentro das enturmações
    const inicializaBotoesExcluirTurma = () => {
        const botoesExcluir = containerEnturmacao.querySelectorAll('[data-botao-excluir-turma]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiTurma)
        })
    }
})

()