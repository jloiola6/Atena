(() => {
    // Função para controlar o campo de regional de acordo com o município selecionado
    const selecaoMunicipio = document.querySelector('[data-selecao-municipio]')
    const campoRegional = document.querySelector('[data-campo-regional]')

    // Lista com as regionais e seus respectivos municípios
    const regionais = [
        {'nome': 'Alto Acre', 'municipios': ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri']},
        {'nome': 'Baixo Acre', 'municipios': ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard']},
        {'nome': 'Juruá', 'municipios': ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves']},
        {'nome': 'Purus', 'municipios': ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira']},
        {'nome': 'Tarauacá / Envira', 'municipios': ['Feijó', 'Jordão', 'Tarauacá']},
    ]

    const inicializaRegional = () => {
        const municipio = selecaoMunicipio.value

        const itemRegional = regionais.filter(regional => regional['municipios'].includes(municipio))[0]
        campoRegional.value = itemRegional['nome']
    }

    inicializaRegional()

    selecaoMunicipio.addEventListener('input', inicializaRegional)
})

()