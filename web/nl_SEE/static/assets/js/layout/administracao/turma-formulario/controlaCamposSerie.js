// Script para controlar os selects que vão ser mostrados e ocultados
(() => {
    const grupoEtapa= document.querySelector('[data-selecao-etapas]')
    const selecaoEtapa = grupoEtapa.querySelector('#campo-etapa')
    const selecoesEtapas= document.querySelectorAll('[data-selecao-etapa]')
    const selecaoModulo= document.querySelector('[data-selecao-eja]')
    const selecaoTurma= document.querySelector('[data-selecao-turma]')

    const controlaExibicao = (elemento, operador)  => {
        if(operador)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }
    const controlaEtapas = () =>{
        
        const etapaSelecionada = selecaoEtapa.value

        selecoesEtapas.forEach((selecao)=>{
            const atributo = selecao.dataset.selecaoEtapa
            const validaEtapa =( atributo == etapaSelecionada)

            controlaExibicao(selecao, validaEtapa)

        
        })
        
        const etapasEja = ['7', '8', '9', '12']
        const validaEja = etapasEja.includes(etapaSelecionada)

        controlaExibicao(selecaoModulo, validaEja)
        controlaExibicao(selecaoTurma, !validaEja)



    } 
    controlaEtapas()
    selecaoEtapa.addEventListener('change', controlaEtapas)
        
})

()