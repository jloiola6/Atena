// Script para controlar o botão de exportação dos Termos de Devolução

(() => {
    const formulario = document.querySelector('[data-formulario-exportacao]')
    const modal = formulario.parentElement.parentElement
    const botaoExportar = document.querySelector('[data-modal-abrir="descricao_notebook"]')

    formulario.addEventListener('submit', () => {
        modal.classList.add('oculto')
        botaoExportar.remove()
    })



})()