// Script para controlar qualquer peculiaridade nos cards de menus

(() => {

    // Esta função controla a animcação do menu Atena
    const menuAtena = () => {
        const menu = document.querySelector('[data-menu-atena]')

        const hoverMenu = (mouseOn) => {
            const logoFechado = document.querySelector('[data-icone-fechado]')
            const logoAberto = document.querySelector('[data-icone-aberto]')

            if(mouseOn){
                logoFechado.classList.add('oculto')
                logoAberto.classList.remove('oculto')
            }else{
                logoFechado.classList.remove('oculto')
                logoAberto.classList.add('oculto')
            }

            
        }

        if(menu != null){
            menu.addEventListener('mouseover', () => {
                hoverMenu(true)
            })

            menu.addEventListener('mouseout', () => {
                hoverMenu(false)
            })  
        }
        
    }

    menuAtena()
})

()