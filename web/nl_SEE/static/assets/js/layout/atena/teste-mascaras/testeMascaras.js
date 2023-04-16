// Script para definir e testar máscaras no sistema

const mascaraNumero = (evento) => {
    const valor = evento.target.value
    
    const novoValor = valor
    .replace(/\D/g, '')
    
    evento.target.value = novoValor
}

const mascaraCPF = (evento) => {
    evento.target.maxLength = '14'

    const valor = evento.target.value
    
    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1-$2')


    evento.target.value = novoValor
}

const mascaraCNPJ= (evento) => {
    evento.target.maxLength = '18'

    const valor = evento.target.value
    
    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1.$2')
    .replace(/(\d{3})(\d)/, '$1/$2')
    .replace(/(\d{4})(\d)/, '$1-$2')


    evento.target.value = novoValor
}

const mascaraTelefone= (evento) => {
    evento.target.maxLength = '15'

    const valor = evento.target.value
    
    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{4})(\d)/, '$1-$2')
    .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
    
    evento.target.value = novoValor
}

const mascaraCEP = (evento) => {
    evento.target.maxLength = '9'

    const valor = evento.target.value

    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d{5})(\d)/, '$1-$2')
    
    evento.target.value = novoValor
}

const mascaraMoeda = (evento) => {
    evento.target.maxLength = '23'

    const valor = evento.target.value

    const options = {style: 'currency', currency: "BRL"}

    const novoValor = valor
    .replace(/\D/g, '')

    const valorFormatado = new Intl.NumberFormat('pt-br', options).format(novoValor / 100)

    evento.target.value = valorFormatado
}

const mascaraCC = (evento) => {
    evento.target.maxLength = '40'

    const valor = evento.target.value

    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d+)(\d)/, '$1-$2')

    evento.target.value = novoValor
}

const mascaraSEI = (evento) => {
    evento.target.maxLength = '25'

    const valor = evento.target.value

    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d{4})(\d{1})/, '$1.$2')
    .replace(/(\d{6})(\d{1})/, '$1.$2')
    .replace(/(\d{6})\.(\d{5})(\d{1})/, '$1.$2/$3')
    .replace(/\/(\d{4})(\d{1})/, '/$1-$2')

    evento.target.value = novoValor
}

const mascaraContrato = (evento) => {
    evento.target.maxLength = '9'

    const valor = evento.target.value

    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d+)(\d{4})/, '$1/$2')

    evento.target.value = novoValor
}

const mascaraEmpenho = (evento) => {
    evento.target.maxLength = '14'

    const valor = evento.target.value

    const novoValor = valor
    .replace(/\D/g, '')
    .replace(/(\d+)(\d{4})/, '$1/$2')

    evento.target.value = novoValor
}

const campoNumero = document.querySelector('[data-mascara-numero]')
const campoCPF = document.querySelector('[data-mascara-cpf]')
const campoCNPJ = document.querySelector('[data-mascara-cnpj]')
const campoTelefone = document.querySelector('[data-mascara-telefone]')
const campoCEP = document.querySelector('[data-mascara-cep]')
const campoMoeda = document.querySelector('[data-mascara-moeda]')
const campoCC = document.querySelector('[data-mascara-cc]')
const campoSEI = document.querySelector('[data-mascara-sei]')
const campoContrato = document.querySelector('[data-mascara-contrato]')
const campoEmepenho = document.querySelector('[data-mascara-empenho]')

campoNumero.addEventListener('input', mascaraNumero)
campoCPF.addEventListener('input', mascaraCPF)
campoCNPJ.addEventListener('input', mascaraCNPJ)
campoTelefone.addEventListener('input', mascaraTelefone)
campoCEP.addEventListener('input', mascaraCEP)
campoMoeda.addEventListener('input', mascaraMoeda)
campoCC.addEventListener('input', mascaraCC)
campoSEI.addEventListener('input', mascaraSEI)
campoContrato.addEventListener('input', mascaraContrato)
campoEmepenho.addEventListener('input', mascaraEmpenho)