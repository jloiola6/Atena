// Script para controlar o comportamento dos campos no formulario de contrato

(() => {
    const formulario = document.querySelector('form')

    const botaoSubmeter = formulario.querySelector('button[type="submit"]')

    formulario.onsubmit = (() => {
        botaoSubmeter.disabled = true
    })
})

()