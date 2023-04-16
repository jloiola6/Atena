// ADICIONAR REQUIRED

export const FormularioGrupo = (contador, tipoContrato) => {
    const div = document.createElement('div')

    const grupoTitulo = document.createElement('div')
    grupoTitulo.classList.add('formulario-grupo')

    const tituloItem = document.createElement('h3')
    tituloItem.textContent = 'Item do contrato'
    tituloItem.classList.add('texto-medio')
    tituloItem.classList.add('texto-azul')

    grupoTitulo.appendChild(tituloItem)

    const grupoCampos = document.createElement('div')
    grupoCampos.classList.add('contrato-item-grupo-campos')

    const grupoNumero = document.createElement('div')
    grupoNumero.classList.add('formulario-grupo')

    const labelNumero = document.createElement('label')
    labelNumero.textContent = 'N° do item'
    labelNumero.classList.add('texto-azul')
    labelNumero.classList.add('label-campo')

    const inputNumero = document.createElement('input')
    inputNumero.name = 'numero_item' + contador
    inputNumero.maxLength = 3
    inputNumero.classList.add('campo-texto')
    inputNumero.classList.add('campo-item-numero')
    inputNumero.toggleAttribute('data-mascara')
    inputNumero.setAttribute('data-mascara', 'numero')

    grupoNumero.appendChild(labelNumero)
    grupoNumero.appendChild(inputNumero)

    const grupoLote = document.createElement('div')
    grupoLote.classList.add('formulario-grupo')

    const labelLote = document.createElement('label')
    labelLote.textContent = 'N° do lote'
    labelLote.classList.add('texto-azul')
    labelLote.classList.add('label-campo')

    const inputLote = document.createElement('input')
    inputLote.name = 'numero_lote' + contador
    inputLote.maxLength = 3
    // inputLote.required = true
    inputLote.classList.add('campo-texto')
    inputLote.classList.add('campo-item-numero')
    inputLote.toggleAttribute('data-mascara')
    inputLote.setAttribute('data-mascara', 'numero')

    grupoLote.appendChild(labelLote)
    grupoLote.appendChild(inputLote)

    const grupoQtd = document.createElement('div')
    grupoQtd.classList.add('formulario-grupo')

    const labelQtd = document.createElement('label')
    labelQtd.textContent = 'Quantidade'
    labelQtd.classList.add('texto-azul')
    labelQtd.classList.add('label-campo')

    const inputQtd = document.createElement('input')
    inputQtd.name = 'quantidade' + contador
    inputQtd.maxLength = 6
    // inputQtd.required = true
    inputQtd.classList.add('campo-texto')
    inputQtd.classList.add('campo-item-numero')
    inputQtd.toggleAttribute('data-mascara')
    inputQtd.setAttribute('data-mascara', 'numero')
    inputQtd.toggleAttribute('data-qtd-item')

    grupoQtd.appendChild(labelQtd)
    grupoQtd.appendChild(inputQtd)

    const grupoValor = document.createElement('div')
    grupoValor.classList.add('formulario-grupo')

    const labelValor = document.createElement('label')
    labelValor.textContent = 'Valor unitário'
    labelValor.classList.add('texto-azul')
    labelValor.classList.add('label-campo')

    const inputValor = document.createElement('input')
    inputValor.name = 'valor_unitário' + contador
    inputValor.maxLength = 30
    // inputValor.required = true
    inputValor.classList.add('campo-texto')
    inputValor.classList.add('campo-item-valor')
    inputValor.toggleAttribute('data-mascara')
    inputValor.setAttribute('data-mascara', 'moeda')
    inputValor.toggleAttribute('data-unitario-item')

    grupoValor.appendChild(labelValor)
    grupoValor.appendChild(inputValor)

    const grupoRemuneracao = document.createElement('div')
    grupoRemuneracao.classList.add('formulario-grupo')
    grupoRemuneracao.toggleAttribute('data-item-remuneracao')

    if(!tipoContrato.includes('Postos de trabalho')){
        grupoRemuneracao.classList.add('oculto')
    }

    const labelRemuneracao = document.createElement('label')
    labelRemuneracao.textContent = 'Remuneração'
    labelRemuneracao.classList.add('texto-azul')
    labelRemuneracao.classList.add('label-campo')

    const inputRemuneracao = document.createElement('input')
    inputRemuneracao.name = 'remuneracao' + contador
    inputRemuneracao.maxLength = 30
    inputRemuneracao.classList.add('campo-texto')
    inputRemuneracao.classList.add('campo-item-valor')
    inputRemuneracao.toggleAttribute('data-mascara')
    inputRemuneracao.setAttribute('data-mascara', 'moeda')

    grupoRemuneracao.appendChild(labelRemuneracao)
    grupoRemuneracao.appendChild(inputRemuneracao)

    const grupoValorTot = document.createElement('div')
    grupoValorTot.classList.add('formulario-grupo')

    const labelValorTot = document.createElement('label')
    labelValorTot.textContent = 'Valor total'
    labelValorTot.classList.add('texto-azul')
    labelValorTot.classList.add('label-campo')

    const inputValorTot = document.createElement('input')
    inputValorTot.name = 'valor_total' + contador
    inputValorTot.maxLength = 30
    inputValorTot.readOnly = true
    // inputValorTot.readOnly = true
    inputValorTot.classList.add('campo-texto')
    inputValorTot.classList.add('campo-item-valor')
    inputValorTot.toggleAttribute('data-mascara')
    inputValorTot.setAttribute('data-mascara', 'moeda')
    inputValorTot.toggleAttribute('data-total-item')

    grupoValorTot.appendChild(labelValorTot)
    grupoValorTot.appendChild(inputValorTot)

    grupoCampos.appendChild(grupoNumero)
    grupoCampos.appendChild(grupoLote)
    grupoCampos.appendChild(grupoQtd)
    grupoCampos.appendChild(grupoValor)
    grupoCampos.appendChild(grupoRemuneracao)
    grupoCampos.appendChild(grupoValorTot)

    const grupoDesricao = document.createElement('div')
    grupoDesricao.classList.add('formulario-grupo')

    const labelDesricao = document.createElement('label')
    labelDesricao.textContent = 'Descrição'
    labelDesricao.classList.add('texto-azul')
    labelDesricao.classList.add('label-campo')

    const inputDesricao = document.createElement('input')
    inputDesricao.name = 'descricao' + contador
    inputDesricao.maxLength = 300
    // inputDesricao.required = true
    inputDesricao.classList.add('campo-texto')
    inputDesricao.classList.add('campo-item-descricao')

    grupoDesricao.appendChild(labelDesricao)
    grupoDesricao.appendChild(inputDesricao)

    const containerBotoes = document.createElement('div')
    containerBotoes.classList.add('container-botoes')

    const botaoExcluir = document.createElement('button')
    botaoExcluir.textContent = 'Excluir'
    botaoExcluir.toggleAttribute('data-botao-excluir-item')
    botaoExcluir.classList.add('botao')
    botaoExcluir.classList.add('botao--vermelho')

    containerBotoes.appendChild(botaoExcluir)

    div.appendChild(grupoTitulo)
    div.appendChild(grupoCampos)
    div.appendChild(grupoDesricao)
    div.appendChild(containerBotoes)

    return div
}