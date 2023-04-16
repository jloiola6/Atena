(() => {
    const selecaoTipo = document.querySelector('[data-selecao-tipo-contrato]')
    const aplicacao = selecaoTipo.getAttribute('data-selecao-tipo-contrato')

    let strAplicacao

    switch (aplicacao) {
        case 'Administração':
            strAplicacao = 'administracao'
            break

        case 'Tecnologia':
            strAplicacao = 'tecnologia'
            break

        case 'Terceirização':
            strAplicacao = 'terceirizacao'
            break
    }

    const inicializaLink = () => {
        const tipo = selecaoTipo.value

        let link = `/${strAplicacao}/contrato-aditivo-formulario?tipo=${tipo}`

        const a = document.querySelector('[data-link-form-contrato]')
        a.href = link
    }

    selecaoTipo.addEventListener('input', inicializaLink)
    inicializaLink()
})

()