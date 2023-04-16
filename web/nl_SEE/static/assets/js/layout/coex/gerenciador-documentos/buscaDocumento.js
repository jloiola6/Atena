// Script para controlar a busca de documentos

(() => {

    // Inicializando os elementos utilizados para processar a busca
    const campoBusca = document.querySelector('[data-campo-busca]')

    const abasNav = document.querySelectorAll('[data-nav-aba]')

    const containersNav = document.querySelectorAll('[data-nav-container]')

    const mensagemSemResultado = document.querySelector('[data-sem-resultado]')

    // Função para limpar o campo de busca quando outra aba for selecionada
    const limpaCampo = () => {
        campoBusca.value = ''
        campoBusca.dispatchEvent(new Event('input'))
    }

    abasNav.forEach((aba) => {
        aba.addEventListener('click', limpaCampo)
    })

    // Função genérica para mudar a exibição de um container
    const controlaExibicaoContainer = (container, exibicao) => {
        if(exibicao)
            container.classList.remove('oculto')
        else
            container.classList.add('oculto')
    }

    // Função da busca
    const buscaPorNome = (evento) => {

        // Percorrendo os containers para realizar a busca somente no que está visível
        containersNav.forEach((container) => {
            if(!container.classList.contains('oculto')){
                const mensagemSemDoucumento = container.querySelector('[data-sem-documentos]')

                // Verificando se o container possui algum documento
                if(mensagemSemDoucumento == null){
                    const texto = evento.target.value
                    const textoVazio = texto.trim() == ''
                    
                    const containersResultados = container.querySelectorAll('[data-documento-resultado]')

                    if(textoVazio){
                        controlaExibicaoContainer(mensagemSemResultado, !textoVazio)

                        containersResultados.forEach((container) => {
                            controlaExibicaoContainer(container, textoVazio)
                        })
                    
                    }else{
                        let resultados = 0
                        containersResultados.forEach((container) => {
                            const nome = container.getAttribute('data-documento-resultado').toLowerCase()
                            const valido = nome.includes(texto.toLowerCase())

                            controlaExibicaoContainer(container, valido)

                            if(valido)
                                resultados++
                        })
                        
                        const semResultados = resultados == 0
    
                        controlaExibicaoContainer(mensagemSemResultado, semResultados)
                    }
                }
            }
                
        })
    }

    campoBusca.addEventListener('input', buscaPorNome)
})

()