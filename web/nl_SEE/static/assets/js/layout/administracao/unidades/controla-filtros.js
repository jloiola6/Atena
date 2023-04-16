// Desabilitar checkbox de municípios de acordo com a regional selecionada

const idsAltoAcre = ['id-Assis-Brasil', 'id-Brasileia', 'id-Epitaciolandia', 'id-Xapuri'];
const idsBaixoAcre = ['id-Acrelandia', 'id-Bujari', 'id-Capixaba', 'id-Placido-de-Castro', 'id-Porto-Acre', 'id-Rio-Branco', 'id-Senador-Guiomard'];
const idsTarauaca = ['id-Feijo', 'id-Jordao', 'id-Tarauaca'];
const idsJurua = ['id-Cruzeiro-do-Sul', 'id-Marechal-Thaumaturgo', 'id-Mancio-Lima', 'id-Porto-Walter', 'id-Rodrigues-Alves'];
const idsPurus = ['id-Manoel-Urbano', 'id-Santa-Rosa-do-Purus', 'id-Sena-Madureira'];

function controlaCheckboxMunicipio(elemento, ativo){
    elemento.checked = ativo;
    elemento.disabled = ativo;
}

function controlaMunicipioPorRegional(lista, ativo){
    let elemento;

    for(let i=0; i<lista.length; i++){
        elemento = document.getElementById(lista[i]);
        // console.log(elemento, elemento.id);
        controlaCheckboxMunicipio(elemento, ativo);
    }
}

function controlaCheckboxRegional(elemento){
    const id = elemento.id;
    const ativo = elemento.checked;

    if(id == "id-alto-acre")
        controlaMunicipioPorRegional(idsAltoAcre, ativo)

    if(id == "id-baixo-acre")
        controlaMunicipioPorRegional(idsBaixoAcre, ativo)

    if(id == "id-jurua")
        controlaMunicipioPorRegional(idsJurua, ativo)

    if(id == "id-purus")
        controlaMunicipioPorRegional(idsPurus, ativo)

    if(id == "id-tarauaca-envira")
        controlaMunicipioPorRegional(idsTarauaca, ativo)
}

function verificaRegionaisSelecionadas() {
    const inputsRegional = document.querySelectorAll(".filtro-regional");
    let elemento, ativo;

    for(let i=0; i<inputsRegional.length; i++){
        elemento = inputsRegional[i];
        ativo = elemento.checked;

        if(ativo)
            controlaCheckboxRegional(elemento);
    }
}