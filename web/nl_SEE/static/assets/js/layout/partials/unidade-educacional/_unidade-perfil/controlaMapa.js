// Script para controlar a exibição do mapa de uma unidade educacional

(() => {
    const spanMapa = document.querySelector('[data-mapa]')
    const botaoEditarMapa = document.querySelector('[data-botao-editar-mapa]')
    const containerEditarMapa = document.querySelector('[data-container-editar-mapa]')

    if(spanMapa){
        const containerMapa = spanMapa.parentElement
        containerMapa.innerHTML = spanMapa.textContent

        const frameMapa = containerMapa.querySelector('iframe')
        frameMapa.classList.add('unidade__mapa')

        const exibeContainerEdicao = () => {
            containerEditarMapa.classList.remove('oculto')
            botaoEditarMapa.parentElement.remove()
        }

        botaoEditarMapa.addEventListener('click', exibeContainerEdicao)
    }

})

()