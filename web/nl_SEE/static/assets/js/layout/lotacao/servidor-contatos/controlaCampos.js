// Script para controlar os campos do formulario de edição de contatos de um servidor

import { inicializaCampos } from "../../../module/mascaras.js";

const inicializaFormulario = () => {
    let contador = 1;

    const excluirContato = (evento) => {
        evento.preventDefault()
        evento.target.parentElement.remove()
    }

    const FormularioGrupo = (tipoContato, contador) => {
        const divGrupo = document.createElement('div')
        divGrupo.classList.add('container-contato-edicao')

        const input = document.createElement('input')
        input.classList.add('campo-texto')
        input.classList.add('campo-medio')
        input.name = tipoContato + contador;
        input.autocomplete = 'off'
        input.required = 'true'

        if(tipoContato == "celular")
            input.placeholder = '68 99999-1234'
        else if(tipoContato == "email")
            input.placeholder = 'escola@escola.com'
        else if(tipoContato == "telefone")
            input.placeholder = '68 3123-1233'

        if(tipoContato == "celular" || tipoContato == "telefone"){
            input.toggleAttribute('data-mascara')
            input.setAttribute('data-mascara', 'telefone')
        }

        const botaoExcluir = document.createElement('button')
        botaoExcluir.toggleAttribute('data-botao-excluir')
        botaoExcluir.classList.add('botao')
        botaoExcluir.classList.add('botao--vermelho')
        botaoExcluir.textContent = 'Exlcuir'
        botaoExcluir.addEventListener('click', excluirContato)

        divGrupo.appendChild(input)
        divGrupo.appendChild(botaoExcluir)

        return divGrupo
    }

    const adicionarContato = (evento) => {
        evento.preventDefault()
        const tipoContato = evento.target.getAttribute('data-botao-adicionar')
        const containerContatos = evento.target.parentElement.parentElement
        containerContatos.insertBefore(FormularioGrupo(tipoContato, contador), containerContatos.lastElementChild)
        inicializaCampos()
        contador++;
    }


    const inicializaBotoes = () => {
        const botoesExcluir = document.querySelectorAll('[data-botao-excluir]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluirContato)
        })

        const botoesAdicionar = document.querySelectorAll('[data-botao-adicionar]')

        botoesAdicionar.forEach((botao) => {
            botao.addEventListener('click', adicionarContato)
        })
    }

    inicializaBotoes()
}

inicializaFormulario()