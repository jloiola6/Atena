(() => {
    const checkNotebooks = document.querySelectorAll('input[name="notebook"]')
    const checkCarregador = document.querySelectorAll('input[name="carregador"]')
    const buttonExportar = document.getElementById('btn-exportar')
    const mensagem = document.getElementById('msg')


    const vereficarBtn = () => {
        let carregador = document.querySelector('input[name="carregador"]:checked')
        let notebook = document.querySelector('input[name="notebook"]:checked')

        if(notebook.value == 1 && carregador.value == 1){
            buttonExportar.disabled = false
            mensagem.classList.add('oculto')
        }else{
            buttonExportar.disabled = true
            mensagem.classList.remove('oculto')
        }
    }


    checkNotebooks.forEach( elementos => elementos.addEventListener('change',vereficarBtn))
    checkCarregador.forEach( elementos => elementos.addEventListener('input',vereficarBtn))

})()