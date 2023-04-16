// Script para controlar o comportamento do modal de pre-visualização do formulário

(() => {
    const botaoModal = document.querySelector('[data-modal-abrir="confirmar"]')

    const campoOrgao = document.querySelector('[data-campo-orgao]')
    const previewOrgao = document.querySelector('[data-preview-orgao]')

    const campoSubconta = document.querySelector('[data-campo-subconta]')
    const previewSubconta = document.querySelector('[data-preview-subconta]')

    const campoCH = document.querySelector('[data-campo-ch]')
    const previewCH = document.querySelector('[data-preview-ch]')

    const fieldsetTurno = document.getElementById('fieldset-turno')
    const previewTurno = document.querySelector('[data-preview-turno]')

    const campoDataInicio = document.querySelector('[data-campo-data-inicio]')
    const previewDataInicio = document.querySelector('[data-preview-data-inicio]')

    const campoDataFinalizacao = document.querySelector('[data-campo-data-finalizacao]')
    const previewDataFinalizacao = document.querySelector('[data-preview-data-finalizacao]')

    const campoObservacao = document.querySelector('[data-campo-observacao]')
    const previewObservacao = document.querySelector('[data-preview-observacao]')

    // ELEMENTOS PARA CASO O SERVIDOR TENHA NÚMERO DE PORTARIA
    const campoPortaria = document.querySelector('[data-campo-portaria]')
    const previewPortaria = document.querySelector('[data-preview-portaria]')

    const campoDoePortaria = document.querySelector('[data-campo-doe-portaria')
    const previewDoePortaria = document.querySelector('[data-preview-doe-portaria]')

    // ELEMENTO PARA A FUNÇÃO DE PROFESSOR AEE
    const containerEnturmacaoProfessorAEE = document.querySelector('[data-form-container="professor-aee"]')

    // ELEMENTOS PARA A FUNÇÃO DE PROFESSOR
    const containerEnturmacao = document.querySelector('[data-form-container="enturmacao"]')

    // ELEMENTOS PARA A FUNÇÃO DE ATENDENTE DOMICILIAR, MEDIADOR, ETC...
    const containerEnturmacaoAEE = document.querySelector('[data-form-container="enturmacao-aee"]')
    const containerAlunosAEE = document.querySelector('[data-form-container="alunos-aee"]')

    // ELEMENTOS PARA A FUNÇÃO DE PROFESSOR EM UNIDADE ADM
    const containerEnturmacaoAdm = document.querySelector('[data-form-container="enturmacao-adm"]')

    const previewTurmas = document.querySelector('[data-preview-turmas]')
    const previewAlunos = document.querySelector('[data-preview-alunos]')
    const previewDisciplina = document.querySelector('[data-preview-disciplina]')

    const preencheColunas = () => {
        if(campoOrgao){
            previewOrgao.textContent = `Para: ${campoOrgao.value}`
        }

        previewSubconta.textContent = campoSubconta[campoSubconta.selectedIndex].textContent

        if(campoPortaria){
            previewPortaria.textContent = campoPortaria.value
            previewDoePortaria.textContent = campoDoePortaria.value
        }

        if(campoCH){
            previewCH.textContent = campoCH.value

            if(campoCH.value != '')
                previewCH.textContent += 'H'
        }

        if(fieldsetTurno){
            const inputsMarcados = [...fieldsetTurno.elements].filter((input) => input.checked)

            if(inputsMarcados.length > 0){
                const labels = inputsMarcados.map((input) => input.labels[0].textContent)

                previewTurno.textContent = labels.toString().replace(',', ', ')
            }

        }

        previewDataInicio.textContent = campoDataInicio.value

        if(campoDataFinalizacao)
            previewDataFinalizacao.textContent = campoDataFinalizacao.value

        previewObservacao.textContent = campoObservacao.value

        // PREENCHENDO O PREVIEW DE TURMAS DE UM PROFESSOR AEE
        if(containerEnturmacaoProfessorAEE){
            const grupoTurmas = containerEnturmacaoProfessorAEE.querySelector('[data-grupo-turma]')
            const selecoesTurma = grupoTurmas.querySelectorAll('select')

            const turmas = [...selecoesTurma].map((selecao) => selecao[selecao.selectedIndex].textContent)

            let html = ''

            turmas.forEach((turma) => {
                html += `
                    <p class="">${turma}</p>
                `
            })

            previewTurmas.innerHTML = html
        }

        // PREECHENDO O PREVIEW DE TURMAS DE UM PROFESSOR
        if(containerEnturmacao){
            let html = ''

            const containers = containerEnturmacao.querySelectorAll('[data-container-enturmacao]')

            containers.forEach((container) => {
                const fieldset = container.querySelector('fieldset')
                const radioDisciplinas = fieldset.elements[0]

                if(radioDisciplinas.checked){
                    const grupoDisciplina = container.querySelector('[data-grupo-disciplina]')
                    const selecaoDisciplina = grupoDisciplina.querySelector('select')

                    const disciplina = selecaoDisciplina[selecaoDisciplina.selectedIndex].textContent

                    const grupoTurmas = container.querySelector('[data-grupo-turma]')
                    const selecoesTurma = grupoTurmas.querySelectorAll('select')

                    const turmasSelecionadas = [...selecoesTurma].map((selecao) => {
                        return selecao[selecao.selectedIndex].textContent
                    })

                    html += `
                        <p class="">${disciplina} | ${turmasSelecionadas.toString().replace(',', ', ')}</p>
                    `


                }else{
                    const grupoTipoRota = container.querySelector('[data-grupo-rota]')
                    const selecaoTipoRota = grupoTipoRota.querySelector('select')

                    const rota = selecaoTipoRota.value

                    const grupoRota = container.querySelector(`[data-selecao-rota="${rota}"]`)

                    const selecoesRota = grupoRota.querySelectorAll('select')

                    const rotasSelecionadas = [...selecoesRota].map((selecao) => selecao.value)

                    const grupoTurmas = container.querySelector('[data-grupo-turma]')
                    const selecoesTurma = grupoTurmas.querySelectorAll('select')

                    const turmasSelecionadas = [...selecoesTurma].map((selecao) => {
                        return selecao[selecao.selectedIndex].textContent
                    })

                    if(rotasSelecionadas.length > 1){
                        rotasSelecionadas.forEach((rotaSelecionada) => {
                            html += `
                                <p class="">${rota} - ${rotaSelecionada} | ${turmasSelecionadas[0]}</p>
                            `
                        })
                    }else{
                        turmasSelecionadas.forEach((turma) => {
                            html += `
                                <p class="">${rota} - ${rotasSelecionadas[0]} | ${turma}</p>
                            `
                        })
                    }

                }

                previewTurmas.innerHTML = html
            })
        }

        // PREENCHENDO O PREVIEW DE TURMAS E ALUNO DE UM ATENDENTE DOMICILIAR, MEDIADOR, ETC...
        if(containerEnturmacaoAEE){
            let html = ''

            const selecaoTurma = containerEnturmacaoAEE.querySelector('[data-selecao-turma-aee]')
            const turma = selecaoTurma[selecaoTurma.selectedIndex].textContent

            const selecoesAlunos = containerAlunosAEE.querySelectorAll('[data-selecao-alunos]')

            const alunosSelecionados = [...selecoesAlunos].map((selecao) => selecao[selecao.selectedIndex].textContent)

            alunosSelecionados.forEach((aluno) => {
                html += `
                    <p class="">${aluno} - ${turma}</p>
                `
            })

            previewAlunos.innerHTML = html
        }

        // PREENCHENDO O PREVIEW DE DISCIPLINA DE UM PROFESSOR EM UNIDADE ADMINISTRATIVA
        if(containerEnturmacaoAdm){
            let html = ''

            const selecaoDisciplina = containerEnturmacaoAdm.querySelector('select')
            const disciplina = selecaoDisciplina[selecaoDisciplina.selectedIndex].textContent

            html += `
                <p>${disciplina}</p>
            `

            previewDisciplina.innerHTML = html
        }
    }

    botaoModal.addEventListener('click', preencheColunas)
})

()