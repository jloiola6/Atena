(() => {
    const validaCpf = (cpf) => {
        // Verificando se todos os números digitados são iguais
        let tudoIgual = true

        for(let i=0; i < cpf.length - 1; i++)
            if(cpf[i] != cpf[i+1]){
                tudoIgual = false
                break
            }

        if(tudoIgual)
            return false

        const digito1 = Number.parseInt(cpf[9])
        const digito2 = Number.parseInt(cpf[10])
        
        // Verificando o primeiro digito
        let aux = 10
        let soma = 0

        for(let i=0; i < cpf.length - 2; i++ ){
            const numero = Number.parseInt(cpf[i])
            
            soma += numero * aux
            aux--
        }

        soma *= 10
        
        let resultado = soma % 11

        if(resultado >= 10)
            resultado = 0


        if(resultado != digito1)
            return false

        // Verificando o segundo dígito
        aux = 11
        soma = 0

        for(let i=0; i < cpf.length - 1; i++){
            const numero = Number.parseInt(cpf[i])

            soma += numero * aux
            aux --
        }

        soma *= 10

        resultado = soma % 11

        if(resultado >= 10)
            resultado = 0
        
        if(resultado != digito2)
            return false

        return true
    }

    // Controlando os elementos da página de acordo com o valor digitado
    const verificarCampo = (evento) => {
        const valor = evento.target.value.replace(/\D/g ,'')
        const botaoConsulta = document.querySelector('[data-botao-consulta]')
        const mensagemErro = document.querySelector('[data-mensagem-erro]')

        if(valor.length == 11){
            const valido = validaCpf(valor)

            botaoConsulta.disabled = !valido

            if(valido)
                mensagemErro.classList.add('oculto')
            else
                mensagemErro.classList.remove('oculto')

        }else{
            botaoConsulta.disabled = true
            mensagemErro.classList.add('oculto')
        }


    }

    const campoCpf = document.querySelector('[data-campo-cpf]')
    campoCpf.addEventListener('input', verificarCampo)
})

()

