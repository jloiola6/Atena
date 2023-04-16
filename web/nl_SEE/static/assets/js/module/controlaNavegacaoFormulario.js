// Script utilziado para controlar a navagacao em abas e containers em formularios

(() => {
    const abas = document.querySelectorAll('[data-form-aba]')
    const containers = document.querySelectorAll('[data-form-container]')
    const botoes = document.querySelectorAll('[data-form-botao]')

    const ativaAba = (aba, ativacao) => {
        if(ativacao)
            aba.classList.add("navegacao-surface-item-ativo");
        else
            aba.classList.remove("navegacao-surface-item-ativo");
    }

    const renicia = () => {
        abas.forEach((aba) => {
            ativaAba(aba, false)
        })

        containers.forEach((container) => {
            container.classList.add('oculto')
        })
    }

    const exibeContainer = (container) => {
        container.classList.remove('oculto')
    }

    const inicializaBotoes = () => {
        botoes.forEach((botao) => {
            botao.addEventListener('click', (evento) => {
                evento.preventDefault()
                renicia()
                const atributo = botao.getAttribute('data-form-botao')
                const container = document.querySelector(`[data-form-container="${atributo}"]`)
                const aba = document.querySelector(`[data-form-aba="${atributo}"]`)
                exibeContainer(container)
                ativaAba(aba, true)
            })
        })
    }

    inicializaBotoes()
})

()