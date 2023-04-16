// Script para acessar o perfil de um aluno ao clicar na tabela

const retornaId = (elemento) => {
    const celula = elemento.cells[0];
    const id = celula.innerHTML;

    return id;
};

const inicializaTabela = () => {
    const linhasAlunos = document.querySelectorAll("[data-tabela-aluno]");
    let link = "/dinem/aluno_perfil";

    linhasAlunos.forEach((aluno) => {
        aluno.onclick = () => {
            window.location.href = link.concat("?id=").concat(retornaId(aluno));
        }
    });
};

inicializaTabela();