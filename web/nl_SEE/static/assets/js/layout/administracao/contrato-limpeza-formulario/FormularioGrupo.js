// ADICIONAR REQUIRED

export const FormularioGrupo = (contador) => {
    const html = `
        <div>
            <div>
                <div class="formulario-grupo">
                    <h3 class="texto-medio texto-azul">Item (Área interna)</h3>
                </div>

                <div class="contrato-item-grupo-campos">
                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_item">N° do item</label>
                        <input class="campo-texto " type="text" value="" name="numero_item${contador}" id="campo-numero_item" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_lote">N° do Lote</label>
                        <input class="campo-texto " type="text" value="" name="numero_lote${contador}" id="campo-numero_lote" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label for="selecao-metragem" class="texto-azul label-campo">M² contratado</label>

                        <select class="campo-texto campo-pequeno" name="metragem${contador}" id="selecao-metragem" data-selecao-metragem>
                            <option value="600">600</option>
                            <option value="800">800</option>
                        </select>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-metragem">M² mensal</label>
                        <input class="campo-texto " type="text" value="" name="metragem_mensal${contador}" id="campo-metragem" maxlength="9" autocomplete="off" data-mascara="numero" data-metragem-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_unitario">Valor unitário</label>
                        <input class="campo-texto " type="text" value="" name="valor_unitario${contador}" id="campo-valor_unitario" maxlength="30" autocomplete="off" data-mascara="moeda" data-unitario-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-quantidade">Quantidade</label>
                        <input class="campo-texto " type="text" value="" name="quantidade${contador}" id="campo-quantidade" autocomplete="off" data-mascara="numero" data-qtd-item readonly>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_total">Valor total</label>
                        <input class="campo-texto " type="text" value="" name="valor_total${contador}" id="campo-valor_total" maxlength="30" autocomplete="off" data-mascara="moeda" data-total-item readonly>
                    </div>
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-descricao">Descrição</label>
                    <textarea maxlength="300" class="campo-area campo-texto item-descricao" name="descricao${contador}" id="campo-descricao"></textarea>
                </div>
            </div>

            <div>
                <div class="formulario-grupo">
                    <h3 class="texto-medio texto-azul">Item (Área externa)</h3>
                </div>

                <div class="contrato-item-grupo-campos">
                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_item">N° do item</label>
                        <input class="campo-texto " type="text" value="" name="numero_item${contador + 1}" id="campo-numero_item" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_lote">N° do Lote</label>
                        <input class="campo-texto " type="text" value="" name="numero_lote${contador + 1}" id="campo-numero_lote" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label for="selecao-metragem" class="texto-azul label-campo">M² contratado</label>

                        <select class="campo-texto campo-pequeno" name="metragem${contador + 1}" id="selecao-metragem" data-selecao-metragem>
                            <option value="1200">1200</option>
                            <option value="1800">1800</option>
                        </select>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-metragem">M² mensal</label>
                        <input class="campo-texto " type="text" value="" name="metragem_mensal${contador + 1}" id="campo-metragem" maxlength="9" autocomplete="off" data-mascara="numero" data-metragem-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_unitario">Valor unitário</label>
                        <input class="campo-texto " type="text" value="" name="valor_unitario${contador + 1}" id="campo-valor_unitario" maxlength="30" autocomplete="off" data-mascara="moeda" data-unitario-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-quantidade">Quantidade</label>
                        <input class="campo-texto " type="text" value="" name="quantidade${contador + 1}" id="campo-quantidade" autocomplete="off" data-mascara="numero" data-qtd-item readonly>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_total">Valor total</label>
                        <input class="campo-texto " type="text" value="" name="valor_total${contador + 1}" id="campo-valor_total" maxlength="30" autocomplete="off" data-mascara="moeda" data-total-item readonly>
                    </div>
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-descricao">Descrição</label>
                    <textarea maxlength="300" class="campo-area campo-texto item-descricao" name="descricao${contador + 1}" id="campo-descricao"></textarea>
                </div>
            </div>

            <div>
                <div class="formulario-grupo">
                    <h3 class="texto-medio texto-azul">Item (Esquadrias)</h3>
                </div>

                <div class="contrato-item-grupo-campos">
                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_item">N° do item</label>
                        <input class="campo-texto " type="text" value="" name="numero_item${contador + 2}" id="campo-numero_item" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-numero_lote">N° do Lote</label>
                        <input class="campo-texto " type="text" value="" name="numero_lote${contador + 2}" id="campo-numero_lote" maxlength="3" autocomplete="off" data-mascara="numero">
                    </div>

                    <div class="formulario-grupo">
                        <label for="selecao-metragem" class="texto-azul label-campo">M² contratado</label>

                        <select class="campo-texto campo-pequeno" name="metragem${contador + 2}" id="selecao-metragem" data-selecao-metragem>
                            <option value="220">220</option>
                            <option value="300">300</option>
                        </select>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-metragem">M² mensal</label>
                        <input class="campo-texto " type="text" value="" name="metragem_mensal${contador + 2}" id="campo-metragem" maxlength="9" autocomplete="off" data-mascara="numero" data-metragem-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_unitario">Valor unitário</label>
                        <input class="campo-texto " type="text" value="" name="valor_unitario${contador + 2}" id="campo-valor_unitario" maxlength="30" autocomplete="off" data-mascara="moeda" data-unitario-item>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-quantidade">Quantidade</label>
                        <input class="campo-texto " type="text" value="" name="quantidade${contador + 2}" id="campo-quantidade" autocomplete="off" data-mascara="numero" data-qtd-item readonly>
                    </div>

                    <div class="formulario-grupo">
                        <label class="texto-azul label-campo" for="campo-valor_total">Valor total</label>
                        <input class="campo-texto " type="text" value="" name="valor_total${contador + 2}" id="campo-valor_total" maxlength="30" autocomplete="off" data-mascara="moeda" data-total-item readonly>
                    </div>
                </div>

                <div class="formulario-grupo">
                    <label class="texto-azul label-campo" for="campo-descricao">Descrição</label>
                    <textarea maxlength="300" class="campo-area campo-texto item-descricao" name="descricao${contador + 2}" id="campo-descricao"></textarea>
                </div>
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