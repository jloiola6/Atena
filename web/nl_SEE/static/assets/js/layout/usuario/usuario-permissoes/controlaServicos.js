// Script para controlar a exibição de serviços de acordo com a aplicação selecionada pelo usuário

(() => {
    const selecaoAplicacoes = document.querySelector("[data-selecao-aplicacao]")
    const selecaoServicos = document.querySelector("[data-selecao-servico]")

    const opcoesServicos = document.querySelectorAll("[data-opcao-servico]")

    const campoInep = document.querySelector("[data-campo-inep]")

    const carregarServicos = () => {
        const idAplicacao = selecaoAplicacoes.value

        let primeiroSelecionado = false

        opcoesServicos.forEach((opcao) => {
            const valueServico = opcao.value
            const idServicoAplicacao = opcao.getAttribute("data-opcao-servico")

            
            if(idAplicacao != idServicoAplicacao)
                opcao.classList.add("oculto")
            else{
                opcao.classList.remove("oculto")
                verificaServicoGestor()
                const selecionado = opcao.getAttribute("data-opcao-servico-selecionado") == "true"

                if(!primeiroSelecionado || selecionado){
                    selecaoServicos.value = valueServico
                    primeiroSelecionado = true
                }
                
            }
        })
    }

    const exibeCampoInep = (operador) => {
        const inputInep = campoInep.lastElementChild
        inputInep.required = operador

        if(operador)
            campoInep.classList.remove("oculto")
        
        else
            campoInep.classList.add("oculto")
    }


    const verificaServicoGestor = () => {
        const servicoSelecionado = selecaoServicos.options[selecaoServicos.selectedIndex]

        if(servicoSelecionado != undefined){
            if(servicoSelecionado.text == "Gestor Escolar")
                exibeCampoInep(true)
            else
                exibeCampoInep(false)
        }
    }

    const cadastro = document.querySelector('[data-pagina-cadastro]')

    const cadastroHabilitado = cadastro.getAttribute('data-pagina-cadastro') == 'true'
    
    if(cadastroHabilitado){
        
        selecaoAplicacoes.addEventListener("change", carregarServicos)
        selecaoServicos.addEventListener("change", verificaServicoGestor)
        
        carregarServicos()
        verificaServicoGestor()
    }
    
})

()