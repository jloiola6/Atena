// Script para controlar o comportamento e validação do formulário de infraestrutura

(() => {
    const campos = document.querySelectorAll('[data-checkbox]')
    const grupos = document.querySelectorAll('[data-grupo-check]')
    const botaoCadastrar = document.querySelector('[data-botao-cadastrar]')

    const desabilitaCampos = (campo) => {
        const checkboxNA = campo

        const formularioGrupo = checkboxNA.parentElement.parentElement

        const grupoFilhos = formularioGrupo.children

        for (const filho of grupoFilhos) {
            if(filho.tagName == 'DIV'){
                const checkbox = filho.firstElementChild
                
                if(checkbox.getAttribute('data-checkbox') != 'NA'){
                    if(checkbox.checked)
                        checkbox.checked = false

                    checkbox.disabled = checkboxNA.checked
                }
            }
        }

        // console.log(formularioGrupo, grupoFilhos)
    }

    const inicializaCamposNA = () => {
        campos.forEach((campo) => {
            if(campo.getAttribute('data-checkbox') == 'NA'){
                campo.addEventListener('click', () => desabilitaCampos(campo))

                if(campo.checked)
                    desabilitaCampos(campo)
            }

            
        })
    }

    inicializaCamposNA()

    const verificaCampos = () => {
        let habilita = true

        grupos.forEach((grupo) => {
            let umCheck = false
            
            const grupoFilhos = grupo.children

            for (const filho of grupoFilhos) {
                if(filho.tagName == 'DIV'){
                    const checkbox = filho.firstElementChild

                    if(checkbox.checked){
                            umCheck = true
                            break
                        }
                }
            }

            if(!umCheck){
                habilita = false
            }

        })

        botaoCadastrar.disabled = !habilita
    }

    const inicializaCampos = () => {
        campos.forEach((campo) => {
            campo.addEventListener('click', verificaCampos)
        })
    }

    verificaCampos()
    inicializaCampos()
})

()