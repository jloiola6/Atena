// Script para controlar os campos do formulario de edição de contatos de uma unidade

import { inicializaCampos } from "../../../module/mascaras.js";

(() => {
    let contador = 1;

    // Criando o elemento para inserção de contatos
    const FormularioGrupo = (tipoContato, contador) => {
        let tipo, placeholder, mascara

        if(tipoContato == 'telefone' || tipoContato == 'celular'){
            tipo = 'tel'
            mascara = 'data-mascara="telefone"'

            if(tipoContato == 'telefone')
                placeholder = 'Ex: (00) 0000-0000'
            else
                placeholder = 'Ex: (00) 00000-0000'
        }
        else{
            tipo = 'email'
            placeholder = 'Ex: escola@escola.com'
            mascara = ''
        }

        const html = `
            <input class="campo-texto campo-medio" type="${tipo}" name="${tipoContato + contador}" placeholder="${placeholder}" autocomplete="off" ${mascara} required>
            <button class="botao botao--vermelho" data-botao-excluir>Excluir</button>
        `

        const div = document.createElement('div')
        div.innerHTML = html
        div.classList.add('container-contato-edicao')

        return div
    }

    // Funções para manipular a criação de novos campos de contato
    const excluirContato = (evento) => {
        evento.preventDefault()
        evento.target.parentElement.remove()
    }

    const adicionarContato = (evento) => {
        evento.preventDefault()
        const tipoContato = evento.target.getAttribute('data-botao-adicionar')
        const containerContatos = evento.target.parentElement.parentElement
        containerContatos.insertBefore(FormularioGrupo(tipoContato, contador), containerContatos.lastElementChild)
        inicializaCampos()
        inicializaBotoes()
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
})

()