(() => {
    // Script para controlar o comportamento do formulário de escolaridade de um servidor
    const selecaoFormacao = document.querySelector('[data-selecao-formacao]')

    const containerEscola = document.querySelector('[data-container-escola]')
    const containerMagisterio = document.querySelector('[data-container-magisterio]')

    const selecaoEscola = containerEscola.querySelector('[data-selecao-escola]')
    const novaEscola = containerEscola.querySelector('[data-nova-escola]')

    const radioEscolaExistente = containerEscola.querySelector('[data-radio-escola-existente]')
    const radioEscolaNova = containerEscola.querySelector('[data-radio-escola-nova]')

    const containerSuperior = document.querySelector('[data-container-superior]')

    const radioConcluido = containerSuperior.querySelector('[data-radio-concluido]')
    const radioCursando = containerSuperior.querySelector('[data-radio-cursando]')

    const grupoConclusao = document.querySelector('[data-grupo-conclusao]')

    // Função genérica para controlar a exibição de um elemento
    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Função para controlar o formulário de acordo com o tipo de formação selecionada
    const controlaTipo = () => {
        const formacaoSelecionada = selecaoFormacao.value

        if(formacaoSelecionada == 'Ensino Médio'){
            const validaMedio = formacaoSelecionada == 'Ensino Médio'
            controlaExibicao(containerEscola, validaMedio)
            controlaExibicao(containerSuperior, !validaMedio)
            controlaExibicao(containerMagisterio, !validaMedio)
        }else if(formacaoSelecionada == 'Ensino Médio - Magistério'){
            const validaMagisterio = formacaoSelecionada == 'Ensino Médio - Magistério'
            controlaExibicao(containerMagisterio, validaMagisterio)
            controlaExibicao(containerSuperior, !validaMagisterio)
            controlaExibicao(containerEscola, !validaMagisterio)
        }else{
            const validaSuperior = ['Tecnólogo', 'Bacharelado', 'Licenciatura', 'Doutorado', 'Mestrado', 'Pós-Graduação'].includes(formacaoSelecionada)
            controlaExibicao(containerSuperior, validaSuperior)
            controlaExibicao(containerMagisterio, !validaSuperior)
            controlaExibicao(containerEscola, !validaSuperior)
        }
    }

    controlaTipo()
    selecaoFormacao.addEventListener('change', controlaTipo)

    // Função para controlar o campo de data de conclusão de acordo com a opção selecionada
    const controlaConclusao = () => {
        if(containerSuperior.classList.contains('oculto')){
            controlaExibicao(grupoConclusao, true)
            return
        }

        const concluido = radioConcluido.checked

        controlaExibicao(grupoConclusao, concluido)
    }

    controlaConclusao()
    selecaoFormacao.addEventListener('change', controlaConclusao)
    radioConcluido.addEventListener('click', controlaConclusao)
    radioCursando.addEventListener('click', controlaConclusao)
})

()