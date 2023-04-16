// Script para detectar a resolução do dispositivo que está acessando

(() => {
    const campoResolucao = document.querySelector('[data-campo-resolucao]')
    const botaoDetectar = document.querySelector('[data-botao-detectar]')

    const detectarResolucao = () => {
        const largura = window.outerWidth
        const altura = window.outerHeight

        campoResolucao.value = `${largura} x ${altura}`
    }

    botaoDetectar.addEventListener('click', detectarResolucao)
})

()