(() => {

    // if(document.querySelector('[data-tabela-link]') != null){
    //     const linkTabela = document.querySelector('[data-tabela-link]').getAttribute('data-tabela-link')
    //     const linhas = document.querySelectorAll('[data-tabela-link-chave]')
        
    //     linhas.forEach((linha) => {
    //         const linkLinha = linha.getAttribute('data-tabela-link-chave')
    //         linha.addEventListener('click', () => {
                
    //             window.location.href = linkTabela.concat(linkLinha)
    //         })
    //     })
    // }

    if(document.querySelector('[data-tabela-link]') != null){
        const linhasLinkadas = document.querySelectorAll('[data-tabela-link-chave]')

        linhasLinkadas.forEach((linha) => {
            const linkLinha = linha.getAttribute('data-tabela-link-chave')
            const linkTabela = linha.parentElement.getAttribute('data-tabela-link')

            if(linkTabela != null)
                linha.addEventListener('click', () => {window.location.href = linkTabela.concat(linkLinha)})
        })
    }
})

()