(() => {

    const tratarEspecificacoes = (especificacoes) => {
        const lista = especificacoes.replace('{', '').replace('}', '').replaceAll("\n", '').trim().split(',')

        return lista
    }

    const getValor = (string) => {
        const valor = string.split(':')[1]

        return valor.replaceAll("'", '')
    }

    const computadores = document.querySelectorAll('[data-item-tipo="Computador/Notebook"]')

    computadores.forEach((computador) => {

        const patrimonio = computador.getAttribute('data-item-patrimonio')
        const marca = computador.getAttribute('data-item-marca')
        const modelo = computador.getAttribute('data-item-modelo')


        const especificacoes = computador.textContent

        const pai = computador.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-computador-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-computador-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-computador-modelo]')
            modalModelo.textContent = modelo

            const computadorEspecificacoes = tratarEspecificacoes(especificacoes)

            const processador = computadorEspecificacoes[0]
            const ram = computadorEspecificacoes[1]
            const disco = computadorEspecificacoes[2]
            const ssd = computadorEspecificacoes[3]
            const placa = computadorEspecificacoes[4]
            const tipo = computadorEspecificacoes[5]
            const cor = computadorEspecificacoes[6]

            const modalTipo = document.querySelector('[data-computador-tipo]')
            modalTipo.textContent = getValor(tipo)

            const modalProcessador = document.querySelector('[data-computador-processador]')
            modalProcessador.textContent = getValor(processador)

            const modalRam = document.querySelector('[data-computador-ram]')
            modalRam.textContent = getValor(ram)

            const modalDisco = document.querySelector('[data-computador-disco]')
            modalDisco.textContent = getValor(disco)

            const modalSsd = document.querySelector('[data-computador-ssd]')
            modalSsd.textContent = getValor(ssd)

            const modalPlaca = document.querySelector('[data-computador-placa]')
            modalPlaca.textContent = getValor(placa)

            const modalCor = document.querySelector('[data-computador-cor]')
            modalCor.textContent = getValor(cor)

            const id = computador.getAttribute('data-item-id')
            const tipoItemId = computador.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-computador-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const impressoras = document.querySelectorAll('[data-item-tipo="Impressora"]')

    impressoras.forEach((impressora) => {

        const patrimonio = impressora.getAttribute('data-item-patrimonio')
        const marca = impressora.getAttribute('data-item-marca')
        const modelo = impressora.getAttribute('data-item-modelo')

        const especificacoes = impressora.textContent

        const pai = impressora.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-impressora-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-impressora-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-impressora-modelo]')
            modalModelo.textContent = modelo

            const impressoraEspecificacoes = tratarEspecificacoes(especificacoes)

            const tipo = impressoraEspecificacoes[0]
            const conexao = impressoraEspecificacoes[1]

            const modalTipo = document.querySelector('[data-impressora-tipo]')
            modalTipo.textContent = getValor(tipo)

            const modalConexao = document.querySelector('[data-impressora-conexao]')
            modalConexao.textContent = getValor(conexao)

            const id = impressora.getAttribute('data-item-id')
            const tipoItemId = impressora.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-impressora-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const nobreaks = document.querySelectorAll('[data-item-tipo="Nobreak"]')

    nobreaks.forEach((nobreak) => {

        const patrimonio = nobreak.getAttribute('data-item-patrimonio')
        const marca = nobreak.getAttribute('data-item-marca')
        const modelo = nobreak.getAttribute('data-item-modelo')

        const especificacoes = nobreak.textContent

        const pai = nobreak.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-nobreak-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-nobreak-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-nobreak-modelo]')
            modalModelo.textContent = modelo

            const nobreakEspecificacoes = tratarEspecificacoes(especificacoes)

            const tomadas = nobreakEspecificacoes[0]
            const estabilizador = nobreakEspecificacoes[1]

            const modalTomadas = document.querySelector('[data-nobreak-tomadas]')
            modalTomadas.textContent = getValor(tomadas)

            const modalEstabilizador = document.querySelector('[data-nobreak-estabilizador]')
            modalEstabilizador.textContent = getValor(estabilizador)

            const id = nobreak.getAttribute('data-item-id')
            const tipoItemId = nobreak.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-nobreak-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const projetores = document.querySelectorAll('[data-item-tipo="Projetor"]')

    projetores.forEach((projetor) => {

        const patrimonio = projetor.getAttribute('data-item-patrimonio')
        const marca = projetor.getAttribute('data-item-marca')
        const modelo = projetor.getAttribute('data-item-modelo')

        const especificacoes = projetor.textContent

        const pai = projetor.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-projetor-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-projetor-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-projetor-modelo]')
            modalModelo.textContent = modelo

            const projetorEspecificacoes = tratarEspecificacoes(especificacoes)

            const resolucao = projetorEspecificacoes[0]
            const watts = projetorEspecificacoes[1]
            const lumens = projetorEspecificacoes[2]

            const modalResolucao = document.querySelector('[data-projetor-resolucao]')
            modalResolucao.textContent = getValor(resolucao)

            const modalWatts = document.querySelector('[data-projetor-watts]')
            modalWatts.textContent = getValor(watts)

            const modalLumens = document.querySelector('[data-projetor-lumens]')
            modalLumens.textContent = getValor(lumens)

            const id = projetor.getAttribute('data-item-id')
            const tipoItemId = projetor.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-projetor-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const switches = document.querySelectorAll('[data-item-tipo="Switch"]')
    
    switches.forEach((switchItem) => {

        const patrimonio = switchItem.getAttribute('data-item-patrimonio')
        const marca = switchItem.getAttribute('data-item-marca')
        const modelo = switchItem.getAttribute('data-item-modelo')

        const especificacoes = switchItem.textContent

        const pai = switchItem.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-switch-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-switch-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-switch-modelo]')
            modalModelo.textContent = modelo

            const switchEspecificacoes = tratarEspecificacoes(especificacoes)

            const rj = switchEspecificacoes[0]
            const sfp = switchEspecificacoes[1]
            const fonte  = switchEspecificacoes[2]
            const watts  = switchEspecificacoes[3]

            const modalRj = document.querySelector('[data-switch-rj]')
            modalRj.textContent = getValor(rj)
            
            const modalSfp = document.querySelector('[data-switch-sfp]')
            modalSfp.textContent = getValor(sfp)

            const modalFonte = document.querySelector('[data-switch-fonte]')
            modalFonte.textContent = getValor(fonte)

            const modalWatts = document.querySelector('[data-switch-watts]')
            modalWatts.textContent = getValor(watts)

            const id = switchItem.getAttribute('data-item-id')
            const tipoItemId = switchItem.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-switch-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const ares = document.querySelectorAll('[data-item-tipo="Ar Condicionado"]')
    
    ares.forEach((ar) => {

        const patrimonio = ar.getAttribute('data-item-patrimonio')
        const marca = ar.getAttribute('data-item-marca')
        const modelo = ar.getAttribute('data-item-modelo')

        const especificacoes = ar.textContent

        const pai = ar.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-ar-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-ar-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-ar-modelo]')
            modalModelo.textContent = modelo

            const arEspecificacoes = tratarEspecificacoes(especificacoes)

            const capacidade = arEspecificacoes[0]
            const cor = arEspecificacoes[1]

            const modalCapacidade = document.querySelector('[data-ar-capacidade]')
            modalCapacidade.textContent = getValor(capacidade)
            
            const modalCor = document.querySelector('[data-ar-cor]')
            modalCor.textContent = getValor(cor)

            const id = ar.getAttribute('data-item-id')
            const tipoItemId = ar.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-ar-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const fogoes = document.querySelectorAll('[data-item-tipo="Fogão"]')
    
    fogoes.forEach((fogao) => {

        const patrimonio = fogao.getAttribute('data-item-patrimonio')
        const marca = fogao.getAttribute('data-item-marca')
        const modelo = fogao.getAttribute('data-item-modelo')

        const especificacoes = fogao.textContent

        const pai = fogao.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-fogao-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-fogao-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-fogao-modelo]')
            modalModelo.textContent = modelo

            const fogaoEspecificacoes = tratarEspecificacoes(especificacoes)

            const capacidade = fogaoEspecificacoes[0]
            const cor = fogaoEspecificacoes[1]
            const voltagem = fogaoEspecificacoes[2]
            const industrial = fogaoEspecificacoes[3]

            const modalCapacidade = document.querySelector('[data-fogao-capacidade]')
            modalCapacidade.textContent = getValor(capacidade)
            
            const modalCor = document.querySelector('[data-fogao-cor]')
            modalCor.textContent = getValor(cor)
            
            const modalVoltagem = document.querySelector('[data-fogao-voltagem]')
            modalVoltagem.textContent = getValor(voltagem)
            
            const modalIndustrial = document.querySelector('[data-fogao-industrial]')
            modalIndustrial.textContent = getValor(industrial)

            const id = fogao.getAttribute('data-item-id')
            const tipoItemId = fogao.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-fogao-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const freezers = document.querySelectorAll('[data-item-tipo="Freezer"]')
    
    freezers.forEach((freezer) => {

        const patrimonio = freezer.getAttribute('data-item-patrimonio')
        const marca = freezer.getAttribute('data-item-marca')
        const modelo = freezer.getAttribute('data-item-modelo')

        const especificacoes = freezer.textContent

        const pai = freezer.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-freezer-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-freezer-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-freezer-modelo]')
            modalModelo.textContent = modelo

            const freezerEspecificacoes = tratarEspecificacoes(especificacoes)

            const cor = freezerEspecificacoes[0]
            const capacidade = freezerEspecificacoes[1]
            const voltagem = freezerEspecificacoes[2]

            const modalCapacidade = document.querySelector('[data-freezer-capacidade]')
            modalCapacidade.textContent = getValor(capacidade)
            
            const modalCor = document.querySelector('[data-freezer-cor]')
            modalCor.textContent = getValor(cor)
            
            const modalVoltagem = document.querySelector('[data-freezer-voltagem]')
            modalVoltagem.textContent = getValor(voltagem)
    
            const id = freezer.getAttribute('data-item-id')
            const tipoItemId = freezer.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-freezer-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const geladeiras = document.querySelectorAll('[data-item-tipo="Geladeira"]')
    
    geladeiras.forEach((geladeira) => {

        const patrimonio = geladeira.getAttribute('data-item-patrimonio')
        const marca = geladeira.getAttribute('data-item-marca')
        const modelo = geladeira.getAttribute('data-item-modelo')

        const especificacoes = geladeira.textContent

        const pai = geladeira.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-geladeira-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-geladeira-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-geladeira-modelo]')
            modalModelo.textContent = modelo

            const geladeiraEspecificacoes = tratarEspecificacoes(especificacoes)

            const cor = geladeiraEspecificacoes[0]
            const capacidade = geladeiraEspecificacoes[1]
            const voltagem = geladeiraEspecificacoes[2]

            const modalCapacidade = document.querySelector('[data-geladeira-capacidade]')
            modalCapacidade.textContent = getValor(capacidade)
            
            const modalCor = document.querySelector('[data-geladeira-cor]')
            modalCor.textContent = getValor(cor)
            
            const modalVoltagem = document.querySelector('[data-geladeira-voltagem]')
            modalVoltagem.textContent = getValor(voltagem)

            const id = geladeira.getAttribute('data-item-id')
            const tipoItemId = geladeira.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-geladeira-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const liquidificadores = document.querySelectorAll('[data-item-tipo="Liquidificador"]')
    
    liquidificadores.forEach((liquidificador) => {

        const patrimonio = liquidificador.getAttribute('data-item-patrimonio')
        const marca = liquidificador.getAttribute('data-item-marca')
        const modelo = liquidificador.getAttribute('data-item-modelo')

        const especificacoes = liquidificador.textContent

        const pai = liquidificador.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-liquidificador-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const modalMarca = document.querySelector('[data-liquidificador-marca]')
            modalMarca.textContent = marca
            
            const modalModelo = document.querySelector('[data-liquidificador-modelo]')
            modalModelo.textContent = modelo

            const liquidificadorEspecificacoes = tratarEspecificacoes(especificacoes)

            const cor = liquidificadorEspecificacoes[0]
            const capacidade = liquidificadorEspecificacoes[1]
            const watts = liquidificadorEspecificacoes[2]
            const voltagem = liquidificadorEspecificacoes[3]

            const modalCapacidade = document.querySelector('[data-liquidificador-capacidade]')
            modalCapacidade.textContent = getValor(capacidade)
            
            const modalCor = document.querySelector('[data-liquidificador-cor]')
            modalCor.textContent = getValor(cor)
            
            const modalVoltagem = document.querySelector('[data-liquidificador-voltagem]')
            modalVoltagem.textContent = getValor(voltagem)
            
            const modalWatts = document.querySelector('[data-liquidificador-watts]')
            modalWatts.textContent = getValor(watts)

            const id = liquidificador.getAttribute('data-item-id')
            const tipoItemId = liquidificador.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-liquidificador-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const quadros = document.querySelectorAll('[data-item-tipo="Quadro"]')
    
    quadros.forEach((quadro) => {

        const patrimonio = quadro.getAttribute('data-item-patrimonio')
   
        const especificacoes = quadro.textContent

        const pai = quadro.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-quadro-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const quadroEspecificacoes = tratarEspecificacoes(especificacoes)

            const tipo = quadroEspecificacoes[0]
            const tamanho = quadroEspecificacoes[1]

            const modalTipo = document.querySelector('[data-quadro-tipo]')
            modalTipo.textContent = getValor(tipo)

            const modalTamanho = document.querySelector('[data-quadro-tamanho]')
            modalTamanho.textContent = getValor(tamanho)

            const id = quadro.getAttribute('data-item-id')
            const tipoItemId = quadro.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-quadro-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    })

    const armarios = document.querySelectorAll('[data-item-tipo="Armário"]')
    const cadeiras = document.querySelectorAll('[data-item-tipo="Cadeira"]')
    const mesas = document.querySelectorAll('[data-item-tipo="Mesa"]')
    const estantes = document.querySelectorAll('[data-item-tipo="Estante"]')

    const inicializaMobilia = (mobilia) => {

        const patrimonio = mobilia.getAttribute('data-item-patrimonio')

        const tipoMobilia = mobilia.getAttribute('data-item-tipo')

        const especificacoes = mobilia.textContent

        const pai = mobilia.parentElement

        pai.addEventListener('click', () => {
            const modalPatrimonio = document.querySelector('[data-mobilia-patrimonio]')
            modalPatrimonio.textContent = patrimonio

            const mobliaEspecificacoes = tratarEspecificacoes(especificacoes)

            const tipo = mobliaEspecificacoes[0]

            const modalMobilia = document.querySelector('[data-mobilia]')
            modalMobilia.textContent = tipoMobilia

            const modalTipo = document.querySelector('[data-mobilia-tipo]')
            modalTipo.textContent = getValor(tipo)

            const id = mobilia.getAttribute('data-item-id')
            const tipoItemId = mobilia.getAttribute('data-tipo-item-id')

            const linkEdicao = '/administracao/inventario_formulario'
            const modalEditar = document.querySelector('[data-mobilia-link]')

            modalEditar.href = `${linkEdicao}?id_item=${id}&id_tipo=${tipoItemId}`
        })
    }

    armarios.forEach(inicializaMobilia)
    cadeiras.forEach(inicializaMobilia)
    estantes.forEach(inicializaMobilia)
    mesas.forEach(inicializaMobilia)

})

()