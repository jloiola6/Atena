// Script para controlar a exibição de etapas de ensino de acordo com a modalidade selecionada pelo usuário

const inicializaFormulario = () => {
    const selecaoModalidades = document.querySelector("[data-selecao-modalidade]")
    const selecaoEtapas = document.querySelector("[data-selecao-etapa]")

    const opcoesEtapas = document.querySelectorAll("[data-opcao-etapa]")

    const carregaEtapas = () => {
        const idModalidade = selecaoModalidades.value

        let primeiroSelecionado = false

        opcoesEtapas.forEach((opcao) => {
            const valueEtapa = opcao.value
            const modalidade = opcao.getAttribute("data-opcao-etapa")

            if(modalidade != idModalidade)
                opcao.classList.add("oculto")
            else{
                opcao.classList.remove("oculto")

                if(!primeiroSelecionado){
                    selecaoEtapas.value = valueEtapa
                    primeiroSelecionado = true
                }
            }
        })
    }

    selecaoModalidades.addEventListener("change", carregaEtapas)

    carregaEtapas()
}

inicializaFormulario()