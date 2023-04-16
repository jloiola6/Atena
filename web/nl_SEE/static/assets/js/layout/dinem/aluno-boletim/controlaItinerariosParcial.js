(() => {

    const radioAprofundamento = document.querySelector('[data-radio-aprofundamento]')
    const radioProfissional = document.querySelector('[data-radio-profissional]')

    const grupoConhecimento = document.querySelector('[data-grupo-conhecimento]')
    const grupoFormacaoTecnica = document.querySelector('[data-campo-formacao]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    if(radioAprofundamento && radioProfissional){
        const controlaRadios = () => {
            controlaExibicao(grupoConhecimento, radioAprofundamento.checked)
            controlaExibicao(grupoFormacaoTecnica, !radioAprofundamento.checked)
        }
        
        controlaRadios()
        
        radioAprofundamento.addEventListener('click', controlaRadios)
        radioProfissional.addEventListener('click', controlaRadios)
    }


})

()