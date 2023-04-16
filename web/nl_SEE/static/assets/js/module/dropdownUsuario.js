// Script para controlar o dropdown que controla um card ao clicar no botão de usuário no cabeçalho

(() => {
    
    const spamUsuario = document.querySelector("[data-usuario]")
    const dropdownUsuario = document.querySelector("[data-usuario-dropdown]")

    const exibeDropdown = (operador) => {
        dropdownUsuario.setAttribute('data-usuario-dropdown', `${operador}`)

        if(operador)
            dropdownUsuario.classList.remove("oculto")
        else
            dropdownUsuario.classList.add("oculto")
    }

    const controlaDropdown = () => {
        const operador = dropdownUsuario.getAttribute('data-usuario-dropdown') == "false"
        exibeDropdown(operador)
    }

    if(spamUsuario != null)
        spamUsuario.addEventListener("click", controlaDropdown)
    

    window.addEventListener('click', (evento) => {
        // Verifica se o click foi no dropdown do usuário ou no seu conteúdo
        const dropdownClicado = evento.target.matches('[data-usuario-dropdown]') || evento.target.matches('[data-usuario-dropdown-conteudo]')

        // Verifica se o dropdown já está aberto
        const dropdownAberto = dropdownUsuario.getAttribute('data-usuario-dropdown') == 'true'

        // Verifica se o click foi no span de usuário
        const spanClicado = evento.target.matches('[data-usuario]')

        if(!spanClicado)
            if(!dropdownClicado && dropdownAberto)
                controlaDropdown()
    })
})

()