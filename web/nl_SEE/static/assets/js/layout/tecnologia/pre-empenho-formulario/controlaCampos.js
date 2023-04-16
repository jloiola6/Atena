// Script para controlar o comportamento do formulário de pré-empenho

(() => {
    // Inicializando os elementos da página
    const camposMensais = document.querySelectorAll('[data-mensal-item]')
    const camposTotais = document.querySelectorAll('[data-total-item]')
    const campoMes = document.querySelector('[data-meses]')
    const campoGlobal = document.querySelector('[data-valor-global]')

    // Função para atualizar o total do item de acordo com a quantidade de meses
    const atualizaTotais = () => {
        const qtdMeses = Number.parseInt(campoMes.value)

        if(!isNaN(qtdMeses) && qtdMeses > 0 && qtdMeses <= 12){
            camposMensais.forEach((campo) => {
                const valorMensal = Number.parseFloat(campo.value.replace('R$', '').replace('.', '').replace(',', '.'))
                const valorTotal = valorMensal * qtdMeses

                const pai = campo.parentElement.parentElement
                const campoTotal = pai.querySelector('[data-total-item]')

                campoTotal.value = valorTotal.toFixed(2)
                campoTotal.dispatchEvent(new Event('input'))
            })

        }

        atualizaGlobal()
    }

    

    // Inicializando o campo de quantidade de meses com a função de atualização
    campoMes.addEventListener('input', atualizaTotais)
    
    // Função para atualizar o valor do campo de valor global
    const atualizaGlobal = () => {
        let total = 0.0

        camposTotais.forEach((campo) => {
            const valor = Number.parseFloat(campo.value.replace('R$', '').replace('.', '').replace(',', '.'))
            total += valor
        })

        campoGlobal.value = total.toFixed(2)
        campoGlobal.dispatchEvent(new Event('input'))
    }

    atualizaTotais()
})

()