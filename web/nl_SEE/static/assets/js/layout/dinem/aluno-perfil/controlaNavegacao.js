// Script para controlar a navegação do formulário do Relatório Final do aluno


function ativaItem(item){
    item.classList.add("navegacao-surface-item-ativo");
}

function desativaItem(item){
    item.classList.remove("navegacao-surface-item-ativo");
}

function limpaAbas(){
    const abas = document.querySelectorAll("[data-nav-item]")
    
    abas.forEach((aba) => {
        desativaItem(aba)
    })
}

function mostraContainer(container){
    container.classList.remove("oculto");
}

function escondeContainer(container){
    container.classList.add("oculto");
}

function getItem(atributo){
    const itemsNavegacao = document.querySelectorAll("[data-nav-item]");
    
    let elemento = null

    itemsNavegacao.forEach((item) => {
        itemAtributo = item.getAttribute("data-nav-item");
        
        if(itemAtributo == atributo){
            elemento = item;
        }
    });
    return elemento;
}

const inicializaElementos = () => {
    const abas = document.querySelectorAll("[data-nav-item]")
    const containers = document.querySelectorAll("[data-nav-container]")

    ativaItem(abas[0])
    mostraContainer(containers[0])

    

    abas.forEach((aba) => {
        aba.addEventListener('click', function(){
            limpaAbas()
            ativaItem(aba)
            
            const atributoAba = aba.getAttribute("data-nav-item")

            containers.forEach((container) => {
                const atributoContainer = container.getAttribute("data-nav-container")
                escondeContainer(container)

                if(atributoAba == atributoContainer){
                    mostraContainer(container)
                }
            })
        })
    })
}

// function inicializaElementos(){
//     const botaoGeralAvancar = document.getElementById("botao-geral-avancar");

//     const botaoDiversificadaVoltar = document.getElementById("botao-diversificada-voltar");

//     const geralAvancar = (evento) => {
//         evento.preventDefault();

//         const divGeral = document.querySelector("[data-form-geral]");
//         divGeral.style.display = "none"

//         const divDiversificada = document.querySelector("[data-form-diversificada]");
//         divDiversificada.style.display = "block"

//         const navGeral = getItem("geral");
//         const navDiversificada = getItem("diversificada");

//         desativaItem(navGeral);
//         ativaItem(navDiversificada);
//     }

//     const diversificadaVoltar = (evento) => {
//         evento.preventDefault();

//         const divDiversificada = document.querySelector("[data-form-diversificada]");
//         divDiversificada.style.display = "none";

//         const divGeral = document.querySelector("[data-form-geral]");
//         divGeral.style.display = "block"

//         const navDiversificada = getItem("diversificada");
//         const navGeral = getItem("geral");

//         desativaItem(navDiversificada);
//         ativaItem(navGeral);
//     }


//     if(botaoGeralAvancar != null)
//         botaoGeralAvancar.addEventListener("click", geralAvancar);

//     if(botaoDiversificadaVoltar != null)
//         botaoDiversificadaVoltar.addEventListener("click", diversificadaVoltar);
// }

inicializaElementos();