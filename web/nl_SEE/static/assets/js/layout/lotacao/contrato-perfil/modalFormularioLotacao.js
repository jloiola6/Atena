// Script para controlar o comportamento do modal que encaminha para o formulário de lotação

(() => {
    const selecaoTipoLotacao = document.querySelector('[data-selecao-tipo-lotacao]')

    const selecaoTipoUnidade = document.querySelector('[data-selecao-tipo-unidade]')
    const radioEscola = document.querySelector('[data-radio-escola]')
    const radioAdm = document.querySelector('[data-radio-adm]')

    const selecaoEscola = document.querySelector('[data-selecao-escola]')
    const selecaoAdm = document.querySelector('[data-selecao-adm]')

    const selecaoFuncaoEscola = document.querySelector('[data-selecao-funcao-escola]')
    const selecaoFuncaoAdm = document.querySelector('[data-selecao-funcao-adm]')
    const selecaoFuncao = document.querySelector('[data-selecao-funcao]')


    // Função genérica para controlar a exibição dos elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Comportamento para determinar quais funções serão apresentadas no modal
    const controlaTipoUnidade = () => {
        const tipoLotacao = selecaoTipoLotacao.value

        if(['Sem Lotação'].includes(tipoLotacao))
            return

        const validaEscola = radioEscola.checked

        controlaExibicao(selecaoFuncaoEscola, validaEscola)
        controlaExibicao(selecaoFuncaoAdm, !validaEscola)
        controlaExibicao(selecaoFuncao, false)

        if(['Cedido', 'Permuta'].includes(tipoLotacao)){
            controlaExibicao(selecaoEscola, false)
            controlaExibicao(selecaoAdm, false)
            controlaExibicao(selecaoFuncaoEscola, false)
            controlaExibicao(selecaoFuncaoAdm, false)
            controlaExibicao(selecaoFuncao, true)

            return
        }

        controlaExibicao(selecaoEscola, validaEscola)
        controlaExibicao(selecaoAdm, !validaEscola)
    }

    radioEscola.addEventListener('click', controlaTipoUnidade)
    radioAdm.addEventListener('click', controlaTipoUnidade)

    // Função para controlar as seleções de acordo com o tipo de lotação selecionado
    const controlaTipoLotacao = () => {
        const tipoLotacao = selecaoTipoLotacao.value

        if (tipoLotacao == 'Sem Lotação') {
            controlaExibicao(selecaoTipoUnidade, false)

            controlaExibicao(selecaoEscola, false)
            controlaExibicao(selecaoAdm, false)

            controlaExibicao(selecaoFuncao, false)
            controlaExibicao(selecaoFuncaoEscola, false)
            controlaExibicao(selecaoFuncaoAdm, false)

        } else if (tipoLotacao.includes('Cedido') || tipoLotacao.includes('Permuta')) {
            controlaExibicao(selecaoTipoUnidade, false)

            controlaExibicao(selecaoEscola, false)
            controlaExibicao(selecaoAdm, false)

            controlaExibicao(selecaoFuncaoEscola, false)
            controlaExibicao(selecaoFuncaoAdm, false)

            controlaExibicao(selecaoFuncao)
        } else {
            controlaExibicao(selecaoTipoUnidade, true)
        }

        controlaTipoUnidade()
    }

    controlaTipoLotacao()
    selecaoTipoLotacao.addEventListener('change', controlaTipoLotacao)



    // /
    // const controlaTipoLotacao = () => {
    //     const tipoSelecionado = selecaoTipoLotacao.value

    //     // Comportamento para caso o servidor não possua nenhuma lotação
    //     const validaTipo = ['Sem Lotação'].includes(tipoSelecionado)

    //     controlaExibicao(selecaoTipoUnidade, !validaTipo)
    //     controlaExibicao(selecaoEscola, !validaTipo)
    //     controlaExibicao(selecaoAdm, !validaTipo)


    //     controlaExibicao(selecaoFuncaoEscola, !validaTipo)
    //     controlaExibicao(selecaoFuncaoAdm, !validaTipo)

    //     controlaTipoUnidade()
    // }

    // controlaTipoLotacao()
    // selecaoTipoLotacao.addEventListener('change', controlaTipoLotacao)


})

()