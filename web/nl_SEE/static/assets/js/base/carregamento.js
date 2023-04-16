(() => {
    const modalCarrregamento = document.querySelector('[data-modal-carregamento]')

    // Mostrando o modal de carregamento enquanto a página está carregando
    window.addEventListener('load', () => {
        modalCarrregamento.classList.add('oculto')
    })

    // const forms = document.querySelectorAll('form')

    // if(forms != null)
    //     forms.forEach((form) => {
    //         form.addEventListener('submit', () => {
    //             modalCarrregamento.classList.remove('oculto')
    //         }) 
    //     })
})

()

