// Scripts para exibir corretamente os dados de histórico das Unidades

const corrigeHoras = () => {
    const horas = document.querySelectorAll("[data-unidade-historico-hora]");

    let string, novaString;

    horas.forEach((hora) => {
        string = hora.innerHTML;
        novaString = string.split(" ")[1];
        hora.innerHTML = (novaString);
    });
};

const modificacoes = document.querySelectorAll("[data-unidade-historico-modificacao]");

let string, novaString;

modificacoes.forEach((modificacao) => {
    string = modificacao.innerHTML;

    // Removendo as chaves
    novaString = string.replaceAll("{", "").replaceAll("}", "");

    // Corrigindo os nomes de atributos
    novaString = novaString.replaceAll("'cod_inep'", "<b>INEP</b>");
    novaString = novaString.replaceAll("'nome_escola'", "<b>Nome</b>");
    novaString = novaString.replaceAll("'cod_turmalina'", "<b>Turmalina</b>");
    novaString = novaString.replaceAll("'dependencia_adm'", "<b>Dependência Administrativa</b>");
    novaString = novaString.replaceAll("'cnpj'", "<b>CNPJ</b>");

    // Removendo os parenteses e virgulas
    novaString = novaString.replaceAll("('", "de ").replaceAll("', '", " para ").replaceAll("')", "");
    novaString = novaString.replaceAll(",", "<br>");

    // novaString.forEach((campo) => {
    //     campo = campo.replaceAll("('", "de ").replaceAll("', '", " para ");
    //     console.log(campo);
    // });

    // console.log(novaString);

    modificacao.innerHTML = (novaString);
});

corrigeHoras();