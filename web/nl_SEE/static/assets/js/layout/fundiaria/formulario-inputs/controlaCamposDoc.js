(() => {
    const containerPai = document.querySelector('[data-container-inputs-doc]')

    let contador = 1;

    const FormularioGrupo = (contador) => {
        const html = `
            <div>
                <input class="campo-arquivo" id="arquivo" type="file" name="arquivo${contador}" required>
                <button class="botao botao--vermelho" data-botao-excluir>Excluir</button>
            </div>
        `

        const div = document.createElement('div')
        div.innerHTML = html
        div.classList.add('formulario-grupo')

        return div
    }

    // Funções para manipular a criação de novos campos de contato
    const excluirContato = (evento) => {
        evento.preventDefault()
        evento.target.parentElement.parentElement.remove()
    }

    const adicionarContato = (evento) => {
        evento.preventDefault()
        containerPai.appendChild(FormularioGrupo(contador))
        inicializaBotoes()
        contador++;
    }

    const inicializaBotoes = () => {
        const botoesExcluir = document.querySelectorAll('[data-botao-excluir]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluirContato)
        })

        const botoesAdicionar = document.querySelectorAll('[data-botao-adicionar]')

        botoesAdicionar.forEach((botao) => {
            botao.addEventListener('click', adicionarContato)
        })
    }

    inicializaBotoes()
})

()