(() => {
    // Script para controlar o cadastro de um ou mais alunos por Assistente Educaional AEE ou Mediador
    const selecaoTurma = document.querySelector('[data-selecao-turma-aee]')

    const botaoAvancarAlunosAEE = document.querySelector('[data-form-botao="alunos-aee"]')

    const container = document.querySelector('[data-form-container="alunos-aee"]')

    const mensagemSemAlunos = container.querySelector('[data-sem-alunos]')

    const formGrupoAlunos = container.querySelector('[data-grupo-alunos]')

    const botaoAdicionar = container.querySelector('[data-botao-adicionar-aluno]')
    const grupoAluno = botaoAdicionar.parentElement.parentElement

    const linkFormularioAluno = container.querySelector('[data-link-formulario-aluno]')

    let contadorAlunos = 1
    const MAXIMO_DE_ALUNOS = 5

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Funções para controlar o campo de adição de alunos já existentes
    const excluirAluno = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const div = botao.parentElement

        div.remove()

        const contadorDeSelecoes = document.querySelectorAll('[data-selecao-alunos]').length
        controlaExibicao(botaoAdicionar, !(contadorDeSelecoes == MAXIMO_DE_ALUNOS))
    }

    const BotaoExcluir = () => {
        const botao = document.createElement('button')
        botao.textContent = 'Excluir'

        botao.classList.add('botao')
        botao.classList.add('botao--vermelho')

        botao.toggleAttribute('data-botao-excluir')

        botao.addEventListener('click', excluirAluno)

        return botao
    }

    const adicionaAluno = (evento) => {
        evento.preventDefault()

        const divSelecaoAluno = botaoAdicionar.previousElementSibling

        const html = divSelecaoAluno.innerHTML

        const novoGrupo = document.createElement('div')
        novoGrupo.innerHTML = html
        novoGrupo.appendChild(BotaoExcluir())

        grupoAluno.appendChild(novoGrupo)
        contadorAlunos++

        const novaSelecao = novoGrupo.querySelector('select')
        novaSelecao.name = `mediador-aluno${contadorAlunos}`

        const contadorDeSelecoes = document.querySelectorAll('[data-selecao-alunos]').length

        controlaExibicao(botaoAdicionar, !(contadorDeSelecoes == MAXIMO_DE_ALUNOS))
    }

    botaoAdicionar.addEventListener('click', adicionaAluno)

    // Funções assíncronas para buscar os alunos de uma turma via API
    const getAlunos = async (id) => {
        if(id.includes(' '))
            return []

        const url = `${window.location.origin}/api/aluno/turma`

        try{
            const response = await fetch(`${url}/?id=${id}`)
            const json = await response.json()

            return json
        }catch(erro){
            console.log('Erro na requisição')
            console.log(`Detalhes: ${erro}`)
        }
    }

    const constroiListaAlunos = async (id) => {
        const dados = await getAlunos(id)

        const lista = dados.map(dado => [dado.aluno__id, dado.aluno__nome])
        return lista
    }

    const atualizaAlunos = async (evento) => {
        const id = selecaoTurma.value
        const alunos = await constroiListaAlunos(id)

        const listaVazia = alunos.length == 0

        const selecoesAlunos = container.querySelectorAll('[data-selecao-alunos]')

        selecoesAlunos.forEach((selecaoAlunos) => {
            selecaoAlunos.innerHTML = ''

            if(!listaVazia)
                alunos.forEach((aluno) => {
                    const opcao = document.createElement('option')
                    opcao.value = aluno[0]
                    opcao.textContent = aluno[1]

                    selecaoAlunos.appendChild(opcao)

                })
        })

        controlaExibicao(mensagemSemAlunos, listaVazia)
        controlaExibicao(formGrupoAlunos, !listaVazia)
    }

    botaoAvancarAlunosAEE.addEventListener('click', atualizaAlunos)
})

()