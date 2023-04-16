// Script para controlar o comportamento dos filtros no modal em Unades Educacionais

(() => {
    // Controle da ativação dos chekboxes de municípios de acordo com a regional selecionada

    // Lista com as regionais e seus respectivos municípios
    const regionais = [
        {'nome': 'Alto Acre', 'municipios': ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri']},
        {'nome': 'Baixo Acre', 'municipios': ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard']},
        {'nome': 'Juruá', 'municipios': ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves']},
        {'nome': 'Purus', 'municipios': ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira']},
        {'nome': 'Tarauacá / Envira', 'municipios': ['Feijó', 'Jordão', 'Tarauacá']},
    ]

    // Inicializando os checkboxes
    const checkboxMunicipios = document.querySelectorAll('[data-municipio]')
    const checkboxRegionais = document.querySelectorAll('[data-regional]')

    // Função de controle dos checkboxes de municípios
    const controlaMunicipios = (evento) => {
        const regionalSelecionada = evento.target.dataset.regional
        const ativo = evento.target.checked

        // Utilizando o filter para buscar a lista de municípios de acordo com a regional selecionada
        const municipios = regionais.filter((regional) => regional['nome'] == regionalSelecionada)[0]['municipios']

        checkboxMunicipios.forEach((check) => {
            const valor = check.dataset.municipio

            if(municipios.includes(valor)){
                check.checked = ativo
                check.disabled = ativo
            }
        })
    }

    // Adicionando os escutadores aos checkboxes de regionais com a função de controle
    checkboxRegionais.forEach((check) => {
        check.addEventListener('click', controlaMunicipios)
    })

    // Verificação das regionais já selecionadas ao carregamento da página
    checkboxRegionais.forEach((check) => {
        console.log
        check.dispatchEvent(new Event('click'))
    })
})

()