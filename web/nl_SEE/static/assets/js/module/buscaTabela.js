(() => {
    const tabelaPrincipal = document.querySelector('[data-busca-tabela-principal]')
    const tabelaBusca = document.querySelector('[data-busca-tabela]')
    const linhasBusca = [...tabelaBusca.rows]

    const colunasBusca = tabelaBusca.querySelectorAll('[data-busca-tabela-coluna]')

    const camposBusca = document.querySelectorAll('[data-busca-tabela-campo]')

    const spanErro = document.querySelector('[data-busca-tabela-erro]')

    if(tabelaBusca){

        const controlaExibicao = (elemento, operador) => {
            if(operador)
            elemento.classList.remove('oculto')
            else
            elemento.classList.add('oculto')
        }

        controlaExibicao(tabelaBusca, false)
        controlaExibicao(spanErro, false)

        const limpaCampos = (campo) => {
            camposBusca.forEach((campoBusca) => {
                if(campo != campoBusca)
                campoBusca.value = ''
            })
        }

        const busca = (evento) => {
            const campo = evento.target
            const campoValor = campo.value

            const valorValido = campoValor.trim().length > 0

            if (valorValido){
                const campoAtributo = campo.dataset.buscaTabelaCampo

                let ocorrencias = 0

                limpaCampos(campo)

                colunasBusca.forEach((coluna) => {
                    const colunaAtributo = coluna.dataset.buscaTabelaColuna

                    if(colunaAtributo == campoAtributo){
                        const colunaValor = coluna.textContent

                        const linha = coluna.parentElement

                        const validaValor = colunaValor.toUpperCase().includes(campoValor.toUpperCase())

                        controlaExibicao(linha, validaValor)

                        if(validaValor)
                            ocorrencias++
                    }
                })

                controlaExibicao(spanErro, ocorrencias == 0)
                controlaExibicao(tabelaBusca, ocorrencias > 0)
            }else{
                controlaExibicao(tabelaBusca, valorValido)
                controlaExibicao(spanErro, valorValido)
            }

            controlaExibicao(tabelaPrincipal, !valorValido)
        }

        camposBusca.forEach((campo) => {
            campo.addEventListener('input', busca)
        })
    }

})

()