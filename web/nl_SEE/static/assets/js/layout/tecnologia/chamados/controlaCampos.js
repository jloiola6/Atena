// Script para controlar a exibição dos campos no modal de Adicionar Chamado

(() => {
    const radioAdm = document.querySelector('[data-radio-adm]')
    const radioEscola = document.querySelector('[data-radio-escola]')

    const grupoAdm = document.querySelector('[data-grupo-adm]')
    const grupoEscola = document.querySelector('[data-grupo-escola]')

    const grupoTipoChamado = document.querySelector('[data-grupo-tipo-chamado]')
    const selecaoTipoChamado = grupoTipoChamado.querySelector('select')
    const inputTipoChamado = grupoTipoChamado.querySelector('input')

    // Função genérica para controlar a exibição de campos
    const controlaCampos = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaTipoUnidade = () => {
        const validaAdm = radioAdm.checked

        controlaCampos(grupoAdm, validaAdm)
        controlaCampos(grupoEscola, !validaAdm)

        controlaCampos(selecaoTipoChamado, validaAdm)
        controlaCampos(inputTipoChamado, !validaAdm)
    }

    controlaTipoUnidade()
    radioAdm.addEventListener('click', controlaTipoUnidade)
    radioEscola.addEventListener('click', controlaTipoUnidade)
})

()