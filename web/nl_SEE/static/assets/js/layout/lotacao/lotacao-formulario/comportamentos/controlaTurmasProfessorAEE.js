(() => {
    const container = document.querySelector('[data-form-container="professor-aee"]')
    
    const linkFormulario = container.querySelector('[data-link-formulario-turma]')

    const spansEtapas = container.querySelectorAll('[data-escola-etapa]')
    
    const listaEtapas = [...spansEtapas].map((span) => {
        const etapa = {
            id: span.dataset.escolaEtapa,
            etapa: span.textContent
        }

        span.remove()

        return etapa
    })

    console.log(listaEtapas)

    let contador = 1

    // Função genérica para controlar a exibição de elementos
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Função para abrir um novo modal de uma nova turma
    const abrirModalTurma = (evento) => {
        const modal = ModalNovaTurma(contador, listaEtapas)

        const botaoCancelar = modal.querySelector('[data-cancelar-turma]')
        botaoCancelar.addEventListener('click', fechaModalTurma)

        const botaoSalvar = modal.querySelector('[data-salvar-turma]')
        botaoSalvar.addEventListener('click', adicionaTurma)

        container.appendChild(modal)

        inicializaSelecoesModais()

        const selecaoEtapa = modal.querySelector('[data-selecao-etapa]')
        selecaoEtapa.addEventListener('change', inicializaSelecoesModais)

        contador++
    }

    linkFormulario.addEventListener('click', abrirModalTurma)

    const adicionaTurma = (evento) => {
        evento.preventDefault()
        
        const botao = evento.target
        const modal = botao.parentElement.parentElement.parentElement

        const grupoAno = modal.querySelector('[data-grupo-ano]')
        let selecaoAno

        const selecoesAno = grupoAno.querySelectorAll('select')
        
        selecoesAno.forEach((selecao) => {
            if(!selecao.classList.contains('oculto'))
                selecaoAno = selecao
        })

        const ano = selecaoAno.value

        const grupoTurma = modal.querySelector('[data-grupo-turma]')
        let selecaoTurma

        const selecoesTurma = grupoTurma.querySelectorAll('select')

        selecoesTurma.forEach((selecao) => {
            if(!selecao.classList.contains('oculto'))
                selecaoTurma = selecao
        })

        const turma = selecaoTurma.value

        const selecaoTurno = modal.querySelector('[data-selecao-turno]')
        const turno = selecaoTurno.value

        const valor = `${ano} ${turma} - ${turno}`

        adicionaOpcaoTurma(valor)

        modal.classList.add('oculto')
    }

    // Função que adiciona a turma preenchida no modal nas opções das seleções
    const adicionaOpcaoTurma = (valor) => {
        const selecoesTurma = document.querySelectorAll('[data-selecao-turma]')

        const html = `
            <option value="${contador-1}nova_turma">${valor}</option>
        `

        let auxValor

        selecoesTurma.forEach((selecao) => {
            auxValor = selecao.value
            selecao.innerHTML += html
            selecao.value = auxValor
        })
    }

    const fechaModalTurma = (evento) => {
        evento.preventDefault()

        const botao = evento.target
        const modal = botao.parentElement.parentElement.parentElement

        modal.remove()

        contador--
    }

    // Função que adiciona o comportamento do modal
    const inicializaSelecoesModais = () => {
        const selecoesEtapas = document.querySelectorAll('[data-selecao-etapa]')
        
        if(selecoesEtapas)
            selecoesEtapas.forEach((selecao) => {
                const etapaSelecionada = selecao.value
                const modal = selecao.parentElement.parentElement

                const selecaoModulo = modal.querySelector('[data-selecao-eja]')

                const selecoesAno = modal.querySelectorAll('[data-selecao-ano]')
                const selecaoTurma= modal.querySelector('[data-selecao-letra]')

                selecoesAno.forEach((selecaoAno) => {
                    const atributo = selecaoAno.dataset.selecaoAno

                    const validaEtapa = (atributo == etapaSelecionada)

                    controlaExibicao(selecaoAno, validaEtapa)
                })

                const etapasEja = ['7', '8', '9', '12']
                const validaEja = etapasEja.includes(etapaSelecionada)

                controlaExibicao(selecaoModulo, validaEja)
                controlaExibicao(selecaoTurma, !validaEja)
            })
    }
})

()