// // Funções para controlar a exibição e validação do formulário de organogramas

// function tipoSetor(elemento){
//     listaClasses = elemento.classList;

//     if(listaClasses.contains("diretoria"))
//         return "diretoria";
//     else if(listaClasses.contains("departamento"))
//         return "departamento";
//     else if(listaClasses.contains("divisao"))
//         return "divisao";
//     else if(listaClasses.contains("nucleo"))
//         return "nucleo";
// }

// function resetaMenu(elemento){
//     elemento.lastElementChild.remove();
//     elemento.onclick = null;
// }

// function possuiFilho(elemento){
//     const tipo = tipoSetor(elemento);
//     const proximo = elemento.nextElementSibling;

//     if(proximo == null)
//         return false;
//     else if(tipo == "departamento" && tipoSetor(proximo) != "divisao")
//         return false;
//     else if(tipo == "departamento" && tipoSetor(proximo) == "divisao")
//         return true;

//     if(tipo == "divisao" && tipoSetor(proximo) != "nucleo")
//         return false;
//     else if(tipo == "divisao" && tipoSetor(proximo) == "nucleo")
//         return true;

// }

// function ajusteDepartamentos(){
//     const departamentos = document.getElementsByClassName("departamento");
//     let elemento;

//     for(let i=0; i<departamentos.length; i++){
//         elemento = departamentos[i];
        
//         if(!possuiFilho(elemento))
//             resetaMenu(elemento);
//     }

// }

// function ajusteDivisoes(){
//     const divisoes = document.getElementsByClassName("divisao");
//     let elemento;

//     for(let i=0; i<divisoes.length; i++){
//         elemento = divisoes[i];

//         if(!possuiFilho(elemento))
//             resetaMenu(elemento);
//     }
// }

// ajusteDepartamentos()
// ajusteDivisoes()