// Script para controlar a exibição de checkbox no exportar contrato
(() => {

    // Função genérica para controlar a exibição de um elemento
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Funções para o comportamento de seleção do formato de exportação
    const selecaoExcel = document.querySelector('[data-selecao-excel]')
    const selecaoPdf = document.querySelector('[data-selecao-pdf]')

    const radioExcel = document.querySelector('[data-radio-excel]')
    const radioPdf = document.querySelector('[data-radio-pdf]')

    // Função para ocultar ou mostrar uma div
    const inicializaCampos = () => {
        const operador = radioPdf.checked

        controlaExibicao(selecaoPdf, operador)
        controlaExibicao(selecaoExcel, !operador)
    }

    radioExcel.addEventListener('click', inicializaCampos)
    radioPdf.addEventListener('click', inicializaCampos)

    inicializaCampos()

})

()