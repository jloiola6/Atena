// Script para controlar o comportamento do Relatório Final do aluno de acordo com a situação

(() => {
    const radioMatriculado = document.querySelector('[data-radio-situacao-matriculado]')
    const radioTransferido = document.querySelector('[data-radio-situacao-transferido]')
    const radioDesistente = document.querySelector('[data-radio-situacao-desistente]')

    const containerSalvar = document.querySelector('[data-salvar-situacao]')

    const containerBoletim = document.querySelector('[data-container-boletim]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaContainerBoletim = () => {
        const validaMatriculado = radioMatriculado.checked

        controlaExibicao(containerSalvar, !validaMatriculado)
        controlaExibicao(containerBoletim, validaMatriculado)
    }

    controlaContainerBoletim()

    radioMatriculado.addEventListener('click', controlaContainerBoletim)
    radioTransferido.addEventListener('click', controlaContainerBoletim)
    radioDesistente.addEventListener('click', controlaContainerBoletim)
})

()

// import {inicializaRotas} from "../aluno-boletim/controlaCampos.js";

// const inicializaSituacoes = () => {
//     const radioMatriculado = document.getElementById("radio-matriculado");
//     const radioTransferido = document.getElementById("radio-transferido");
//     const radioDesistente = document.getElementById("radio-desistente");

//     const botaoSalvar = document.querySelector("[data-form-transferido-salvar]")
//     const formularioRelatorio = document.querySelector("[data-form-relatorio]");

//     const controlaFormulario = (display) => {
//         if(formularioRelatorio != null)
//             formularioRelatorio.style.display = display;
//     }

//     const controlaBotaoSalvar = (display) => {
//         if(botaoSalvar != null)
//             botaoSalvar.style.display = display;
//     }

//     const controlaRequired = (operador) => {
//         const campos = document.querySelectorAll("[data-campo-nota]");

//         campos.forEach((campo) => {
//             campo.required = operador;
//         });
//     }


//     if(radioMatriculado != null)
//         radioMatriculado.onclick = () => {
//             controlaFormulario("block");
//             controlaRequired(true);
//             controlaBotaoSalvar("none")
//             inicializaRotas();
//         }

//     if(radioTransferido != null){
//         radioTransferido.onclick = () => {
//             controlaFormulario("none");
//             controlaRequired(false);
//             controlaBotaoSalvar("block");
//         }

//         if(radioTransferido.checked){
//             controlaFormulario("none");
//             controlaRequired(false);
//             controlaBotaoSalvar("block");
//         }
//     }

//     if(radioDesistente != null){
//         radioDesistente.onclick = () => {
//             controlaFormulario("none");
//             controlaRequired(false);
//             controlaBotaoSalvar("block");
//         }

//         if(radioDesistente.checked){
//             controlaFormulario("none");
//             controlaRequired(false);
//             controlaBotaoSalvar("block");
//         }
//     }
// }

// inicializaSituacoes();