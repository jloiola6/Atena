// Script para controlar a exibição dos campos de endereço nos formulários de unidades administrativas

(() => {
    const radiosSede = document.querySelectorAll('[data-unidade-sede]')
    const radioSim = radiosSede[0]
    const radioNao = radiosSede[1]

    const controlaCamposEndereco = (operador) => {
        const camposEndereco = document.querySelectorAll('[data-formulario-endereco]')

        camposEndereco.forEach((campo) => {
            campo.lastElementChild.required = operador

            if(campo.lastElementChild.name == 'complemento')
                campo.lastElementChild.required = false

            if(operador)
                campo.classList.remove('oculto')
            else
                campo.classList.add('oculto')
        })
    }

    const inicializaCamposEndereco = () => {
        const operador = radioNao.checked
        controlaCamposEndereco(operador)
    }

    inicializaCamposEndereco()

    radioSim.addEventListener('click', inicializaCamposEndereco)
    radioNao.addEventListener('click', inicializaCamposEndereco)

    const selecaoMunicipios = document.querySelector('[data-selecao-municipio]')
    const campoRegional = document.querySelector('[data-campo-regional]')

    const altoAcre = ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri']
    const baixoAcre = ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard']
    const tarauaca = ['Feijó', 'Jordão', 'Tarauacá']
    const jurua = ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves']
    const purus = ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira']

    const controlaRegional = () => {
        const municipioSelecionado = selecaoMunicipios.value
        let regional

        if(baixoAcre.includes(municipioSelecionado))
            regional = 'Baixo Acre'

        if(altoAcre.includes(municipioSelecionado))
            regional = 'Alto Acre'

        if(tarauaca.includes(municipioSelecionado))
            regional = 'Tarauacá/Envira'

        if(jurua.includes(municipioSelecionado))
            regional = 'Juruá'

        if(purus.includes(municipioSelecionado))
            regional = 'Purus'

        campoRegional.value = regional
    }

    controlaRegional()
    selecaoMunicipios.addEventListener('change', controlaRegional)
})

()