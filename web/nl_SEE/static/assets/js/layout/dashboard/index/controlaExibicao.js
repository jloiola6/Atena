// Script para controlar a exibição da dashboard

(() => {
    const botoesDashboard = document.querySelectorAll('[data-dashboard-botao]')



    const trocaContainer = (evento) => {
        let botao

        if(!evento.target.attributes.getNamedItem('data-dashboard-botao'))
            botao = evento.target.parentElement
        else
            botao = evento.target
        
        if(!botao.attributes.getNamedItem('selecionado')){
            const botaoAtual = document.querySelector('[selecionado]')
            botaoAtual.toggleAttribute('selecionado')
            botao.toggleAttribute('selecionado')


            const containerAtual = document.querySelector(`[data-dashboard-container="${botaoAtual.getAttribute('data-dashboard-botao')}"]`)
            const containerNovo = document.querySelector(`[data-dashboard-container="${botao.getAttribute('data-dashboard-botao')}"]`)

            containerAtual.classList.toggle('oculto')
            containerNovo.classList.toggle('oculto')
        }
    }

    botoesDashboard.forEach((botao) => botao.addEventListener('click', trocaContainer))
})

()