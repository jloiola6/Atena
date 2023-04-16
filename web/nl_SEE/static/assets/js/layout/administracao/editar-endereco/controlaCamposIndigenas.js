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
        const botaoAvancar = document.querySelector('[data-botao-avancar]')
        const botaoSalvar = document.querySelector('[data-botao-salvar]')

        const controlaExibicaoIndigena = () => {
            const valorSelecionado = selecaoTipoLocalzacao.value
            const exibicao = valorSelecionado == 'Indígena'

            if(exibicao){
                abaIndigena.classList.remove('oculto')
                botaoAvancar.classList.remove('oculto')
                botaoSalvar.classList.add('oculto')
            }else{
                abaIndigena.classList.add('oculto')
                botaoAvancar.classList.add('oculto')
                botaoSalvar.classList.remove('oculto')
            }

        }

        selecaoTipoLocalzacao.addEventListener('change', controlaExibicaoIndigena)

        controlaExibicaoIndigena()
    }

    exibeFormIndigena()
    inicializaCamposIndigenas()
})

()