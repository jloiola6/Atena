// Script para controlar a busca na página de Unidades Administrativas

(() => {
    const containerUnidades = document.querySelector('[data-container-unidades]')
    const containerBusca = document.querySelector('[data-container-busca]')

    const unidadesNomes = document.querySelectorAll('[data-busca-nome]')

    const campoNome = document.querySelector('[data-campo-nome]')

    const mensagemSemResultado = document.querySelector('[data-sem-resultado]')
    
    const controlaExibicaoContainer = (container, exibicao) => {
        if(exibicao)
            container.classList.remove('oculto')
        else
            container.classList.add('oculto')
    }

    const buscaPorNome = (evento) => {
        const campo = evento.target
        const texto = campo.value
        const textoVazio = texto.trim() == ''

        if(textoVazio){
            controlaExibicaoContainer(containerBusca, !textoVazio)
            controlaExibicaoContainer(mensagemSemResultado, !textoVazio)
            controlaExibicaoContainer(containerUnidades, textoVazio)
        }else{
            controlaExibicaoContainer(containerBusca, !textoVazio)
            controlaExibicaoContainer(containerUnidades, textoVazio)

            let resultados = 0

            unidadesNomes.forEach((unidade) => {
                const nome = unidade.getAttribute('data-busca-nome').toLocaleLowerCase()
                const valido = nome.includes(texto.toLocaleLowerCase())

                controlaExibicaoContainer(unidade, valido)
                
                if(valido)
                    resultados++

            })

            const semResultados = resultados == 0

            controlaExibicaoContainer(mensagemSemResultado, semResultados)

        }
    }

    campoNome.addEventListener('input', buscaPorNome)
})

()