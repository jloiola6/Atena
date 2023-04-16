// Script para controlar a validação de formulários antes que sejam submetido

(() => {
    const formularios = document.querySelectorAll('form')

    const containerCamposPendentes = (labels) => {
        const div = document.createElement('div')
        div.toggleAttribute('data-form-pendentes')
        div.classList.add('container-detalhes')

        const html = `
            <span class="texto-azul">Os seguintes campos precisam ser preenchidos:</span>
        `

        div.innerHTML = html

        labels.forEach((label) => {
            div.innerHTML += `
                <span class="texto-vermelho texto-negrito">${label}</span>
            `
        })

        return div
    }

    // Percorrendo todos os formulários da página
    if(formularios)
        formularios.forEach((formulario) => {
            const botaoSubmissao = formulario.querySelector('button[type="submit"]')

            const validaSubmissao = (evento) => {
                evento.preventDefault()
                const botao = evento.target
                // console.log('Formulario ',formulario)

                const camposRequired = formulario.querySelectorAll('input[required]')
                // console.log('Campos required ',camposRequired)

                const camposVazios = [...camposRequired].filter((campo) => {
                    return campo.value.trim() == ''
                })
                // console.log('Campos vazios', camposVazios)

                if(camposVazios.length > 0){
                    const labels = [...camposVazios].map(campo => {
                        return campo.labels[0].textContent
                    })

                    // console.log('Labels', labels)
                    const containerBotoes = botao.parentElement
                    const containerPai = containerBotoes.parentElement

                    const divPendentes = containerPai.querySelector('[data-form-pendentes]')

                    if(divPendentes)
                        divPendentes.remove()

                    const novaDivPendentes = containerCamposPendentes(labels)

                    containerPai.appendChild(novaDivPendentes)
                }else
                    formulario.submit()
            }

            botaoSubmissao.addEventListener('click', validaSubmissao)
        })
})

()