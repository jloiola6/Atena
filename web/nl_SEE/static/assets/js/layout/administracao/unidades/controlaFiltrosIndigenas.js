// Script para controlar a exibição de filtros relativos aos filtros para unidades de localização indígenas

(() => {
    const controlaContainers = (exibicao) => {

        const containersFiltros = document.querySelectorAll('[data-filtro-indigena]')
        
        containersFiltros.forEach((container) => {

            if(exibicao)
                container.style.display = 'flex'
            else
                container.style.display = 'none'
        })
    
    }

    const inicializaCampo = () => {
        const campo = document.getElementById('id-indigena')

        if(campo.checked)
            controlaContainers(true)

        campo.addEventListener('click', () => {controlaContainers(campo.checked)})
    }

    inicializaCampo()
})

()