// Script para controlar a exibião de modais

(() => {
    const botoes = document.querySelectorAll('[data-modal-abrir]')

    botoes.forEach((botao) => {
        botao.addEventListener('click', (evento) => {
            evento.preventDefault()
            const atributo = botao.getAttribute('data-modal-abrir')
            const modal = document.querySelector(`[data-modal="${atributo}"]`)

            if(modal){
                modal.classList.remove('oculto')

                if(atributo == 'confirmar'){
                    const camposPendentes = modal.querySelector('[data-form-pendentes]')

                    if(camposPendentes)
                        camposPendentes.remove()
                }
            }else{
                console.error(`MODAL NÃO ENCONTRATO\nAtributo: ${atributo}`)
            }
        })
    })

    window.onclick = (event) => {
        if(event.target.matches("[data-modal]")){
            const modais = document.querySelectorAll("[data-modal]")

            if(modais != null)
                modais.forEach((modal) => {
                    if(!modal.hasAttribute('data-modal-bloqueado'))
                        modal.classList.add('oculto')
                })
        }
    }

    const botoesFechar = document.querySelectorAll('[data-modal-fechar]')

    botoesFechar.forEach((botao) => {
        botao.addEventListener('click', (evento) => {
            evento.preventDefault()
            const modais = document.querySelectorAll("[data-modal]")

            if(modais != null)
                modais.forEach((modal) => {
                    modal.classList.add('oculto')
                })
        })
    })
})

()