(() => {
    const controlaExibicaoo = (menu, operador) => {
        // Maximiza ou minimiza menu de acordo com o operador

        const filho = [...menu.children][0]
        const possuiCards = filho.classList.contains('container-cards-simples')
        const possuiLinks = filho.classList.contains('container-detalhes')
        const possuiprofessores = filho.classList.contains('tabela-servidores')

        // console.log(menu)
        if(operador){
            menu.style.maxHeight = null
        }else{
            const larguraJanela = window.innerWidth

            if(larguraJanela <= 425)
                menu.style.maxHeight = "128px"
            else if(larguraJanela <= 768)
                menu.style.maxHeight = "88px"
            else
                menu.style.maxHeight = "64px"

            if(possuiCards){
                const altura = `${filho.offsetHeight+32}px`
                menu.style.height = altura
                menu.style.maxHeight = altura
            } else if (possuiLinks) {
                const altura = `${filho.offsetHeight+30}px`
                menu.style.height = altura
                menu.style.maxHeight = altura
            } else if (possuiprofessores) {
                const altura = `${filho.offsetHeight+50}px`
                menu.style.height = altura
                menu.style.maxHeight = altura
            }
        }


    }

    const getMenusFilhoss = (identificador) => {
        // Retorna uma lista de menus HTML que com os menus filhos de um menu pai
        const menusFilhos = document.querySelectorAll(`[data-accordeon-filho="${identificador}"]`)

        return menusFilhos
    }

    const controlaMenusFilhoss = (menus, operador) => {
        // Atualiza a exibição dos menus filhos com base nos parâmetros
        menus.forEach((menu) => {
            const identificador = menu.getAttribute("data-accordeon-pai")
            const ativo = menu.getAttribute("data-accordeon-ativo") == "true"

            if(ativo){
                const menusFilhos = getMenusFilhoss(identificador)
                controlaMenusFilhoss(menusFilhos, operador)
            }

            controlaExibicaoo(menu, operador)
        })
    }

    const controlaMenuPaii = (menu) => {
        // Controla o container de um menu accordeon qualquer
        const identificador = menu.getAttribute("data-accordeon-pai")
        const ativo = menu.getAttribute("data-accordeon-ativo") == "true"
        const botaoExpandir = menu.lastElementChild

        // Modifica o estado do menu pai
        if(ativo){
            menu.setAttribute("data-accordeon-ativo", "false")
            menu.classList.remove("menu-pai-ativo")
            botaoExpandir.classList.remove("accordeon-expandir-ativo")
        }else{
            menu.setAttribute("data-accordeon-ativo", "true")
            menu.classList.add("menu-pai-ativo")
            botaoExpandir.classList.add("accordeon-expandir-ativo")
        }

        // Muda a exibição dos menus filhos
        const menusFilhos = getMenusFilhoss(identificador);
        controlaMenusFilhoss(menusFilhos, ativo);
    }

    const menus = document.querySelectorAll("[data-accordeon-pai]")

    menus.forEach((menu) => {
        const identificador = menu.getAttribute("data-accordeon-pai")
        const possuiFilho = getMenusFilhoss(identificador).length > 0
        const botaoExpandir = menu.lastElementChild

        if(possuiFilho){
            botaoExpandir.addEventListener("click", () => {controlaMenuPaii(menu)})
        }else{
            botaoExpandir.remove()
        }
    })
})

()