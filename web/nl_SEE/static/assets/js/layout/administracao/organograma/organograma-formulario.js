// Funções para controlar a exibição e validação do formulário de organogramas

function ativaBotaoCadastrar(operador){
    const botaoCadastrar = document.getElementById("botao-cadastrar-organograma");
    botaoCadastrar.disabled = !operador;
}

function ativaCampoNome(operador){
    const campoNome = document.getElementById("organograma-formulario-nome");
    campoNome.disabled = !operador;

    if(!operador)
        campoNome.value = "";
}

function validaFormularioOrganograma(){
    const campoNome = document.getElementById("organograma-formulario-nome");
    
    const valido = campoNome.value.trim().length > 0;

    ativaBotaoCadastrar(valido);
}

function valorRadioMarcado(){
    const radioLista = document.getElementsByName("organograma-formulario-hierarquia");

    for(let i=0; i<radioLista.length; i++)
        if(radioLista[i].checked)
            return radioLista[i].value;   
}

function exibeGrupo(elemento, operador){
    if(operador)
        elemento.style.display = "block";
    else
        elemento.style.display = "none";
}

function controlaCamposSelecao(){
    const valorMarcado = valorRadioMarcado();
    
    const grupoDepartamento = document.getElementById("organograma-formulario-grupo-departamento");
    const grupoDivisao = document.getElementById("organograma-formulario-grupo-divisao");

    if(valorMarcado == "departamento"){
        exibeGrupo(grupoDepartamento, false);
        exibeGrupo(grupoDivisao, false);
    }else if(valorMarcado == "divisao" ){
        exibeGrupo(grupoDepartamento, true);
        exibeGrupo(grupoDivisao, false);
    }else if(valorMarcado == "nucleo" ){
        exibeGrupo(grupoDepartamento, true);
        exibeGrupo(grupoDivisao, true);
    }
}

function valorDiretoriaSelecionada(){
    const selecaoDiretoria = document.getElementById("organograma-formulario-diretoria");
    const diretoriaSelecionada = selecaoDiretoria.options[selecaoDiretoria.selectedIndex].value;

    return diretoriaSelecionada;
}

function carregaDepartamentos(){
    
    const diretoriaSelecionada = valorDiretoriaSelecionada();

    const selecaoDepartamento = document.getElementById("organograma-formulario-departamento");
    let departamento;

    for(let i=selecaoDepartamento.options.length - 1; i>=0; i--){
        departamento = selecaoDepartamento.options[i];

        if(!departamento.classList.contains(diretoriaSelecionada)){
            departamento.style.display = "none";
        }
        else{
            departamento.style.display = "block";

            selecaoDepartamento.value = departamento.value;
        }
    }
    carregaDivisoes();
}

function valorDepartamentoSelecionado(){
    const selecaoDepartamento = document.getElementById("organograma-formulario-departamento");
    const departamentoSelecionado = selecaoDepartamento.options[selecaoDepartamento.selectedIndex].value;

    return departamentoSelecionado;
}

function possuiDivisoes(departamento){
    const opcoesDivioes = document.querySelectorAll(".opcaoDivisao");
    let opcao;

    for(let i=0; i<opcoesDivioes.length; i++){
        opcao = opcoesDivioes[i];
        console.log(opcao);
        if(opcao.classList.contains(departamento))
           return true;    
    }
    
    return false;
}



function carregaDivisoes(){
    const departamentoSelecionado = valorDepartamentoSelecionado();

    const selecaoDivisao = document.getElementById("organograma-formulario-divisao");
    let divisao;
    let contDivisoes = 0;

    for(let i=0; i<selecaoDivisao.options.length; i++){
        divisao = selecaoDivisao.options[i];

        if(!divisao.classList.contains(departamentoSelecionado)){
            divisao.style.display = "none";
        }
        else{
            contDivisoes++;
            divisao.style.display = "block";
            selecaoDivisao.value = divisao.value;
        }
    }

    const valido = contDivisoes == 0;

    selecaoDivisao.disabled = valido;
    ativaCampoNome(!valido);
    
}