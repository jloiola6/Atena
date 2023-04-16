// Script para controlar a exibição do mapa no perfil da unidade
(() => {
    const spanMapa = document.querySelector('[data-unidade-mapa]')
    
    if(spanMapa != null){
        const containerMapa = document.querySelector('[data-container-mapa]')
        containerMapa.innerHTML = spanMapa.textContent
    }else
        return
    
    const containerEdicao = document.querySelector('[data-container-mapa-editar]')
    const botaoEditar = document.querySelector('[data-editar-mapa]')

    if(botaoEditar != null)
        botaoEditar.addEventListener('click', (evento) => {
            evento.target.parentElement.classList.add('oculto')

            containerEdicao.classList.remove('oculto')
        })

    const botaoCancelar = document.querySelector('[data-editar-mapa-cancelar]')

    if(botaoCancelar != null)
        botaoCancelar.addEventListener('click', (evento) => {
            evento.preventDefault()

            containerEdicao.classList.add('oculto')

            botaoEditar.parentElement.classList.remove('oculto')
        })
})

()