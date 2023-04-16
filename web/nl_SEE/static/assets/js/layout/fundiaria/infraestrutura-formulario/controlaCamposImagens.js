// Script para controlar os inputs de imagens
(() => {
    // Inicializando os botoes de exclusão
    const botoesExcluir = document.querySelectorAll('[data-excluir-imagem]')

    const excluiContainer = (evento) => {
        evento.preventDefault()
        const botao = evento.target
        const pai = botao.parentElement

        pai.remove()
    }

    const adicionaContainer = (evento) => {
        const botao = evento.target
        const tipo = botao.dataset.excluirImagem

        let container

        // if(tipo == 'Frente')
        //     container = document.querySelector('[data-div-frente]')
        // else
        //     container = document.querySelector('[data-div-aerea]')

        container = document.querySelector('[data-div-frente]')

        container.classList.add('formulario-grupo')
        container.innerHTML = FormularioGrupo()
    }

    if(botoesExcluir != null){
        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiContainer)
            botao.addEventListener('click', adicionaContainer)
        })
    }
    
    const FormularioGrupo = (tipo) => {

        // let name

        // if(tipo == 'Frente')
        //     name = 'arquivo1'
        // else
        //     name = 'arquivo2'

        // const html = `
        //     <label class="texto-azul label-campo" for="arquivo">Insira imagem (${tipo})</label>
        //     <input class="campo-arquivo" id="arquivo" type="file" accept=".png, .jpeg, .jpg" name="${name}" required>
        // `
        const html = `
            <label class="texto-azul label-campo" for="arquivo">Insira imagem (Frente)</label>
            <input class="campo-arquivo" id="arquivo" type="file" accept=".png, .jpeg, .jpg" name="arquivo1" required>
            <label class="texto-azul label-campo" for="arquivo">Insira imagem (Aérea)</label>
            <input class="campo-arquivo" id="arquivo" type="file" accept=".png, .jpeg, .jpg" name="arquivo2" required>
        `

        return html
    }
})

()