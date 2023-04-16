// Script para controlar os campos de situação de lotação para confirmação

(() => {
    const formularios = document.querySelectorAll('[data-formulario-confirmacao]')

    // Função genérica para controlar a exibicao de elementos
    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    formularios.forEach((formulario) => {
        const radioSituacaoCorreta = formulario.querySelector('[data-radio-situacao-correta]')
        const radioSituacaoIncorreta = formulario.querySelector('[data-radio-situacao-incorreta]')

        const grupoTipoUnidade = formulario.querySelector('[data-grupo-tipo-unidade]')

        const radioTipoUnidadeEscolar = formulario.querySelector('[data-radio-tipo-unidade-escolar]')
        const radioTipoUnidadeAdm = formulario.querySelector('[data-radio-tipo-unidade-adm]')

        const grupoEscola = formulario.querySelector('[data-grupo-escola]')
        const grupoAdm = formulario.querySelector('[data-grupo-adm]')

        const botaoSubmissao = formulario.querySelector('button[type="submit"]')

        const controlaSituacao = () => {
            const validaSitacao = radioSituacaoCorreta.checked


            controlaExibicao(grupoTipoUnidade, !validaSitacao)
            controlaExibicao(grupoEscola, !validaSitacao)
            controlaExibicao(grupoAdm, !validaSitacao)

            controlaTipo()
        }

        radioSituacaoCorreta.addEventListener('click', controlaSituacao)
        radioSituacaoIncorreta.addEventListener('click', controlaSituacao)

        const controlaTipo = () => {
            const validaSitacao = radioSituacaoCorreta.checked
            const validaEscola = radioTipoUnidadeEscolar.checked

            controlaExibicao(grupoEscola, validaEscola && !validaSitacao)
            controlaExibicao(grupoAdm, !validaEscola && !validaSitacao)
        }

        radioTipoUnidadeEscolar.addEventListener('click', controlaTipo)
        radioTipoUnidadeAdm.addEventListener('click', controlaTipo)

        controlaSituacao()

        formulario.onsubmit = () => {
            botaoSubmissao.disabled = true
        }
    })
})

()