// Script para controlar o comportamento do formulário de infraestrutura

(() => {
    // Funções para o comportamento de seleção do tipo de unidade
    // Função genérica para controlar a exibição de um elemento
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const selecaoEscola = document.querySelector('[data-selecao-escola]')
    const selecaoAdministrativa = document.querySelector('[data-selecao-administrativa]')

    const radioAdm = document.querySelector('[data-radio-adm]')
    const radioEscola = document.querySelector('[data-radio-escola]')

    const inicializaCampos = () => {
        const operador = radioEscola.checked

        controlaExibicao(selecaoEscola, operador)
        controlaExibicao(selecaoAdministrativa, !operador)
    }

    if(radioEscola && radioAdm){
        radioEscola.addEventListener('click', inicializaCampos)
        radioAdm.addEventListener('click', inicializaCampos)

        inicializaCampos()
    }

    // Funções para controlar a adição de Unidades consumidoras
    //Rastreando botão de adicionar
    const botaoAdicionar = document.querySelector('[data-adicionar-consumidora]')

    let contador = 2

    //Função para criar o elemento
    const FormularioGrupo =  (contador) => {
        const html = `
            <input class="campo-texto campo-pequeno" name="energia_eletrica${contador}" type="text">
            <button data-excluir-consumidora class="botao botao--vermelho">Excluir</button>
        `

        const div = document.createElement('div')
        div.innerHTML = html
        return div
    }

    const excluirCampo = (evento) => {
        evento.preventDefault()

        evento.target.parentElement.remove()
    }

    const inicializaBotoes = () => {
        const botoesExcluir = document.querySelectorAll('[data-excluir-consumidora]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluirCampo)
        })
    }

    inicializaBotoes()

    //Função para adicionar um campo
    const adicionarCampo = (evento) => {
        evento.preventDefault()

        const pai = evento.target.parentElement.parentElement
        pai.insertBefore(FormularioGrupo(contador), pai.lastElementChild)
        contador++

        inicializaBotoes()
    }

    botaoAdicionar.addEventListener('click', adicionarCampo)

})

()