// Script para controlar os campos nos filtros avançados de contratos

(() => {
    const selecoesTudo = document.querySelectorAll('[data-selecao-tudo]')
    const selecoes = document.querySelectorAll('input[type="checkbox"]')

    const selecionaTudo = (evento) => {
        const campo = evento.target

        if(campo.checked){
            const grupo = campo.parentElement.parentElement

            const selecoes = grupo.querySelectorAll('input')

            selecoes.forEach((campo) => {
                campo.checked = true
            })
        }
    }

    selecoesTudo.forEach((campo) => {
        campo.addEventListener('click', selecionaTudo)
    })

    const controlaSelecao = (evento) => {
        const campo = evento.target
        
        if(!campo.checked){
            const grupo = campo.parentElement.parentElement
            const selecaoTudo = grupo.querySelector('[data-selecao-tudo]')

            selecaoTudo.checked = false
        }
    }

    selecoes.forEach((campo) => {
        if(!campo.id.includes('todos'))
            campo.addEventListener('click', controlaSelecao)
    })
})

()