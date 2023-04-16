// Script utilziado para controlar a navagacao em abas e containers em formularios

(() => {
    const abas = document.querySelectorAll('[data-form-aba]')
    const containers = document.querySelectorAll('[data-form-container]')
    const botoes = document.querySelectorAll('[data-form-botao]')
   

    const dados = document.querySelector('[data-form-container="dados"]')
    const endereco = document.querySelector('[data-form-container="endereco"]')
    const contato = document.querySelector('[data-form-container="contato"]')
    const banco = document.querySelector('[data-form-container="dados-bancarios"]')
    

    const msg = () => { 
        const mensage = document.createElement('p')
        mensage.textContent = 'Preencha o campo'
        mensage.classList.add('texto-vermelho')
        mensage.classList.add('texto-pequeno')
        mensage.classList.add('consulta-mensagem-erro')

        return mensage

    }
   
    const ativaAba = (aba, ativacao) => {
        if(ativacao)
            aba.classList.add("navegacao-surface-item-ativo");
        else
            aba.classList.remove("navegacao-surface-item-ativo");
    }

    const renicia = () => {
        abas.forEach((aba) => {
            ativaAba(aba, false)
        })

        containers.forEach((container) => {
            container.classList.add('oculto')
        })
    }

    const exibeContainer = (container) => {
        container.classList.remove('oculto')
    }
    // Verificar inputs de referentes a Dados no template
    const formDado = (dados) => {
        
        const inputsDados = dados.querySelectorAll('input')
        let verifynome = false
        let verifydata = false
        
        inputsDados.forEach((elementos) => {
            const mensage = msg()

            if (elementos.name === 'nome'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifynome = true
                }else{
                    verifynome = false
                    elementos.style.borderColor = 'red'

                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            
            } else if (elementos.name === 'data_nascimento'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifydata = true
                }else{
                    verifydata = false
                    elementos.style.borderColor = 'red'
                    
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            }
        })


        if (verifydata && verifynome){
            return true
        }
        else{
            return false
        }
    }

    // Verificar inputs de referentes a Endereço no template
    const formEndereco = (dados) =>{
        const inputsDados = dados.querySelectorAll('input')

        let verifynumero = false 
        let verifycep = false 

        inputsDados.forEach((elementos) => {
            const mensage = msg()

            if (elementos.name === 'numero'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifynumero = true
                }else{
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                    elementos.style.borderColor = 'red'
                    verifynumero = false
                }
            
            }
            if (elementos.name === 'cep'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifycep = true
                }else{
                    elementos.style.borderColor = 'red'
                    verifycep = false
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            }
        })

        if (verifynumero && verifycep){
            return true
        }
        else{
            return false
        }
    }

    // Verificar inputs de referentes a Contato no template
    const formContato = (dados) =>{
        const inputsDados = dados.querySelectorAll('input')
        let verify = false 

        inputsDados.forEach((elementos) => {
            const mensage = msg()
            if (elementos.name === 'celular'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verify = true
                }else{
                    verify = false
                    elementos.style.borderColor = 'red'
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            }
        })
        return verify
        
    }

    // Verificar inputs de referentes a Bancarios no template
    const formBanco = (dados) =>{
        const inputsDados = dados.querySelectorAll('input')
        let verifyconta = false 
        let verifyagencia = false

        inputsDados.forEach((elementos) => {
            const mensage = msg()

            if (elementos.name === 'agencia'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifyagencia = true
                }else{
                    elementos.style.borderColor = 'red'
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            }

            if (elementos.name === 'conta'){
                if(elementos.value != ''){
                    elementos.style.borderColor =  '#C1C1c1'
                    if (elementos.nextSibling){
                        elementos.nextSibling.remove()
                    }
                    verifyconta = true
                }else{
                    elementos.style.borderColor = 'red'
                    if (elementos.nextSibling.nodeName == '#text'){
                        elementos.insertAdjacentElement('afterend', mensage)
                    }
                }
            }
        })
        

        if (verifyagencia && verifyconta){
            return true
        }
        else{
            return false
        }
        
    }

    const inicializaBotoes = () => {
        botoes.forEach((botao) => {
            botao.addEventListener('click', (evento) => {
                evento.preventDefault()

                const atributo = botao.getAttribute('data-form-botao')
                const container = document.querySelector(`[data-form-container="${atributo}"]`)
                const aba = document.querySelector(`[data-form-aba="${atributo}"]`)

                // Verificar o form atual está preenchido, para a próxima aba
                console.log(atributo)
                if(atributo == 'dados'){
                    renicia()
                    exibeContainer(container)
                    ativaAba(aba, true)

                }else if (atributo == 'endereco'){
                    if (formDado(dados)) {
                        renicia()
                        exibeContainer(container)
                        ativaAba(aba, true)
                    }
                }
                else if(atributo == 'contato'){
                    if(formEndereco(endereco)){
                        renicia()
                        exibeContainer(container)
                        ativaAba(aba, true)
                    }
                }else if(atributo == 'dados-bancarios'){
                    if(formContato(contato)){
                        renicia()
                        exibeContainer(container)
                        ativaAba(aba, true)
                    }
                }else if (atributo == 'cadastro'){
                    if(formBanco(banco)){
                        const modal = document.querySelector('[data-modal="confirmar"]')
                        modal.classList.remove('oculto')
                    }
                }
  
            })
        })  
    }
    
  

    inicializaBotoes()
})

()