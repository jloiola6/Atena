(() => {

    const getServidores = async (id) => {
        const url = `${window.location.origin}/api/servidor`
        try{
            const response = await fetch(`${url}/?valor=${id}`)
            const json = await response.json()
    
            console.log(response)
    
            return json
        }catch(erro){
            console.log('Erro na requisição')
            console.log(`Detalhes: ${erro}`)
        }
    }
    
    const constroiListaServidores = async (id) => {
        const dados = await getServidores(id)
    
        const lista = dados.map(dado => [dado.id, dado.nome])
        return lista
    }
    
    const atualizaContainerServidor = async (evento) => {
        const input = evento.target
        const atributo = input.getAttribute('aria-controls')
    
        const id = atributo.replace('select2-', '').replace('-results', '')
    
        if(id.includes('equipe')){
            const selecaoServidor = document.getElementById(id)
            const valor = evento.target.value
        
            if(valor !== ''){
                const servidores = await constroiListaServidores(valor)
        
                selecaoServidor.innerHTML = ''
        
                servidores.forEach((servidor) => {
                    const opcao = document.createElement('option')
                    opcao.value = servidor[0]
                    opcao.textContent = servidor[1]
        
                    selecaoServidor.appendChild(opcao)
                })   
            }
        }
    }
    
    const selects = document.querySelectorAll('.selection')
    
    selects.forEach((select) => {
        if(select) 
            select.addEventListener('click', () => {
                const inputServidor = document.querySelector('.select2-search__field')
                inputServidor.addEventListener('keyup', atualizaContainerServidor)
            })
    })
})

()