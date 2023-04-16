// Script para adicionar máscaras a campos de formulários

const mascara = {
    numero (evento){
        const campo = evento.target
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')

        campo.value = novoValor
    },

    cnpj (evento){
        const campo = evento.target
        campo.maxLength = '18'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1/$2')
        .replace(/(\d{4})(\d)/, '$1-$2')

        campo.value = novoValor
    },

    cpf (evento){
        const campo = evento.target
        campo.maxLength = '14'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1-$2')

        campo.value = novoValor
    },

    moeda (evento){
        const campo = evento.target
        campo.maxLength = '23'
        const valor = campo.value

        const options = {style: 'currency', currency: 'BRL'}

        const novoValor = valor
        .replace(/\D/g, '')

        const valorFormatado = new Intl.NumberFormat('pt-br', options).format(novoValor / 100)

        campo.value = valorFormatado
    },

    cep (evento){
        const campo = evento.target
        campo.maxLength = '9'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{5})(\d)/, '$1-$2')

        campo.value = novoValor
    },

    telefone (evento){
        const campo = evento.target
        campo.maxLength = '15'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')

        campo.value = novoValor
    },

    cc (evento){
        const campo = evento.target
        campo.maxLength = '40'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d+)(\d)/g, '$1-$2')

        campo.value = novoValor
    },

    sei (evento){
        const campo = evento.target
        campo.maxLength = '25'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{4})(\d{1})/, '$1.$2')
        .replace(/(\d{6})(\d{1})/, '$1.$2')
        .replace(/(\d{6})\.(\d{5})(\d{1})/, '$1.$2/$3')
        .replace(/\/(\d{4})(\d{1})/, '/$1-$2')

        campo.value = novoValor
    },

    contrato (evento){
        const campo = evento.target
        campo.maxLength = '9'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d+)(\d{4})/, '$1/$2')

        campo.value = novoValor
    },

    empenho (evento){
        const campo = evento.target
        campo.maxLength = '15'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d+)(\d{4})/, '$1/$2')

        campo.value = novoValor
    },

    parecer (evento){
        const campo = evento.target
        campo.maxLength = '14'
        const valor = campo.value

        const novoValor = valor
        .replace(/\D/g, '')
        .replace(/(\d{4})(\d)/, '$1.$2')
        .replace(/(\d{4}\.\d{2})(\d)/, '$1.$2')

        campo.value = novoValor
    },


    diario (evento){
        const campo = evento.target

        campo.maxLength = '7'

        let novoValor = campo.value


        if (campo.value.match(/(\d{5})/)){
            novoValor = campo.value.replace(/\W/g,"")
            novoValor= campo.value.replace(/(\d{5})([A-Za-z]{1})/,"$1-$2")
            campo.value = novoValor;

        }else{

            novoValor = campo.value.replace(/\D/g,"");
            campo.value = novoValor;
        }
    },

    nota (evento){
        const campo = evento.target
        campo.type = 'number'

        campo.min = 0
        campo.max = 10
        campo.step = 0.1

        if(campo.value){
            const novoValor = Number.parseFloat(campo.value).toFixed(1)

            campo.value = novoValor
        }
    }
}

export const inicializaCampos = () =>{
    const campos = document.querySelectorAll('[data-mascara]')

    campos.forEach((campo) => {
        const metodo = campo.getAttribute('data-mascara')
        let evento

        if(metodo == 'nota'){
            evento = 'blur'
        }else{
            evento = 'input'
        }

        campo.addEventListener(evento, mascara[metodo])
        campo.dispatchEvent(new Event(evento))
    })
}

inicializaCampos()
