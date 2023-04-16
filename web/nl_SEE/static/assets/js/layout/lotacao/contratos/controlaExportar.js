// Script para controlar as exportações de lotações
(() => {
   const formularioExportar = document.querySelector('[data-form-exportar]')

   if(formularioExportar){
        const botaoExportar = formularioExportar.querySelector('[name="btn-exportar"]')
        console.log(botaoExportar)

        const desabilitaBotao = () => {
            botaoExportar.disabled = true
        }

        formularioExportar.addEventListener('submit', desabilitaBotao)
   }
})
()