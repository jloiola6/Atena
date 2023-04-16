// Script para controlar a exibição dos campos no formulário de item no de inventário

(() => {
    const selecaoTipo = document.querySelector('[data-selecao-tipo-item]')

    const selecaoEquipamento = document.querySelector('[data-selecao-equipamento]')
    
    const exibe = (elemento, exibicao) => {
        if(exibicao)
            elemento.classList.remove('oculto')
        else
            elemento.classList.add('oculto')
    }

    // Carregar os campos de acordo com o Tipo de Item selecionado

    const carregaCamposTipoEquipamento = () => {
        const tipoSelecionado = selecaoTipo.value

        const campoPatrimonio = document.querySelector('[data-campo-patrimonio]')
        const campoMarca = document.querySelector('[data-campo-marca]')
        const campoModelo = document.querySelector('[data-campo-modelo]')
        const campoDescricao = document.querySelector('[data-campo-descricao]')
        const campoQuantidade = document.querySelector('[data-campo-quantidade]')

        switch (tipoSelecionado) {
            case 'mobilia':
                exibe(campoPatrimonio, true)
                exibe(campoMarca, false)
                exibe(campoModelo, false)
                exibe(campoDescricao, false)
                exibe(campoQuantidade, false)
                break;

            case 'eletronico':
            case 'eletrodomestico':
                exibe(campoPatrimonio, true)
                exibe(campoMarca, true)
                exibe(campoModelo, true)
                exibe(campoDescricao, false)
                exibe(campoQuantidade, false)
                break;
                
            case 'insumo':
                exibe(campoPatrimonio, false)
                exibe(campoMarca, false)
                exibe(campoModelo, false)
                exibe(campoDescricao, true)
                exibe(campoQuantidade, true)
                break;
        }
    }

    // Carregar os itens de acordo com o Tipo de Item selecionado

    const carregaEquipamentos = () => {
        const tipoSelecionado = selecaoTipo.value

        let primeiroSelecionado = false

        for (let i = 0; i < selecaoEquipamento.length; i++) {
            const opcaoEquipamento = selecaoEquipamento[i]
            const tipoEquipamento = opcaoEquipamento.getAttribute('data-equipamento-tipo')

            
            if(tipoEquipamento == tipoSelecionado){
                exibe(opcaoEquipamento, true)

                if(!primeiroSelecionado){
                    selecaoEquipamento.value = opcaoEquipamento.value
                    primeiroSelecionado = true
                }
            }
            else
                exibe(opcaoEquipamento, false)
        }

        carregaCampos()
    }

    // Carregar campos de acordo com o Item selecionado

    const controlaRequired = () => {
        const campos = document.querySelectorAll('.campo-texto')
        
        campos.forEach((campo) => {
            const oculto = campo.parentElement.classList.contains('oculto') || campo.parentElement.parentElement.classList.contains('oculto')

            campo.required = !oculto
        })
    }

    const carregaCampos = () => {
        const equipamentoSelecionado = selecaoEquipamento.options[selecaoEquipamento.selectedIndex].textContent

        let campoExibido

        switch (equipamentoSelecionado) {
            case 'Utensílios de cozinha':
            case 'Materiais Escolar':
                campoExibido = 'insumo'
                break

            case 'Quadro':
                campoExibido = 'quadro'
                break

            case 'Fogão':
                campoExibido = 'fogao'
                break

            case 'Liquidificador':
                campoExibido = 'liquidificador'
                break

            case 'Ar Condicionado':
                campoExibido = 'ac'
                break

            case 'Geladeira':
            case 'Freezer':
                campoExibido = 'geladeira'
                break

            case 'Switch':
                campoExibido = 'switch'
                break

            case 'Impressora':
                campoExibido = 'impressora'
                break

            case 'Projetor':
                campoExibido = 'projetor'
                break

            case 'Nobreak':
                campoExibido = 'nobreak'
                break

            case 'Computador/Notebook':
                campoExibido = 'computador'
                break
                
            case 'Cadeira':
                campoExibido = 'cadeira'
                break

            case 'Mesa':
                campoExibido = 'mesa'
                break

            case 'Armário':
                campoExibido = 'armario'
                break

            case 'Estante':
                campoExibido = 'estante'
                break;
            
        }

        const camposForm = document.querySelectorAll('[data-form]')
        const tipoSelecionado = selecaoTipo.value

        camposForm.forEach((campo) => {
            const atributo = campo.getAttribute('data-form')
            
            exibe(campo, atributo == campoExibido)
            
        })
        controlaRequired()
        // console.log(equipamentoSelecionado, campoExibido, tipoSelecionado)
    }

    selecaoTipo.addEventListener('change', carregaCamposTipoEquipamento)
    selecaoTipo.addEventListener('change', carregaEquipamentos)
    selecaoEquipamento.addEventListener('change', carregaCampos)
    carregaCamposTipoEquipamento()
    carregaEquipamentos()

})

()