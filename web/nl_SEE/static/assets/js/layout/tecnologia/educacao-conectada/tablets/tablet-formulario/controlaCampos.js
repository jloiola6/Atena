// Script para controlar o comportamento do formulário de tablets de uma turma
(() => {
    const camposEquipamento = document.querySelectorAll('[data-campo-equipamento]')

    const avancaCampo = (evento) => {
        if(evento.key == 'Enter'){
            evento.preventDefault()

            const campo = evento.target
            const valor = campo.value

            const tamanhoLista = camposEquipamento.length

            if(valor.length > 0)
                camposEquipamento.forEach((input, indice) => {
                    if(campo == input)
                        if(indice != tamanhoLista-1)
                            camposEquipamento[indice+1].focus()
                })
        }
    }

    if(camposEquipamento)
        camposEquipamento.forEach((campo) => {
            campo.addEventListener('keydown', avancaCampo)
        })

})

()