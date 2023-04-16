// Script para controlar a disposição dos campos de unidades de localização indígena

(() => {

    const inicializaCamposIndigenas = () => {
        const radiosExistente = document.querySelectorAll('[data-radio-indigena-existente]')
        const radiosNova = document.querySelectorAll('[data-radio-indigena-nova]')

        radiosExistente.forEach((radio) => {
            const atributo = radio.getAttribute('data-radio-indigena-existente')

            radio.addEventListener('click', () => {
                const selecao = document.querySelector(`[data-selecao-indigena="${atributo}"]`)
                const campo = document.querySelector(`[data-campo-indigena="${atributo}"]`)

                selecao.classList.remove('oculto')
                campo.classList.add('oculto')
            })
        })

        radiosNova.forEach((radio) => {
            const atributo = radio.getAttribute('data-radio-indigena-nova')

            radio.addEventListener('click', () => {
                const selecao = document.querySelector(`[data-selecao-indigena="${atributo}"]`)
                const campo = document.querySelector(`[data-campo-indigena="${atributo}"]`)

                campo.classList.remove('oculto')
                selecao.classList.add('oculto')
            })
        })
    }

    // Função para controlar a exibição dos detalhes indígenas no formulário de unidade de acordo com o tipo de localização selecionado
    const exibeFormIndigena = () => {
        const selecaoTipoLocalzacao = document.querySelector('[data-selecao-tipo-localizacao]')
        const abaIndigena = document.querySelector('[data-form-aba="indigena"]')
        const botoesIndigenas = document.querySelectorAll('[data-botao-indigena]')

        const controlaExibicaoIndigena = () => {
            const valorSelecionado = selecaoTipoLocalzacao.value
            const exibicao = valorSelecionado == 'Indígena'

            
            botoesIndigenas.forEach((botao) => {
                
                // let atributo

                if(exibicao){
                    abaIndigena.classList.remove('oculto')

                    const atributo = botao.getAttribute('data-form-botao')
                    botao.setAttribute('data-form-botao', 'indigena')
                    botao.setAttribute('data-botao-indigena', atributo)
                }else{
                    abaIndigena.classList.add('oculto')

                    const atributo = botao.getAttribute('data-botao-indigena')

                    if(atributo != 'indigena'){
                        botao.setAttribute('data-botao-indigena', 'indigena')
                        botao.setAttribute('data-form-botao', atributo)
                    }
                }
            })

        }

        selecaoTipoLocalzacao.addEventListener('change', controlaExibicaoIndigena)

        controlaExibicaoIndigena()
    }

    exibeFormIndigena()
    inicializaCamposIndigenas()
})

()