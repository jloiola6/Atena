// MOSTRANDO TODAS AS ESCOLAS NA TELA DE FORMA ASSÍCRONA

const urlEscolas = `${window.location.origin}/api/escolas/`

const container = document.querySelector('[data-container-escolas]')
const botao = document.querySelector('[data-botao-escolas]')

const getDados = async () => {
    try{
        const response = await fetch(urlEscolas)
        const json = await response.json()

        return json
    }catch(erro){
        console.log('Erro na requisição')
    }
}

const constroiLista = async () => {
    const dados = await getDados()
    
    const lista = dados.map(dado => dado.nome_escola)
    
    return lista
}

const carregaEscolas = async (evento) => {
    const ulEscolas = document.createElement('ul')
    ulEscolas.classList.add('container-detalhes')

    const escolas = await constroiLista()

    escolas.forEach(escola => {
        const liEscola = document.createElement('li')
        liEscola.textContent = escola
        
        ulEscolas.appendChild(liEscola)
    })

    container.appendChild(ulEscolas)

    evento.target.parentElement.remove()
}

botao.addEventListener('click', carregaEscolas)


// MOSTRANDO TURMAS DE UMA ESCOLA DE ACORDO COM O ID DIGITADO
const containerTurmas = document.querySelector('[data-container-escola-turmas]')

const constroiUl = (lista) => {
    const ulTurmas = document.createElement('ul')
    ulTurmas.classList.add('container-detalhes')

    if(lista.length){
        lista.forEach(turma => {
            const liTurma = document.createElement('li')
            liTurma.textContent = turma
            ulTurmas.appendChild(liTurma)
        })
    }else{
        const mensagem = document.createElement('span')
        mensagem.textContent = 'ID não encontrado'
        ulTurmas.appendChild(mensagem)
    }
    
    return ulTurmas
}


const getTurmas = async (id) => {
    const url = `${window.location.origin}/api/escola/turma`
    try{
        const response = await fetch(`${url}/?id=${id}`)
        const json = await response.json()
        console.log(response)
        return json
    }catch(erro){
        console.log('Erro na requisição')
        console.log(`Detalhes: ${erro}`)
    }
}

const constroiListaTurmas = async (id) => {
    const dados = await getTurmas(id)

    const lista = dados.map(dado => dado.nome)

    return lista
}

const atualizaContainer = async (evento) => {
    const valor = evento.target.value

    if(valor !== ''){
        const valorAtual = containerTurmas.dataset.containerEscolaTurmas

        if(valor != valorAtual){
            containerTurmas.dataset.containerEscolaTurmas = valor
            
            const turmas = await constroiListaTurmas(valor)
            
            const ul = containerTurmas.querySelector('ul')

            if(ul)
                ul.remove()
            
            containerTurmas.appendChild(constroiUl(turmas))
        }
    }
}

const inputID = document.querySelector('[data-busca-id]')
inputID.addEventListener('keyup', atualizaContainer)