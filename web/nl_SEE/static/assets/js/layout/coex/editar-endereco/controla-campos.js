// Script para controlar a exibição de campos no formulário de editar endereço da unidade

function getMunicipio(){
    const elemento = document.getElementById("campo-municipio");
    const municipio = elemento.options[elemento.selectedIndex].text;

    return municipio;
}

function getRegional(municipio){
    const altoAcre = ['Assis Brasil', 'Brasiléia', 'Epitaciolândia', 'Xapuri'];
    const baixoAcre = ['Acrelândia', 'Bujari', 'Capixaba', 'Plácido de Castro', 'Porto Acre', 'Rio Branco', 'Senador Guiomard'];
    const tarauaca = ['Feijó', 'Jordão', 'Tarauacá'];
    const jurua = ['Cruzeiro do Sul', 'Marechal Thaumaturgo', 'Mâncio Lima', 'Porto Walter', 'Rodrigues Alves'];
    const purus = ['Manoel Urbano', 'Santa Rosa do Purus', 'Sena Madureira'];

    if(baixoAcre.indexOf(municipio) >= 0)
		return "Baixo Acre";

    if(altoAcre.indexOf(municipio) >= 0)
        return "Alto Acre";
    
    if(jurua.indexOf(municipio) >= 0)
        return "Juruá";

    if(purus.indexOf(municipio) >= 0)
        return "Purus";

    if(tarauaca.indexOf(municipio) >= 0)
        return "Tarauacá / Envira";
}

function exibeRegional(){
    const municipio = getMunicipio();
    const regional = getRegional(municipio);

    const elemento = document.getElementById("campo-regional");
    elemento.value = regional;
}

exibeRegional();