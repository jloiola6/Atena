(() => {
    const lista = document.querySelector('[data-lista]')
    const itens = lista.children

    const botao = document.querySelector('[data-botao-escolher]')

    // const escolido = document.querySelector('[data-escolhido]')

    const fudidos = [...itens].map((item) => item.textContent)

    const fotos = document.querySelectorAll('[data-fotinha]')

    const esconderTudo = () => {
        fotos.forEach((foto) => {
            foto.classList.add('oculto')
        })
    }

    const escolher = () => {
        esconderTudo()
        const fudido = Math.floor(Math.random() * fudidos.length)
        fotos[fudido].classList.remove('oculto')
        console.log(fudidos[fudido])

    }

    botao.addEventListener('click', escolher)

})

()
