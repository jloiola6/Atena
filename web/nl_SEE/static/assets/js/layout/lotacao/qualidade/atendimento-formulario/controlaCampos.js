// Script para controlar o comportamento do formulário de serviço
(() => {
    const grupoServicoNovo = document.querySelector('[data-grupo-servico-novo]')
    const campoServico = grupoServicoNovo.querySelector('#campo-servico-novo')

    const grupoServicoExistente = document.querySelector('[data-grupo-servico-existente]')

    const grupoAtendente = document.querySelector('[data-grupo-atendente]')

    const radioServicoExistente = document.querySelector('[data-radio-servico-existente]')
    const radioServicoNovo = document.querySelector('[data-radio-servico-novo]')

    const controlaExibicao = (elemento, operador) => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    const controlaServico = () => {
        const validaExistente = radioServicoExistente.checked

        controlaExibicao(grupoServicoExistente, validaExistente)
        controlaExibicao(grupoServicoNovo, !validaExistente)
        controlaExibicao(grupoAtendente, validaExistente)

        campoServico.required = !validaExistente
    }

    controlaServico()
    radioServicoExistente.addEventListener('click', controlaServico)
    radioServicoNovo.addEventListener('click', controlaServico)
})

()