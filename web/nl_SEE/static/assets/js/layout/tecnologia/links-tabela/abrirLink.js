// Script para entrar em um perfil de um link ao clicar na tabela

(() => {
    const abreLink = (id) => {
        let link = null

        link = `link_perfil?id=${id}`

        if (link != null)
            window.location.href = link
        else
            console.log("Link inválido")
    }

    const inicializaLinhas = () => {
        const linhas = document.querySelectorAll('[data-link-id]')

        linhas.forEach((linha) => {
            const id = linha.getAttribute('data-link-id')

            linha.addEventListener('click', () => { abreLink(id) })
        })

    }

    inicializaLinhas()
})

()