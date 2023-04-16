(() => {
    const selecaoTipo = document.querySelector('[data-selecao-tipo-contrato]')

    const inicializaLink = () => {
        const tipo = selecaoTipo.value
        let link = '/administracao/contrato-formulario?tipo='

        switch (tipo) {
            case 'Produtos':
                link += 'produto'
                break;

            case 'Serviços':
                link += 'servico'
                break;
        
            case 'Postos de trabalho':
                link += 'trabalho'
                break;
        
            case 'Postos de trabalho - Vigilância Armada':
                link += 'vigilante'
                break;

            case 'Postos de trabalho - Limpeza':
                link += 'limpeza'
                break;
        }

        const a = document.querySelector('[data-link-form-contrato]')
        a.href = link
    }

    selecaoTipo.addEventListener('input', inicializaLink)
    inicializaLink()
})

()