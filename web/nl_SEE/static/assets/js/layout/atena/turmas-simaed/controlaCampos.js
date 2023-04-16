function atualizar_simaed(){
    const div1 = document.querySelector('[data-anexar-arquivo]')
    const div2 = document.querySelector('[data-atualizacao-siamed]')
    const botao = document.getElementById("desativar").disabled = true

    div1.classList.add('oculto')
    div2.classList.remove('oculto')
    
    const modais = document.querySelectorAll("[data-modal]")
    
    if(modais != null)
        modais.forEach((modal) => {
        modal.classList.add('oculto')
    })

} 