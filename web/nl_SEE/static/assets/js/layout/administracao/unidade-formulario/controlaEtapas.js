(() => {
    const grupoEtapas = document.querySelector('[data-grupo-etapas]')
    const camposEtapas = grupoEtapas.elements

    const botaoAvancar = document.querySelector('[data-form-botao="endereco"]')

    const validaEtapas = () => {
        let desabilitaBotao = true

        for(let i=0; i<camposEtapas.length; i++){
            const etapa = camposEtapas[i]

            if(etapa.checked){
                desabilitaBotao = false
                break
            }
        }

        botaoAvancar.disabled = desabilitaBotao
    }

    validaEtapas()

    for(let i=0; i<camposEtapas.length; i++){
        const etapa = camposEtapas[i]

        etapa.addEventListener('click', validaEtapas)
    }
})

()