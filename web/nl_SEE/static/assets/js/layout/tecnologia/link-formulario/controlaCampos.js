// Script para controlar a exibição de campos no formulário de Cadastro e Edição de links

(() => {
    // Função genérica para controlar a exibição de um elemento
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Funções para o comportamento de seleção de fornecedor
    const selecaoItem = document.querySelector('[data-selecao-item]')
    const selecaoFornecedor = document.querySelector('[data-selecao-fornecedor]')

    const inicializaFornecedor = () => {
        const fornecedorSEE = selecaoFornecedor.value == 'SEE'

        controlaExibicao(selecaoItem, fornecedorSEE)
    }

    inicializaFornecedor()

    selecaoFornecedor.addEventListener('input', inicializaFornecedor)

    // Funções para o comportamento de seleção do tipo de unidade
    const selecaoEscola = document.querySelector('[data-selecao-escola]')
    const selecaoAdministrativa = document.querySelector('[data-selecao-administrativa]')

    const radioAdm = document.querySelector('[data-radio-adm]')
    const radioEscola = document.querySelector('[data-radio-escola]')

    const inicializaCampos = () => {
        const operador = radioEscola.checked

        controlaExibicao(selecaoEscola, operador)
        controlaExibicao(selecaoAdministrativa, !operador)
    }

    radioEscola.addEventListener('click', inicializaCampos)
    radioAdm.addEventListener('click', inicializaCampos)

    inicializaCampos()


    // Criando o elemento para inserção de campos de IP Firewall
    const containerFirewall = document.querySelector('[data-container-firewall]')
    let contador = 1

    const FormularioGrupo = (contador) => {
        const html = `
            <input type="text" class="campo-texto campo-pequeno" id="campo-firewall" name="ipfirewall${contador}" placeholder= 'Ex: 127.0.0.1'>
            <button class="botao botao--vermelho" data-botao-excluir>Excluir</button>
        `

        const div = document.createElement('div')
        div.innerHTML = html

        return div
    }

    // Funções para manipular a criação de novos campos de IP Firewall
    const excluirCampoFirewall = (evento) => {
        evento.preventDefault()
        evento.target.parentElement.remove()
    }

    const adicionarCampoFirewall = (evento) => {
        evento.preventDefault()
        containerFirewall.insertBefore(FormularioGrupo(contador), containerFirewall.lastElementChild)
        inicializaBotoes()
        contador++
    }

    const inicializaBotoes = () => {
        const botoesExcluir = document.querySelectorAll('[data-botao-excluir]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluirCampoFirewall)
        })

        const botaoAdicionar = document.querySelector('[data-botao-adicionar]')
        botaoAdicionar.addEventListener('click', adicionarCampoFirewall)
    }

    inicializaBotoes()
})

()