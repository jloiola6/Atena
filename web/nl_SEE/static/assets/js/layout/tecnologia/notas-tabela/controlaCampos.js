(() => {
    const selecoesSituacao = document.querySelectorAll('[data-selecao-situacao]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const exibeCampos = (selecao) => {
        const valor = selecao.value

        const formulario = selecao.parentElement.parentElement

        const grupoDiferenca = formulario.querySelector('[data-grupo-diferenca]')
        const grupoMotivo = formulario.querySelector('[data-grupo-motivo]')

        const validaPendente = valor == 'P'

        controlaExibicao(grupoDiferenca, !validaPendente)
        controlaExibicao(grupoMotivo, !validaPendente)

        if(validaPendente)
            return

        const validaAprovado = valor == 'A'

        controlaExibicao(grupoDiferenca, validaAprovado)
        controlaExibicao(grupoMotivo, !validaAprovado)

    }

    selecoesSituacao.forEach((selecao) => {
        selecao.addEventListener('change', () => {exibeCampos(selecao)})
        exibeCampos(selecao)

        // const valor = selecao.value
        // const formulario = selecao.parentElement.parentElement

        // const grupoDiferenca = formulario.querySelector('[data-grupo-diferenca]')
        // const grupoMotivo = formulario.querySelector('[data-grupo-motivo]')

        // const validaPendente = valor == 'P'

        // controlaExibicao(grupoDiferenca, !validaPendente)
        // controlaExibicao(grupoMotivo, !validaPendente)

        // if(validaPendente)
        //     return

        // const validaAprovado = valor == 'A'

        // controlaExibicao(grupoDiferenca, validaAprovado)
        // controlaExibicao(grupoMotivo, !validaAprovado)
    })
})

()