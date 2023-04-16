// Script para controlar o comportamento de alguns campos no formulário de Relatório Final do aluno

// Controlar a exibição dos campos de rotas

// export const inicializaRotas = () => {

//     const radioPropedeutica = document.getElementById("radio-propedeutica");
//     const radioFormacao = document.getElementById("radio-formacao");
    
//     const camposPropedeuticas = document.querySelectorAll("[data-form-propedeutica]");
    
//     const controlaPropedeuticas = (display) => {
//         camposPropedeuticas.forEach((campo) => {
//             campo.style.display = display;

//             if(display == "none")
//                 campo.lastElementChild.required = false;

//             else if(display == "flex")
//                 campo.lastElementChild.required = true;
//         });
//     };

//     if(radioPropedeutica != null)
//         radioPropedeutica.onclick = () => {
//             controlaPropedeuticas("flex")
//         };

//     if(radioFormacao != null){
//         radioFormacao.onclick = () => {
//             controlaPropedeuticas("none");
//         };

//         if(radioFormacao.checked){
//             controlaPropedeuticas("none");
//         }
//     }
        

// };

// const inicializaMascara = () => {
//     const camposNota = document.querySelectorAll("[data-campo-nota]");

//     camposNota.forEach((campo) => {
//         campo.onchange = () => {
//             if(campo.value != "NaN")
//                 campo.value = parseFloat(campo.value).toFixed(1);
//         };
//     });
// };

// const botaoNot = document.querySelector("[data-cabecalho-notificacao]");

// if(botaoNot != null)
//     botaoNot.onclick = () => {
//         const camposNota = document.querySelectorAll("[data-campo-nota]");
//         camposNota.forEach((campo) => {
//             campo.value = "5.0";
//         });
//     };
        


// inicializaRotas();
// inicializaMascara();