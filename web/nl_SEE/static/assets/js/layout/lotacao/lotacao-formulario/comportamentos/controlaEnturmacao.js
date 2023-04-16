// Script para controlar a adição e exclusão de enturmações no formulário de lotação

(() => {
    const containerEnturmacao = document.querySelector('[data-form-container="enturmacao"]')

    const botaoAdicionarEnturmacao = containerEnturmacao.querySelector('[data-adicionar-enturmacao]')
    const containerBotoes = botaoAdicionarEnturmacao.parentElement

    let contadorEnturmacao = 1
    let contadorTurma = 1
    let contadorRota = 1

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Função que retorna um container com uma nova seleção de turma
    const ContainerTurma = (contadorEnturmacao, contadorTurma) => {
        const div = document.createElement('div')

        const html = `
            <select id="campo-turma-escola${contadorEnturmacao}_${contadorTurma}" class="campo-texto campo-medio" name="turma_escola${contadorEnturmacao}_${contadorTurma}" data-selecao-turma></select>
            <button class="botao botao--vermelho" data-botao-excluir-turma>Excluir turma</button>
        `

        div.innerHTML = html

        const selecaoTurma = containerEnturmacao.querySelector('[data-selecao-turma]')
        const novaSelecao = div.querySelector('[data-selecao-turma]')

        novaSelecao.innerHTML = selecaoTurma.innerHTML

        return div
    }

    // Função que retorna um container com um novo container de enturmação
    const ContainerEnturmacao = (contadorEnturmacao, contadorTurma) => {
        const selecaoDisciplina = containerEnturmacao.querySelector('#campo-disciplina1')

        const div = document.createElement('div')
        div.toggleAttribute('data-container-enturmacao')

        const html = `
            <div class="formulario-grupo">
                <fieldset id="fieldset-tipo-disciplina${contadorEnturmacao}">
                    <input type="radio" name="fieldset-tipo-disciplina${contadorEnturmacao}" value="disciplina" id="radio-disciplina${contadorEnturmacao}" checked data-radio-disciplina>
                    <label class="texto-preto" for="radio-disciplina${contadorEnturmacao}">Disciplinas regulares</label>

                    <input type="radio" name="fieldset-tipo-disciplina${contadorEnturmacao}" value="rota" id="radio-rota${contadorEnturmacao}" data-radio-disciplina>
                    <label class="texto-preto" for="radio-rota${contadorEnturmacao}">Rotas</label>
                </fieldset>
            </div>

            <div data-grupo-disciplina class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-disciplina${contadorEnturmacao}">Disciplina</label>

                <select id="campo-disciplina${contadorEnturmacao}" name="disciplina${contadorEnturmacao}" class="campo-texto campo-medio">
                    ${selecaoDisciplina.innerHTML}
                </select>
            </div>

            <div data-grupo-rota class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-rota${contadorEnturmacao}">Rota</label>

                <select id="campo-rota${contadorEnturmacao}" name="rota${contadorEnturmacao}" class="campo-texto campo-medio">
                    <option value="CHSA">CHSA</option>
                    <option value="CNT">CNT</option>
                    <option value="LGG">LGG</option>
                    <option value="MAT">MAT</option>
                </select>

                <input type="text" name="rota_auxilia${contadorEnturmacao}_${contadorRota}" class="campo-texto campo-medio oculto" readonly>
            </div>

            <div data-selecao-rota="CHSA" class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-chsa${contadorEnturmacao}_${contadorRota}">CHSA</label>

                <div>
                    <select id="campo-chsa${contadorEnturmacao}_${contadorRota}" name="chsa${contadorEnturmacao}_${contadorRota}" class="campo-texto campo-medio">
                        <option value="2U1S1">2U1S1</option>
                        <option value="2U2S1">2U2S1</option>
                        <option value="2U3S1">2U3S1</option>
                        <option value="2U4S1">2U4S1</option>
                        <option value="2U1S2">2U1S2</option>
                        <option value="2U2S2">2U2S2</option>
                        <option value="2U3S2">2U3S2</option>
                        <option value="2U4S2">2U4S2</option>
                        <option value="3U1S1">3U1S1</option>
                        <option value="3U2S1">3U2S1</option>
                        <option value="3U3S1">3U3S1</option>
                        <option value="3U4S1">3U4S1</option>
                        <option value="3U5S1">3U5S1</option>
                        <option value="3U6S1">3U6S1</option>
                        <option value="3U1S2">3U1S2</option>
                        <option value="3U2S2">3U2S2</option>
                        <option value="3U3S2">3U3S2</option>
                        <option value="3U4S2">3U4S2</option>
                        <option value="3U5S2">3U5S2</option>
                        <option value="3U6S2">3U6S2</option>
                    </select>

                    <button class="botao botao--azul" data-botao-adicionar-rota>Adicionar Rota</button>
                </div>
            </div>

            <div data-selecao-rota="CNT" class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-cnt${contadorEnturmacao}_${contadorRota}">CNT</label>

                <div>
                    <select id="campo-cnt${contadorEnturmacao}_${contadorRota}" name="cnt${contadorEnturmacao}_${contadorRota}" class="campo-texto campo-medio">
                            <option value="2U1S1">2U1S1</option>
                            <option value="2U2S1">2U2S1</option>
                            <option value="2U3S1">2U3S1</option>
                            <option value="2U4S1">2U4S1</option>
                            <option value="2U1S2">2U1S2</option>
                            <option value="2U2S2">2U2S2</option>
                            <option value="2U3S2">2U3S2</option>
                            <option value="2U4S2">2U4S2</option>
                            <option value="3U1S1">3U1S1</option>
                            <option value="3U2S1">3U2S1</option>
                            <option value="3U3S1">3U3S1</option>
                            <option value="3U4S1">3U4S1</option>
                            <option value="3U5S1">3U5S1</option>
                            <option value="3U6S1">3U6S1</option>
                            <option value="3U1S2">3U1S2</option>
                            <option value="3U2S2">3U2S2</option>
                            <option value="3U3S2">3U3S2</option>
                            <option value="3U4S2">3U4S2</option>
                            <option value="3U5S2">3U5S2</option>
                            <option value="3U6S2">3U6S2</option>
                    </select>

                    <button class="botao botao--azul" data-botao-adicionar-rota>Adicionar Rota</button>
                </div>
            </div>

            <div data-selecao-rota="LGG" class="formulario-grupo oculto">
                <label class="texto-azul label-campo" for="campo-lgg${contadorEnturmacao}_${contadorRota}">LGG</label>

                <div>
                    <select id="campo-lgg${contadorEnturmacao}_${contadorRota}" name="lgg${contadorEnturmacao}_${contadorRota}" class="campo-texto campo-medio">
                        <option value="2U1S1">2U1S1</option>
                        <option value="2U2S1">2U2S1</option>
                        <option value="2U3S1">2U3S1</option>
                        <option value="2U4S1">2U4S1</option>
                        <option value="2U1S2">2U1S2</option>
                        <option value="2U2S2">2U2S2</option>
                        <option value="2U3S2">2U3S2</option>
                        <option value="2U4S2">2U4S2</option>
                        <option value="3U1S1">3U1S1</option>
                        <option value="3U2S1">3U2S1</option>
                        <option value="3U3S1">3U3S1</option>
                        <option value="3U4S1">3U4S1</option>
                        <option value="3U5S1">3U5S1</option>
                        <option value="3U1S2">3U1S2</option>
                        <option value="3U2S2">3U2S2</option>
                        <option value="3U3S2">3U3S2</option>
                        <option value="3U4S2">3U4S2</option>
                        <option value="3U5S2">3U5S2</option>
                    </select>

                    <button class="botao botao--azul" data-botao-adicionar-rota>Adicionar Rota</button>
                </div>
            </div>

            <div data-selecao-rota="MAT" class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-mat${contadorEnturmacao}_${contadorRota}">MAT</label>

                <div>
                    <select id="campo-mat${contadorEnturmacao}_${contadorRota}" name="mat${contadorEnturmacao}_${contadorRota}" class="campo-texto campo-medio">
                            <option value="2U1S1">2U1S1</option>
                            <option value="2U2S1">2U2S1</option>
                            <option value="2U3S1">2U3S1</option>
                            <option value="2U4S1">2U4S1</option>
                            <option value="2U1S2">2U1S2</option>
                            <option value="2U2S2">2U2S2</option>
                            <option value="2U3S2">2U3S2</option>
                            <option value="2U4S2">2U4S2</option>
                            <option value="3U1S1">3U1S1</option>
                            <option value="3U2S1">3U2S1</option>
                            <option value="3U3S1">3U3S1</option>
                            <option value="3U4S1">3U4S1</option>
                            <option value="3U5S1">3U5S1</option>
                            <option value="3U1S2">3U1S2</option>
                            <option value="3U2S2">3U2S2</option>
                            <option value="3U3S2">3U3S2</option>
                            <option value="3U4S2">3U4S2</option>
                            <option value="3U5S2">3U5S2</option>
                    </select>

                    <button class="botao botao--azul" data-botao-adicionar-rota>Adicionar Rota</button>
                </div>
            </div>

            <div class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-carga-horaria${contadorEnturmacao}">Carga Horária por turma</label>

                <input class="campo-texto campo-pequeno" type="text" name="carga_turma${contadorEnturmacao}" id="campo-carga-horaria${contadorEnturmacao}" placeholder="Ex: 20" maxlength="3" required>
            </div>
        `

        div.innerHTML = html

        const grupoTurma = document.createElement('div')
        grupoTurma.classList.add('formulario-grupo')
        grupoTurma.toggleAttribute('data-grupo-turma')

        grupoTurma.innerHTML = `
            <label class="texto-azul label-campo" for="campo-turma-escola${contadorEnturmacao}_${contadorTurma}">Turma</label>

            <div>
                <select name="turma_escolar${contadorEnturmacao}_${contadorTurma}" id="campo-turma-escola${contadorEnturmacao}_${contadorTurma}" class="campo-texto campo-medio" data-selecao-turma></select>
                <button class="botao botao--azul" data-botao-adicionar-turma>Adicionar Turma</button>
            </div>
        `

        div.appendChild(grupoTurma)

        const selecaoTurma = containerEnturmacao.querySelector('[data-selecao-turma]')

        const novaSelecao = grupoTurma.querySelector('[data-selecao-turma]')

        novaSelecao.innerHTML = selecaoTurma.innerHTML

        const containerBotoes = document.createElement('div')
        containerBotoes.classList.add('container-botoes')

        containerBotoes.innerHTML = `
            <button class="botao botao--vermelho" data-botao-excluir-enturmacao>Excluir Enturmação</button>
        `

        div.appendChild(containerBotoes)

        return div
    }

    // FUNÇÕES PARA O COMPORTAMENTO DAS ROTAS NO FOMRULÁRIO

    const controlaExibicaoSelecaoRota = (selecao, operador) => {
        const campoAuxiliar = selecao.nextElementSibling
        campoAuxiliar.value = selecao.value

        controlaExibicao(selecao, operador)
        controlaExibicao(campoAuxiliar, !operador)
    }

    // Função que adiciona um campo de rota no formulário
    const adicionaRota = (evento) => {
        evento.preventDefault()

        contadorRota++

        const botao = evento.target
        const grupo = botao.parentElement.parentElement
        const container = grupo.parentElement

        const selecaoRota = grupo.querySelector('select')

        // Adicionando o novo campo de rota
        const novaDiv = document.createElement('div')

        const html = `
            <select class="campo-texto campo-medio">${selecaoRota.innerHTML}</select>
            <button class="botao botao--vermelho" data-botao-excluir-rota>Excluir</button>
        `

        novaDiv.innerHTML = html

        // Adicionando o name da nova seleção
        const novaSelecao = novaDiv.querySelector('select')
        const novoName = selecaoRota.name.replace(/\d_\d/g, `${contadorEnturmacao}_${contadorRota}`)
        novaSelecao.name = novoName

        grupo.appendChild(novaDiv)

        inicializaBotoesExcluirRota()

        // Atualizando os elementos de acordo com o comportamento
        const fieldset = container.querySelector('fieldset')
        const radioDisciplina = fieldset.children[0]
        const labelDisciplnas = fieldset.children[1]

        const grupoRota = container.querySelector('[data-grupo-rota]')
        const selecaoTipoRota = grupoRota.querySelector('select')

        controlaExibicaoSelecaoRota(selecaoTipoRota, false)

        controlaExibicao(radioDisciplina, false)
        controlaExibicao(labelDisciplnas, false)

        const botaoAdicionarTurma = container.querySelector('[data-botao-adicionar-turma]')
        botaoAdicionarTurma.disabled = true
    }

    // Função para excluir um campo de rota
    const excluiRota = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const pai = botao.parentElement
        const grupo = pai.parentElement
        const container = grupo.parentElement

        // Excluindo a div da rota
        pai.remove()

        // Atualizando os elementos de acordo com o comportamento
        const fieldset = container.querySelector('fieldset')
        const radioDisciplina = fieldset.children[0]
        const labelDisciplnas = fieldset.children[1]

        const qtdSelecoes = grupo.querySelectorAll('select').length

        controlaExibicao(radioDisciplina, qtdSelecoes == 1)
        controlaExibicao(labelDisciplnas, qtdSelecoes == 1)

        const grupoRota = container.querySelector('[data-grupo-rota]')
        const selecaoTipoRota = grupoRota.querySelector('select')

        controlaExibicaoSelecaoRota(selecaoTipoRota, qtdSelecoes == 1)

        const botaoAdicionarTurma = container.querySelector('[data-botao-adicionar-turma]')
        botaoAdicionarTurma.disabled = qtdSelecoes > 1
    }

    // Função para inicializar os botões de excluir gerados na adição de rotas
    const inicializaBotoesExcluirRota = () => {
        const botoesExcluir = containerEnturmacao.querySelectorAll('[data-botao-excluir-rota]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiRota)
        })
    }

    const inicializaBotoesAdicionarRota = () => {
        const botoesAdicionar = containerEnturmacao.querySelectorAll('[data-botao-adicionar-rota]')

        botoesAdicionar.forEach((botao) => {
            botao.addEventListener('click', adicionaRota)
        })
    }

    inicializaBotoesAdicionarRota()

    // Função que controla quais rotas serão exibidas
    const inicializaCamposRotas = () => {
        const container = containerEnturmacao.querySelectorAll('[data-container-enturmacao]')

        container.forEach((container) => {
            const radiosUnidade = container.querySelectorAll('[data-radio-disciplina]')
            const radioDisciplina = radiosUnidade[0]
            const radioRota = radiosUnidade[1]

            const grupoDisciplinas = container.querySelector('[data-grupo-disciplina]')

            const grupoRotas = container.querySelector('[data-grupo-rota]')
            const selecaoRota = grupoRotas.querySelector('select')

            const selecoesRotas = container.querySelectorAll('[data-selecao-rota]')

            // Função para controlar o comportamento do formulário de acordo com a seleção de disciplinas ou rotas
            const controlaTipoDisicplina = () => {
                const validaRota = radioRota.checked

                controlaExibicao(grupoRotas, validaRota)
                controlaExibicao(grupoDisciplinas, !validaRota)
            }

            controlaTipoDisicplina()
            radioDisciplina.addEventListener('click', controlaTipoDisicplina)
            radioRota.addEventListener('click', controlaTipoDisicplina)

            // Função para controlar as seleções de rotas apresentadas de acordo com a rota selecionada
            const controlaRota = () => {
                const rotaSelecionada = selecaoRota.value

                selecoesRotas.forEach((selecao) => {
                    const atributo = selecao.dataset.selecaoRota
                    const validaRota = (atributo == rotaSelecionada) && radioRota.checked

                    controlaExibicao(selecao, validaRota)
                })
            }

            controlaRota()
            radioDisciplina.addEventListener('click', controlaRota)
            radioRota.addEventListener('click', controlaRota)
            selecaoRota.addEventListener('change', controlaRota)
        })
    }

    inicializaCamposRotas()

    // FUNÇÕES PARA O COMPORTAMENTO DOS CAMPOS DE TURMA NO FORMULÁRIO

    // Função que adiciona uma selecao de turma dentro de uma enturmação
    const adicionaSelecaoTurma = (evento) => {
        evento.preventDefault()
        const botao = evento.target
        const selecao = botao.previousElementSibling

        // Adicionando a seleção
        const contador = selecao.name.split('_')[1].replace('escolar', '')

        contadorTurma++

        const formularioGrupo = botao.parentElement.parentElement

        formularioGrupo.appendChild(ContainerTurma(contador, contadorTurma))

        inicializaBotoesExcluirTurma()

        // Atualizando os elementos de acordo com o comportamento
        const container = formularioGrupo.parentElement
        const botoesAdicionarRota = container.querySelectorAll('[data-botao-adicionar-rota]')

        botoesAdicionarRota.forEach((botao) => {
            botao.disabled = true
        })
    }

    // Função que exclui uma selecao de turma dentro de uma enturmação
    const excluiTurma = (evento) => {
        evento.preventDefault()
        const botao = evento.target
        const div = botao.parentElement
        const container = div.parentElement.parentElement

        // Excluindo a div de seleção de turma
        div.remove()

        // Atualizando os elementos de acordo com o comportamento
        const qtdSelecoes = container.querySelectorAll('[data-selecao-turma]').length

        const botoesAdicionarRota = container.querySelectorAll('[data-botao-adicionar-rota]')

        botoesAdicionarRota.forEach((botao) => {
            botao.disabled = qtdSelecoes > 1
        })
    }

    // Função para inicializar os botões de adicionar uma seleção de turma dentro das enturmações
    const inicializaBotoesAdicionarTurma = () => {
        const botoesAdicionar = containerEnturmacao.querySelectorAll('[data-botao-adicionar-turma]')

        botoesAdicionar.forEach((botao) => {
            botao.addEventListener('click', adicionaSelecaoTurma)
        })
    }

    inicializaBotoesAdicionarTurma()

    // Função para inicializar os botões de excluir uma seleção de turma dentro das enturmações
    const inicializaBotoesExcluirTurma = () => {
        const botoesExcluir = containerEnturmacao.querySelectorAll('[data-botao-excluir-turma]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiTurma)
        })
    }

    // FUNÇÕES PARA O COMPORTAMENTO DOS CAMPOS DE TURMA NO FORMULÁRIO

    // Função para adicionar um container de enturmação no formulário
    const adicionaEnturmacao = (evento) => {
        evento.preventDefault()

        contadorEnturmacao++
        contadorTurma++

        const hr = document.createElement('hr')
        hr.classList.add('formulario-grupo')

        containerEnturmacao.insertBefore(hr, containerBotoes)
        containerEnturmacao.insertBefore(ContainerEnturmacao(contadorEnturmacao, contadorTurma), containerBotoes)

        inicializaCamposRotas()
        inicializaBotoesAdicionarRota()
        inicializaBotoesAdicionarTurma()
        inicializaBotoesExcluirEnturmacao()
    }

    botaoAdicionarEnturmacao.addEventListener('click', adicionaEnturmacao)

    const excluiEnturmacao = (evento) => {
        evento.preventDefault
        const botao = evento.target

        const container = botao.parentElement.parentElement
        const hr = container.previousElementSibling

        hr.remove()
        container.remove()
    }

    const inicializaBotoesExcluirEnturmacao = () => {
        const botoesExcluir = containerEnturmacao.querySelectorAll('[data-botao-excluir-enturmacao]')

        botoesExcluir.forEach((botao) => {
            botao.addEventListener('click', excluiEnturmacao)
        })
    }
})

()