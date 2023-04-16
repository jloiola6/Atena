// Script para controlar a navegação do formulário do Relatório Final do aluno


function ativaItem(item){
    item.classList.add("navegacao-surface-item-ativo");
}

function desativaItem(item){
    item.classList.remove("navegacao-surface-item-ativo");
}

function getItem(atributo){
    const itemsNavegacao = document.querySelectorAll("[data-nav-item]");
    let itemRetorno = null;

    itemsNavegacao.forEach((item) => {
        if(item.getAttribute("data-nav-item") == atributo)
            itemRetorno = item;
    });
    
    return itemRetorno;
}

function inicializaElementos(){
    const botaoGeralAvancar = document.getElementById("botao-geral-avancar");

    const botaoDiversificadaVoltar = document.getElementById("botao-diversificada-voltar");

    const geralAvancar = (evento) => {
        evento.preventDefault();

        const divGeral = document.querySelector("[data-form-geral]");
        divGeral.style.display = "none"

        const divDiversificada = document.querySelector("[data-form-diversificada]");
        divDiversificada.style.display = "block"

        const navGeral = getItem("geral");
        const navDiversificada = getItem("diversificada");

        desativaItem(navGeral);
        ativaItem(navDiversificada);
    }

    const diversificadaVoltar = (evento) => {
        evento.preventDefault();

        const divDiversificada = document.querySelector("[data-form-diversificada]");
        divDiversificada.style.display = "none";

        const divGeral = document.querySelector("[data-form-geral]");
        divGeral.style.display = "block"

        const navDiversificada = getItem("diversificada");
        const navGeral = getItem("geral");

        desativaItem(navDiversificada);
        ativaItem(navGeral);
    }


    if(botaoGeralAvancar != null)
        botaoGeralAvancar.addEventListener("click", geralAvancar);

    if(botaoDiversificadaVoltar != null)
        botaoDiversificadaVoltar.addEventListener("click", diversificadaVoltar);
}

inicializaElementos();