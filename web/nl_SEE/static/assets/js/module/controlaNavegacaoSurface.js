// Script utilziado para controlar a navagacao em abas e containers

(() => {
    const abas = document.querySelectorAll('[data-nav-aba]')
    const containers = document.querySelectorAll('[data-nav-container]')

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

    const inicializaAbas = () => {
        abas.forEach((aba) => {
            aba.addEventListener('click', () => {
                renicia()
                const atributo = aba.getAttribute('data-nav-aba')
                const container = document.querySelector(`[data-nav-container="${atributo}"]`)
                exibeContainer(container)
                ativaAba(aba, true)
            })
        })
    }

    inicializaAbas()
})

()