// ADICIONAR REQUIRED

export const FormularioGrupo = (contador) => {
    const html = `
        <div>
            <div class="formulario-grupo">
                <h3 class="texto-medio texto-azul">Item do contrato</h3>
            </div>

            <div class="contrato-item-grupo-campos">
                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-numero_item">N° do item</label>
                    <input class="campo-texto" type="text" value="" name="numero_item${contador}" id="campo-numero_item" maxlength="3" autocomplete="off" data-mascara="numero">
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-numero_lote">N° do Lote</label>
                    <input class="campo-texto" type="text" value="" name="numero_lote${contador}" id="campo-numero_lote" maxlength="3" autocomplete="off" data-mascara="numero">
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-quantidade">Quantidade</label>
                    <input class="campo-texto" type="text" value="" name="quantidade${contador}" id="campo-quantidade" maxlength="9" autocomplete="off" data-mascara="numero" data-qtd-item>
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-remuneracao">Remuneração</label>
                    <input class="campo-texto campo-item-valor" type="text" value="" name="remuneracao${contador}" id="campo-remuneracao" maxlength="30" autocomplete="off" data-mascara="moeda" >
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-valor_unitario">Valor unitário</label>
                    <input class="campo-texto" type="text" value="" name="valor_unitario${contador}" id="campo-valor_unitario" maxlength="30" autocomplete="off" data-mascara="moeda" data-unitario-item>
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-valor_total">Valor total</label>
                    <input class="campo-texto" type="text" value="" name="valor_total${contador}" id="campo-valor_total" maxlength="30" autocomplete="off" data-mascara="moeda" data-total-item readonly>
                </div>
            </div>

            <div class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-descricao">Descrição</label>
                <textarea maxlength="300" class="campo-area campo-texto item-descricao" name="descricao${contador}" id="campo-descricao"></textarea>
            </div>

            <div class="container-botoes">
                <button class="botao botao--vermelho" data-botao-excluir-item>Excluir</button>
            </div>
        </div>
    `
    const div = document.createElement('div')
    div.innerHTML = html

    return div
}