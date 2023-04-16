// Script para controlar o comportamento do formulário de servidor terceirizado

(() => {
    // CONTROLE DE REGIONAL POR MUNICÍPIO SELECIONADO

    const selecaoMunicipio = document.querySelector('[data-selecao-municipio]')

    const getRegional = (municipio) => {
        const altoAcre = ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri']
        const baixoAcre = ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard']
        const tarauaca = ['Feijó', 'Jordão', 'Tarauacá']
        const jurua = ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves']
        const purus = ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira']

        if(altoAcre.includes(municipio))
            return "Alto Acre"

        if(baixoAcre.includes(municipio))
            return "Baixo Acre"

        if(jurua.includes(municipio))
            return "Juruá"

        if(purus.includes(municipio))
            return "Purus"

        if(tarauaca.includes(municipio))
            return "Tarauacá / Envira"
    }

    const exibeRegional = () => {
        const municipio = selecaoMunicipio.value
        const regional = getRegional(municipio)

        const campoRegional = document.querySelector('[data-campo-regional]')
        campoRegional.value = regional
    }

    exibeRegional()
    selecaoMunicipio.addEventListener('change', exibeRegional)
})

()