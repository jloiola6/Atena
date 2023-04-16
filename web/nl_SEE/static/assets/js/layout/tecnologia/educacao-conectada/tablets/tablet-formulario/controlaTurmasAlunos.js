// Script para controlar o comportamento da sessão de Aluno no formulário de cadastro de um tablet
(() => {
    const formulario = document.querySelector('[data-container-formulario]')

    const containerAlunos = formulario.querySelector('[data-container-alunos]')

    const selecaoTurma = formulario.querySelector('[data-selecao-turma]')

    const mensagemSemAlunos = formulario.querySelector('[data-sem-aluno]')

    const botaoModal = formulario.querySelector('[data-modal-abrir="confirmar"]')

    let inputsEquipamento

    let contador

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const ContainerAluno = (contador, aluno) => {
        const div = document.createElement('div')

        const id = aluno[0]
        const nome = aluno[1]
        const cad = aluno[2] == 1 ? 'Sim' : 'Não'

        const html = `
            <hr class="formulario-grupo">

            <input class="oculto" type="text" value="${id}" name="aluno${contador}" readonly>

            <div class="formulario-grupo">
                <p class=" texto-azul texto-negrito">Aluno: <span class="texto-normal texto-preto">${nome}</span></p>
                <p class=" texto-azul texto-negrito">Possui cad. único: <span class="texto-normal texto-preto">${cad}</span></p>
            </div>

            <div class="grupo-equipamento">
                <div class="formulario-grupo">
                    <label for="campo-tablet-serial${contador}" class="label-campo texto-azul">Tablet (Serial)</label>
                    <input id="campo-tablet-serial${contador}" name="tablet_serial${contador}" class="campo-texto campo-medio" type="text" autocomplete="off" data-campo-equipamento>
                </div>

                <div class="formulario-grupo">
                    <label for="campo-tablet-imei${contador}" class="label-campo texto-azul">Tablet (IMEI)</label>
                    <input id="campo-tablet-imei${contador}" name="tablet_imei${contador}" class="campo-texto campo-medio" type="text" autocomplete="off" data-campo-equipamento>
                </div>

                <div class="formulario-grupo">
                    <label for="campo-chip-serial${contador}" class="label-campo texto-azul">Chip (Serial)</label>
                    <input id="campo-chip-serial${contador}" name="chip_serial${contador}" class="campo-texto campo-medio" type="text" autocomplete="off" data-campo-equipamento>
                </div>
            </div>
        `

        div.innerHTML = html

        return div
    }

    // Funções assíncronas para buscar os alunos de uma turma via API
    const getAlunos = async (id) => {
        const url = `${window.location.origin}/api/ec/aluno/turma`

        try{
            const response = await fetch(`${url}?id=${id}`)
            const json = await response.json()

            return json
        }catch(erro){
            console.log('Erro na requisição')
            console.log(`Detalhes: ${erro}`)
        }
    }

    const constroiListaAlunos = async (id) => {
        const dados = await getAlunos(id)

        const lista = dados.map(dado => [dado.aluno__id, dado.aluno__nome, dado.aluno__bolsa_familia])
        return lista
    }

    // Função que constrói a seleção de alunos de acordo com o retorno da API
    const atualizaSelecaoAlunos = async () => {
        const id = selecaoTurma.value
        const alunos = await constroiListaAlunos(id)

        // Validação da existencia de alunos cadastrados na turma
        const validaAlunos = alunos.length > 0

        containerAlunos.innerHTML = ''

        if(validaAlunos){
            contador = 1

            alunos.forEach((aluno) => {
                containerAlunos.appendChild(ContainerAluno(contador, aluno))
                contador++
            })
        }

        controlaExibicao(mensagemSemAlunos, !validaAlunos)

        inputsEquipamento = formulario.querySelectorAll('[data-campo-equipamento]')
    }

    atualizaSelecaoAlunos()
    selecaoTurma.addEventListener('change', atualizaSelecaoAlunos)

    // Definindo eventos para o formulário
    const comportamentoFormulario = (evento) => {
        if(evento.key == 'Enter'){
            evento.preventDefault()

            const campo = evento.target
            const valor = campo.value

            const tamanhoLista = inputsEquipamento.length

            if(valor.length > 0)
                inputsEquipamento.forEach((input, indice) => {
                    if(campo == input)
                        if(indice != tamanhoLista-1)
                            inputsEquipamento[indice+1].focus()
                })
            }
    }

    formulario.addEventListener('keydown', comportamentoFormulario)
})

()