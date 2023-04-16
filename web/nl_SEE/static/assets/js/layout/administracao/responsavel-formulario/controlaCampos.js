// Script para controlar os campos no formulário da página de perfil de um aluno

(() => {
    const selecaoEstados = document.querySelector('[data-selecao-estado]')
    const selecaoCidades = document.querySelector('[data-selecao-cidade]')
    const opcoesCidades = selecaoCidades.children

    const carregarCidades = () => {
        
        const siglaEstado = selecaoEstados.value
    
        let primeiroSelecionado = true

        Array.from(opcoesCidades).forEach((opcao) => {
            const idCidade = opcao.getAttribute('data-cidade-estado')

            if(siglaEstado == idCidade){
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
})

()