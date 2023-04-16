// Script para controlar o componente de campo de CEP

(() => {
    const campoCep = document.querySelector('[data-campo-cep]')
    const campoRua = document.querySelector('[data-campo-rua]')
    const campoBairro = document.querySelector('[data-campo-bairro]')
    const campoMunicipio = document.querySelector('[data-selecao-municipio]')
    const campoRegional = document.querySelector('[data-campo-regional]')

    if (campoBairro)
        campoBairro.readOnly = true

    if (campoRua)
        campoRua.readOnly = true

    if (campoCep){
        const spanErro = document.createElement('span')
        spanErro.classList.add('texto-vermelho')
        spanErro.classList.add('oculto')
        spanErro.textContent = 'Cep inválido, tente novamente'

        const containerPai = campoCep.parentElement
        containerPai.appendChild(spanErro)

        const buscarEndereco = async (cep) => {
            const url = `https://viacep.com.br/ws/${cep}/json/`
            try{
                const response = await fetch(url)
                const data = await response.json()

                if(data.erro)
                    throw new Error


                return data
            }catch{
                console.log('CEP inválido')
                return null
            }


        }

        const constroiEndereco = async (cep) => {
            const dados = await buscarEndereco(cep)

            if(dados){
                const endereco = {
                    rua: dados.logradouro,
                    bairro: dados.bairro,
                    municipio: dados.localidade
                }

                console.log(endereco)

                return endereco
            }

            return null
        }

        const atualizaCampos = async () => {
            const valor = campoCep.value

            if(valor.length == 9){
                const endereco = await constroiEndereco(valor)

                if(campoBairro && campoRua ){
                    if(endereco){
                        spanErro.classList.add('oculto')

                        if(endereco.rua){
                            campoRua.value = endereco.rua
                            campoRua.readOnly = true
                        }else{

                            campoRua.readOnly = false
                            campoRua.value = ''
                        }

                        if(endereco.bairro){

                            campoBairro.value = endereco.bairro
                            campoBairro.readOnly = true
                        }else{
                            campoBairro.readOnly = false
                            campoBairro.value = ''
                        }


                        if (endereco.municipio) {

                            campoMunicipio.value = endereco.municipio

                            const regionais = [
                                {'nome': 'Alto Acre', 'municipios': ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri']},
                                {'nome': 'Baixo Acre', 'municipios': ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard']},
                                {'nome': 'Juruá', 'municipios': ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves']},
                                {'nome': 'Purus', 'municipios': ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira']},
                                {'nome': 'Tarauacá / Envira', 'municipios': ['Feijó', 'Jordão', 'Tarauacá']},
                            ]


                            // if (campoMunicipio.value.replace(' ','').toLowerCase() == )
                            const itemRegional = regionais.filter(regional => regional['municipios'].includes(campoMunicipio.value))[0]

                            campoRegional.value = itemRegional['nome']

                            // // caso seja municipio seja nulo
                            // campoMunicipio.classList.add('oculto')

                            // // criando input
                            // const inputMunicipio = document.createElement('input')
                            // inputMunicipio.setAttribute('id','campo-municipio')
                            // inputMunicipio.setAttribute('name','municipio')
                            // inputMunicipio.setAttribute('data-selecao-municipio','')
                            // inputMunicipio.classList.add('campo-texto')
                            // inputMunicipio.classList.add('campo-grande')
                            // campoMunicipio.parentElement.append(inputMunicipio)

                            // inputMunicipio.value = endereco.municipio
                        }


                    }else{
                        spanErro.classList.remove('oculto')

                        campoRua.value = ''
                        campoBairro.value = ''
                    }
                }
            }
        }

        campoCep.addEventListener('input', atualizaCampos)
    }

})

()