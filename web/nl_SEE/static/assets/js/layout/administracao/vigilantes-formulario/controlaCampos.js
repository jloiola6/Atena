// Script para controlar os campos do formulario de edição de contatos de uma unidade

const inicializaFormulario = () => {
    const botaoAdicionar = document.querySelector('[data-botao-adicionar]')

    let contador = document.querySelectorAll('.grupo-vigilante').length;

    const excluirContato = (evento) => {
        evento.preventDefault()
        evento.target.parentElement.remove()

        const quantidade = document.querySelectorAll('.grupo-vigilante').length

        if(quantidade < 3){
            botaoAdicionar.disabled = false
            inicializaBotoes()
        }
    }

    const FormularioGrupo = (contador) => {
        const divGrupo = document.createElement('div')
        divGrupo.classList.add('grupo-vigilante')

        const input = document.createElement('input')
        input.classList.add('campo-texto')
        input.classList.add('campo-grande')
        input.name = contador;
        input.placeholder = 'Ex: Érick Fernandes do Nascimento'
        input.autocomplete = 'off'
        input.required = 'true'

        const botaoExcluir = document.createElement('button')
        botaoExcluir.toggleAttribute('data-botao-excluir')
        botaoExcluir.classList.add('botao')
        botaoExcluir.classList.add('botao--vermelho')
        botaoExcluir.textContent = 'Exlcuir'
        botaoExcluir.addEventListener('click', excluirContato)

        divGrupo.appendChild(input)
        divGrupo.appendChild(botaoExcluir)

        return divGrupo
    }

    const adicionarContato = (evento) => {
        evento.preventDefault()

        const quantidade = document.querySelectorAll('.grupo-vigilante').length

        if(quantidade < 3){
            const containerContatos = evento.target.parentElement.parentElement
            containerContatos.insertBefore(FormularioGrupo(contador), containerContatos.lastElementChild)
            contador++
        }

        if(quantidade == 2){
            botaoAdicionar.disabled = true
        }

    }


    const inicializaBotoes = () => {
        const botoesExcluir = document.querySelectorAll('[data-botao-excluir]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluirContato)
        })

        botaoAdicionar.addEventListener('click', adicionarContato)
    }

    inicializaBotoes()
}

inicializaFormulario()