// Script para encapsular uma função que retorna o modal de formulário de um novo aluno

const selecaoEstadosAux = document.querySelector('[data-selecao-estado-aux]')

const estados = [...selecaoEstadosAux.options].map((opcao) => {
    return {id: opcao.value, nome: opcao.textContent, sigla: opcao.dataset.estadoSigla }
})

const selecaoCidadesAux = document.querySelector('[data-selecao-cidade-aux]')

const cidades = [...selecaoCidadesAux.options].map((opcao) => {
    return {id: opcao.value, nome: opcao.textContent, estado: opcao.dataset.estado}
})

selecaoEstadosAux.parentElement.remove()

const preencheCidades = (estado) => {
    return cidades.filter((cidade) => cidade.estado == estado)
}

const ModalNovoAluno = (contador) => {
    const div = document.createElement('div')
    div.classList.add('modal')
    div.setAttribute('data-modal', `data-novo-aluno${contador}`)
    div.toggleAttribute('data-modal-bloqueado')

    const html = `
        <div class="modal-conteudo">
            <h3 class="texto-medio texto-azul">Novo aluno</h3>
            <p class="texto-preto descricao">Insira os dados do aluno</p>

            <div class="formulario-grupo">
                <label for="campo-nome-aluno" class="texto-azul label-campo">Nome</label>
                <input type="text" name="nome-aluno${contador}" id="campo-nome-aluno" class="campo-texto campo-grande" value="" placeholder="Ex: João Pedro Soares" maxlength="100" autocomplete="off">
            </div>

            <div class="formulario-grupo">
                <label for="campo-cpf-aluno" class="texto-azul label-campo">CPF</label>
                <input type="text" name="cpf-aluno${contador}" id="campo-cpf-aluno" class="campo-texto campo-pequeno" value="" placeholder="Ex: 000.000.000-00" data-mascara="cpf" autocomplete="off" maxlength="11">
            </div>

            <div class="formulario-grupo">
                <label for="nascimento-aluno" class="texto-azul label-campo">Data de nascimento</label>
                <input type="date" name="nascimento-aluno${contador}" id="nascimento-aluno" value="" class="campo-texto campo-medio">
            </div>

            <div class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-sexo-aluno">Gênero</label>
                <select name="sexo-aluno${contador}" id="campo-sexo-aluno" class="campo-texto campo-pequeno">
                    <option value=""></option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                    <option value="T">Transgênero</option>
                    <option value="N">Não binário</option>
                    <option value="O">Outro</option>
                </select>
            </div>

            <div class="formulario-grupo">
                <label class="label-campo texto-azul" for="aluno-pai">Nome completo do pai</label>
                <input class="campo-texto campo-grande" name="pai-aluno${contador}" value="" id="aluno-pai" type="text" placeholder="Ex: Fábio Santos Moreira">
            </div>

            <div class="formulario-grupo">
                <label class="label-campo texto-azul" for="aluno-mae">Nome completo da mãe</label>
                <input class="campo-texto campo-grande" name="mae-aluno${contador}" value="" id="aluno-mae" type="text" placeholder="Ex: Fabiana Santos Moreira">
            </div>

            <div class="formulario-grupo">
                <label class="label-campo texto-azul" for="aluno-nacionalidade">Nacionalidade</label>

                <select class="campo-texto campo-pequeno" name="nacionalidade-aluno${contador}" id="aluno-nacionalidade">
                    <option value=""></option>
                    <option value="Brasileiro(a)">Brasileiro(a)</option>
                    <option value="Estrangeiro(a)">Estrangeiro(a)</option>
                </select>
            </div>

            <div class="formulario-grupo">
                <label class="label-campo texto-azul" for="aluno-naturalidade-estado">Naturalidade (estado)</label>

                <select id="aluno-naturalidade-estado" name="estado-aluno${contador}" class="campo-grande campo-texto" data-selecao-estado>
                    <option value=""></option>
                    ${estados.map(estado => `<option value="${estado.sigla}" data-estado-id="${estado.id}">${estado.nome}</option>`)}
                </select>
            </div>

            <div class="formulario-grupo">
                <label class="label-campo texto-azul" for="aluno-naturalidade-municipio">Naturalidade (município)</label>

                <select id="aluno-naturalidade-municipio" name="naturalidade-aluno${contador}" class="campo-grande campo-texto" data-selecao-cidade>
                    <option value=""></option>
                </select>
            </div>

            <div class="container-botoes">
                <button class="botao--verde botao" data-salvar-aluno>Salvar</button>
                <button class="botao--vermelho botao" data-cancelar-aluno>Cancelar</button>
            </div>
        </div>
    `

    div.innerHTML = html

    const selecaoEstado = div.querySelector('[data-selecao-estado]')
    const selecaoCidade = div.querySelector('[data-selecao-cidade]')

    const constroiSelecaoCidade = () => {
        const estadoSelecionado = selecaoEstado[selecaoEstado.selectedIndex].dataset.estadoId
        const cidadesGeradas = preencheCidades(estadoSelecionado)

        selecaoCidade.innerHTML = `
            <option value=""></option>
            ${cidadesGeradas.map((cidade) => `<option value="${cidade.nome}">${cidade.nome}</option>`)}
        `
    }

    selecaoEstado.addEventListener('change', constroiSelecaoCidade)

    return div
}