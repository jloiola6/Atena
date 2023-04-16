// Script para controlar os campos no formulário da página de perfil de um aluno

(() => {
    const selecaoEstados = document.querySelector('[data-selecao-estado]')
    const selecaoCidades = document.querySelector('[data-selecao-cidade]')
    const opcoesCidades = selecaoCidades.children
    
    const carregarCidades = () => {
        
        const idEstado = selecaoEstados.value

        let primeiroSelecionado = true

        Array.from(opcoesCidades).forEach((opcao) => {
            const idCidade = opcao.getAttribute('data-cidade-estado')

            if(idEstado == idCidade){
                opcao.classList.remove('oculto')

                if(primeiroSelecionado){
                    selecaoCidades.value = opcao.value
                    primeiroSelecionado = false
                }
            }else{
                opcao.classList.add('oculto')
            }
        })
    }

    selecaoEstados.addEventListener('change', carregarCidades)

    carregarCidades()

    const selecaoNaturalidade = document.querySelector('[data-selecao-naturalidade]')
    const camposNaturalidade = document.querySelector('[data-naturalidade-brasileira]')
})

()