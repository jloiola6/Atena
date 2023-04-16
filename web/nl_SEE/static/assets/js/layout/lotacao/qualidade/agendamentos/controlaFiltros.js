// Script para controlar o comportamento dos filtros na página de agendamentos

(() =>{
    const fieldset = document.querySelector('[data-fieldset-status]')
    const checkTodos = document.querySelector('[data-check-todos]')

    const checksStatus = fieldset.querySelectorAll('input[type="checkbox"]')

    const marcarTodos = () => {
        const validaTodos = checkTodos.checked

        checksStatus.forEach((check) => {
            if(check != checkTodos){
                check.checked = validaTodos
                check.disabled = validaTodos
            }
        })
    }

    checkTodos.addEventListener('click', marcarTodos)
})

()