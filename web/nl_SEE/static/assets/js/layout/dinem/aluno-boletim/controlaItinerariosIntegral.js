(()=>{
    const radioPropedeutica = document.querySelector('[data-radio-propedeutica]')
    const radioFormacao = document.querySelector('[data-radio-formacao]')

    const grupoRotas = document.querySelector('[data-grupo-rotas]')
    const grupoFormacaoTecnica = document.querySelector('[data-campo-formacao]')

    const checksAprofundamento = document.querySelectorAll('[data-check-aprofundamento]')
    // const grupoAprofundamento = document.querySelectorAll('[data-grupo-aprofundamento]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaRadios = () => {

        controlaExibicao(grupoRotas, radioPropedeutica.checked)
        controlaExibicao(grupoFormacaoTecnica, !radioPropedeutica.checked)

    }

    controlaRadios()

    radioPropedeutica.addEventListener('click', controlaRadios)
    radioFormacao.addEventListener('click', controlaRadios)

    const controlaChecks = () => {
        let contador = 0

        checksAprofundamento.forEach((check) => {
            const atributo = check.dataset.checkAprofundamento
            const grupoAprofundamento = document.querySelector(`[data-grupo-aprofundamento=${atributo}]`)

            controlaExibicao(grupoAprofundamento, check.checked)

            if(check.checked){
                contador++
            }
        })

        checksAprofundamento.forEach((check) => {
            const validaAprofundamento = contador == 2

            if(!check.checked)
                check.disabled = validaAprofundamento
        })
    }

    controlaChecks()

    checksAprofundamento.forEach((check) => {
        check.addEventListener('click', controlaChecks)
    })

})()