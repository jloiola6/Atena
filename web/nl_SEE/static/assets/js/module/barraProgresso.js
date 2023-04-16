// Script para controlar o componente de barra de progresso

(() => {
    const barras = document.querySelectorAll('[data-progresso]')

    if(barras)
        barras.forEach((barra) => {
            const porcentagem = Number.parseInt(barra.dataset.progresso)

            barra.style.width = `${porcentagem}%`

            if(porcentagem < 100){
                barra.classList.add('barra--azul')
            }else if(porcentagem == 100){
                barra.classList.add('barra--verde')
            }else{
                barra.classList.add('barra--vermelha')
                barra.style.width = '100%'
            }
        })
})

()