// Script para controlar a submissão de formulários impedindo que o usuário aperte várias vezes o botão de submissão

(() => {
    const formularios = document.querySelectorAll('form')
    
    if(formularios.length > 0)
        // PERCORRENDO OS FORMULÁRIOS DA PÁGINA
        formularios.forEach((formulario) => {
            // LISTANDO TODOS OS BOTOÕES DE SUBMISSÃO
            const botoesSubmissao = formulario.querySelectorAll('[type="submit"]')

            if(botoesSubmissao.length > 0){
                formulario.addEventListener('submit', () => {
                    botoesSubmissao.forEach((botao) => {
                        // VERIFICANDO SE O BOTÃO NÃO É PARA EXPORTAÇÃO DE ARQUIVOS
                        if(!botao.name.includes('exportar')){
                            botao.classList.add('oculto')
                            
                            const spinner = document.createElement('div')
                            spinner.classList.add('spinner-submissao')
                            
                            botao.parentElement.insertBefore(spinner, botao)
                        }
                    })
                })
            }
        })
})

()