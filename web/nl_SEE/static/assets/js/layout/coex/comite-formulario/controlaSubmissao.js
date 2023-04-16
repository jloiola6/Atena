// Script para controlar a submissão de formulários impedindo que o usuário aperte várias vezes o botão de submissão
(() => {
    const formularios = document.querySelectorAll('form')

    if(formularios.length > 0)
        formularios.forEach((formulario) => {
            const botaoSubmissao = formulario.querySelector('[type="submit"]')

            formulario.addEventListener('submit', (evento) => {
                botaoSubmissao.disabled = true
            })
        })
})

()