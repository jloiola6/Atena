function abreUnidade(elemento){
    const inep = retornaINEP(elemento);
    
    const novoLink = "unidade_perfil?inep=".concat(inep);

    window.location.href = novoLink;
}

function retornaINEP(elemento){
    const celula = elemento.cells[0];
    const inep = celula.innerHTML;

    return inep;
}