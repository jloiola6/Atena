(() => {
    const radioTermo = document.querySelector('[data-radio-termo]')
    const radioCancelamento = document.querySelector('[data-radio-cancelamento]')
    const dataCancelamento = document.querySelector('[data-grupo-data-cancelamento]')
    const motivoCancelamento = document.querySelector('[data-grupo-motivo-cancelamento]')
    const grupoCancelamento = document.querySelector('[data-grupo-cancelamento]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const inicializaCampos = () => {
        const validaCampo = radioCancelamento.checked

        controlaExibicao(grupoCancelamento, validaCampo)
    }

    radioTermo.addEventListener('click', inicializaCampos)
    radioCancelamento.addEventListener('click', inicializaCampos)

    inicializaCampos()

    const formulario = document.querySelector('[data-formulario-exportacao]')
    const modal = formulario.parentElement
    const botaoExportar = document.querySelector('[data-modal-abrir="exportar"]')

    formulario.addEventListener('submit', () => {
        modal.classList.add('oculto')
    })

})

()