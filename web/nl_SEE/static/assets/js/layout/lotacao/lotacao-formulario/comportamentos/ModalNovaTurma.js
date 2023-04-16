// Script para encapsular uma função que retorna o modal de formulário de nova turma

const ModalNovaTurma = (contador, etapas) => {
    const div = document.createElement('div')
    div.classList.add('modal')
    div.setAttribute('data-modal', `data-nova-turma${contador}`)
    div.toggleAttribute('data-modal-bloqueado')

    const html = `
        <div class="modal-conteudo">
            <h3 class="texto-medio texto-azul">Nova turma</h3>
            <p class="texto-preto descricao">Insira os dados da turma</p>


            <div class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-etapa">Etapa</label>
                <select data-selecao-etapa id="campo-etapa" name="etapa${contador}" class="campo-texto campo-grande"></select>
            </div>

            <div class="formulario-grupo" data-grupo-ano>
                <label class="texto-azul label-campo" for="">Ano / Série</label>

                <select data-selecao-ano="2" id="campo-infantil" name="infantil${contador}" class="campo-texto campo-medio">
                    <option value="Ensino Infantil - Pré I">Ensino Infantil - Pré I</option>
                    <option value="Ensino Infantil - Pré II">Ensino Infantil - Pré II</option>
                    <option value="Ensino Infantil - Pré III">Ensino Infantil - Pré III</option>
                </select>

                <select data-selecao-ano="3" id="campo-fundamental1" name="fundamental1${contador}" class="campo-texto campo-medio">
                    <option value="1º Ano">1º Ano</option>
                    <option value="2º Ano">2º Ano</option>
                    <option value="3º Ano">3º Ano</option>
                    <option value="4º Ano">4º Ano</option>
                    <option value="5º Ano">5º Ano</option>
                </select>

                <select data-selecao-ano="4" id="campo-fundamental2" name="fundamental2${contador}" class="campo-texto campo-medio">
                    <option value="6º Ano">6º Ano</option>
                    <option value="7º Ano">7º Ano</option>
                    <option value="8º Ano">8º Ano</option>
                    <option value="9º Ano">9º Ano</option>
                </select>

                <select data-selecao-ano="5" id="campo-medio" name="medio${contador}" class="campo-texto campo-medio">
                    <option value="1ª Série">1ª Série</option>
                    <option value="2ª Série">2ª Série</option>
                    <option value="3ª Série">3ª Série</option>
                </select>

                <select data-selecao-ano="6" id="campo-medio-integral" name="medio-integral${contador}" class="campo-texto campo-medio">
                    <option value="1ª Série">1ª Série</option>
                    <option value="2ª Série">2ª Série</option>
                    <option value="3ª Série">3ª Série</option>
                </select>

                <select data-selecao-ano="7" id="campe-eja-fundamental" name="eja-f1${contador}" class="campo-texto campo-medio">
                    <option value="EJA - FUNDAMENTAL I">EJA - FUNDAMENTAL I</option>
                    <option value="EJA - FUNDAMENTAL II">EJA - FUNDAMENTAL II</option>
                </select>

                <select data-selecao-ano="8" class="campo-texto campo-medio" name="eja-medio${contador}" id="campo-eja-medio">
                    <option value="EJA - MÉDIO">EJA - MÉDIO</option>
                </select>

                <select data-selecao-ano="9" class="campo-texto campo-medio" name="eja-profissional${contador}" id="campo-eja-pro">
                    <option value="EJA - EDUCAÇÃO PROFISSIONAL">EJA - EDUCAÇÃO PROFISSIONAL</option>
                </select>

                <select data-selecao-ano="10" class="campo-texto campo-medio" name="aee${contador}" id="campo-aee">
                    <option value="AEE/AC">AEE/AC</option>
                </select>

                <select data-selecao-ano="11" class="campo-texto campo-medio" name="pac${contador}" id="campo-pac">
                    <option value="PAC">PAC</option>
                </select>

                <select data-selecao-ano="12" id="campo-iniciais" name="campo-inciais1${contador}" class="campo-texto campo-grande">
                    <option value="Educação no Campo - 1º Ano">Educação no Campo - 1º Ano</option>
                    <option value="Educação no Campo - 2º Ano">Educação no Campo - 2º Ano</option>
                    <option value="Educação no Campo - 3º Ano">Educação no Campo - 3º Ano</option>
                    <option value="Educação no Campo - 4º Ano">Educação no Campo - 4º Ano</option>
                    <option value="Educação no Campo - 5º Ano">Educação no Campo - 5º Ano</option>
                </select>

                <select data-selecao-ano="13" id="campo-finais" name="campo-finais2${contador}" class="campo-texto campo-grande">
                    <option value="Educação no Campo - 6º Ano">Educação no Campo - 6º Ano</option>
                    <option value="Educação no Campo - 7º Ano">Educação no Campo - 7º Ano</option>
                    <option value="Educação no Campo - 8º Ano">Educação no Campo - 8º Ano</option>
                    <option value="Educação no Campo - 9º Ano">Educação no Campo - 9º Ano</option>
                </select>

                <select data-selecao-ano="14" id="campo-campo-medio" name="campo-medio${contador}" class="campo-texto campo-grande">
                    <option value="Educação no Campo - 1ª Série">Educação no Campo - 1ª Série</option>
                    <option value="Educação no Campo - 2ª Série">Educação no Campo - 2ª Série</option>
                    <option value="Educação no Campo - 3ª Série">Educação no Campo - 3ª Série</option>
                </select>

                <select data-selecao-ano="15" id="socio-iniciais" name="socio-inciais1${contador}" class="campo-texto campo-grande">
                    <option value="Ensino Socioeducativo - Etapa I (1º e 2º)">Ensino Socioeducativo - Etapa I (1º e 2º)</option>
                    <option value="Ensino Socioeducativo - Etapa II (3º, 4º e 5º)">Ensino Socioeducativo - Etapa II (3º, 4º e 5º)</option>
                </select>

                <select data-selecao-ano="16" id="socio-finais" name="socio-finais2${contador}" class="campo-texto campo-grande">
                    <option value="Ensino Socioeducativo - Etapa III (6º e 7º)">Ensino Socioeducativo - Etapa III (6º e 7º)</option>
                    <option value="Ensino Socioeducativo - Etapa IV (8º e 9º)">Ensino Socioeducativo - Etapa IV (8º e 9º)</option>
                </select>

                <select data-selecao-ano="17" id="campo-socio-medio" name="socio-medio${contador}" class="campo-texto campo-grande">
                    <option value="Ensino Socioeducativo - 1ª Série">Ensino Socioeducativo - 1ª Série</option>
                    <option value="Ensino Socioeducativo - 2ª Série">Ensino Socioeducativo - 2ª Série</option>
                    <option value="Ensino Socioeducativo - 3ª Série">Ensino Socioeducativo - 3ª Série</option>
                </select>

                <select data-selecao-ano="18" class="campo-texto campo-grande" name="socio-eja-fundamental1${contador}" id="campo-socio-eja">
                    <option value="Socioeducativo EJA - FUNDAMENTAL I">Socioeducativo EJA - FUNDAMENTAL I</option>
                </select>

                <select data-selecao-ano="19" class="campo-texto campo-grande" name="socio-eja-fundamental2${contador}" id="campo-socio-eja">
                    <option value="Socioeducativo EJA - FUNDAMENTAL II">Socioeducativo EJA - FUNDAMENTAL II</option>
                </select>

                <select data-selecao-ano="20" class="campo-texto campo-grande" name="socio-eja-medio${contador}" id="campo-socio-eja">
                    <option value="Socioeducativo EJA - MÉDIO">Socioeducativo EJA - MÉDIO</option>
                </select>
            </div>

            <div class="formulario-grupo" data-grupo-turma>
                <label class="texto-azul label-campo"  for="campo-turma">Turma</label>

                <select data-selecao-letra id="campo-turma" name="turma${contador}" class="campo-texto campo-medio" >
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                    <option value="G">G</option>
                    <option value="H">H</option>
                    <option value="I">I</option>
                    <option value="J">J</option>
                    <option value="K">K</option>
                    <option value="L">L</option>
                    <option value="M">M</option>
                    <option value="N">N</option>
                    <option value="O">O</option>
                    <option value="P">P</option>
                    <option value="Q">Q</option>
                    <option value="R">R</option>
                    <option value="S">S</option>
                    <option value="T">T</option>
                    <option value="U">U</option>
                    <option value="V">V</option>
                    <option value="W">W</option>
                    <option value="X">X</option>
                    <option value="Y">Y</option>
                    <option value="Z">Z</option>
                </select>

                <select data-selecao-eja id="campo-modulo" name="modulo${contador}" class="campo-texto campo-medio" >
                    <option value="Módulo I">Módulo I</option>
                    <option value="Módulo I - A">Módulo I - A</option>
                    <option value="Módulo I - B">Módulo I - B</option>
                    <option value="Módulo II">Módulo II</option>
                    <option value="Módulo II - A">Módulo II - A</option>
                    <option value="Módulo II - B">Módulo II - B</option>
                    <option value="Módulo III">Módulo III</option>
                    <option value="Módulo III - A">Módulo III - A</option>
                    <option value="Módulo III - B">Módulo III - B</option>
                    <option value="Módulo IV">Módulo IV</option>
                    <option value="Módulo IV - A">Módulo IV - A</option>
                    <option value="Módulo IV - B">Módulo IV - B</option>
                    <option value="Módulo V">Módulo V</option>
                    <option value="Módulo V - A">Módulo V - A</option>
                    <option value="Módulo V - B">Módulo V - B</option>

                    <option value="Etapa 1 - A">Etapa 1 - A</option>
                    <option value="Etapa 1 - B">Etapa 1 - B</option>

                    <option value="Etapa 2 - A">Etapa 2 - A</option>
                    <option value="Etapa 2 - B">Etapa 2 - B</option>

                    <option value="Etapa 3 - A">Etapa 3 - A</option>
                    <option value="Etapa 3 - B">Etapa 3 - B</option>

                    <option value="Etapa 4 - A">Etapa 4 - A</option>
                    <option value="Etapa 4 - B">Etapa 4 - B</option>
                </select>
            </div>

            <div class="formulario-grupo">
                <label class="texto-azul label-campo" for="campo-turno">Turno</label>

                <select data-selecao-turno id="campo-turno" name="turno${contador}" class="campo-texto campo-medio">
                    <option value="Matutino">Matutino</option>
                    <option value="Vespertino">Vespertino</option>
                    <option value="Noturno">Noturno</option>
                    <option value="Integral">Integral</option>
                </select>
            </div>

            <div class="container-botoes">
                <button class="botao--verde botao" data-salvar-turma>Salvar</button>
                <button class="botao--vermelho botao" data-cancelar-turma>Cancelar</button>
            </div>
        </div>
    `

    div.innerHTML = html

    const selecaoEtapas = div.querySelector('[data-selecao-etapa]')

    etapas.forEach((etapa) => {
        selecaoEtapas.innerHTML += `
            <option value="${etapa.id}">${etapa.etapa}</option>
        `
    })

    return div
}