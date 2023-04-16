(() => {

    const campoSenhaAtual = document.querySelector('[data-senha-atual]')
    const mensagemSenhaIncorreta = document.querySelector('[data-senha-incorreta]')

    const campoNovaSenha = document.querySelector('[data-nova-senha]')
    const mensagemValidacao1 = document.querySelector('[data-validacao1]')
    const mensagemValidacao2 = document.querySelector('[data-validacao2]')
    const mensagemValidacao3 = document.querySelector('[data-validacao3]')

    const campoConfirmaSenha = document.querySelector('[data-confirma-senha]')
    const mensagemConfirmacao = document.querySelector('[data-confirmacao]')


    const containerBotoes = document.querySelector('[data-botao-cadastrar]').parentElement

    const senhaAtual = campoSenhaAtual.dataset.senhaAtual

    campoNovaSenha.readOnly = true
    campoConfirmaSenha.readOnly = true

    const controlaExibicao = (operador, elemento) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }   

    const verificaSenhaAtual = () => {
        const valor = campoSenhaAtual.value

        if(valor.trim().length > 0){

            const valorHash = md5(valor)
            
            const valida = valorHash == senhaAtual

            controlaExibicao(!valida, mensagemSenhaIncorreta)

            if(!valida)
                controlaExibicao(valor.length >= 11, mensagemSenhaIncorreta)
        
            campoNovaSenha.readOnly = !valida
        }
        
    }

    const verificaNovaSenha = () => {
        const valor = campoNovaSenha.value

        const validacao1 = valor.length >= 8 && valor.length <= 15
        controlaExibicao(!validacao1, mensagemValidacao1)

        const validacao2 = /[A-Z]/.test(valor)
        controlaExibicao(!validacao2, mensagemValidacao2)

        const validacao3 = /\d/.test(valor)
        controlaExibicao(!validacao3, mensagemValidacao3)

        campoConfirmaSenha.readOnly = !(validacao1 && validacao2 && validacao3)
    }

    const confirmaSenha = () => {
        const valor = campoConfirmaSenha.value

        const valida = valor == campoNovaSenha.value
        controlaExibicao(!valida, mensagemConfirmacao)
        controlaExibicao(valida, containerBotoes)
    }

    campoSenhaAtual.addEventListener('input', verificaSenhaAtual)
    campoNovaSenha.addEventListener('input', verificaNovaSenha)
    campoConfirmaSenha.addEventListener('input', confirmaSenha)
})

()