// Controle do tema exibido
(() => {
    const botaoTema = document.querySelector('[data-tema]')

    const iconeModoPadrao = document.querySelector('[data-icone-padrao]')
    const iconeModoEscuro = document.querySelector('[data-icone-escuro]')

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
        elemento.classList.remove('oculto')
        else
        elemento.classList.add('oculto')
    }

    // Funções para acessar o tema armazenadono Local Storage
    const getTema = () => {
        return localStorage.tema
    }

    const setTema = (tema) => {
        localStorage.tema = tema
    }

    // Função que troca o tema quando o botão é clicado
    const trocaTema = () => {
        const body = document.body
        const atributo = botaoTema.getAttribute('data-tema')

        const validaPadrao = atributo == 'padrao'

        controlaExibicao(iconeModoEscuro, validaPadrao)
        controlaExibicao(iconeModoPadrao, !validaPadrao)

        if(validaPadrao){
            setTema('padrao')

            botaoTema.setAttribute('data-tema', 'escuro')
            body.classList.remove('modo-escuro')
        }else{
            setTema('escuro')

            botaoTema.setAttribute('data-tema', 'padrao')
            body.classList.add('modo-escuro')
        }
    }

    const inicializaBotao = () => {
        botaoTema.addEventListener('click', trocaTema)
    }

    //Função que inicializa o tema como padrao em caso de primeiro acesso
    const inicializaTema = () => {
        if(localStorage['tema'] == null)
            localStorage.setItem('tema', 'padrao')
    }

    const carregaTema = () => {
        inicializaTema()
        inicializaBotao()

        const body = document.body
        const tema = getTema()

        const validaPadrao = tema == 'padrao'

        controlaExibicao(iconeModoEscuro, validaPadrao)
        controlaExibicao(iconeModoPadrao, !validaPadrao)

        if(validaPadrao){
            botaoTema.setAttribute('data-tema', 'escuro')
            body.classList.remove('modo-escuro')
        }else{
            botaoTema.setAttribute('data-tema', 'padrao')
            body.classList.add('modo-escuro')
        }
    }

    carregaTema()
})

()