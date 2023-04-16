import datetime
import mysql.connector


def salvarBanco():
    con = mysql.connector.connect(host='localhost',database='secretaria', user='see',password='dtmisee@', auth_plugin='mysql_native_password')

    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado ao servidor MySQL versão ",db_info)
        cursor = con.cursor()
        data_atual = datetime.date.today()

        cursor.execute(f"update secretaria.terceirizacao_servidor_ocorrencia_funcional set status = 0 where '{data_atual}' not between data_inicio and data_termino;")
        con.commit()

        cursor.execute(f"UPDATE secretaria.lotacao_servidor_ocorrencia_funcional AS fun INNER JOIN secretaria.lotacao_servidor_contrato AS cont ON fun.contrato_id= cont.id SET cont.situacao = 'EM EXERCÍCIO' WHERE '{data_atual}' not between fun.data_inicio and fun.data_termino;")
        con.commit()

        cursor.execute(f"update secretaria.lotacao_servidor_ocorrencia_funcional set status = 0 where '{data_atual}' not between data_inicio and data_termino;")
        con.commit()

        cursor.execute(f"update secretaria.lotacao_servidor_hora_complementar set status = 0 where '{data_atual}' not between data_inicio and data_termino;")
        con.commit()

        cursor.execute(f"update secretaria.lotacao_servidor_gratificacao set status = 0 where '{data_atual}' not between data_inicio and data_termino;")
        con.commit()

        cursor.execute(f"update secretaria.lotacao_servidor_contrato_aditivo set status = 0 where '{data_atual}' > data_termino;")
        con.commit()

        cursor.execute(f"update secretaria.lotacao_servidor_lotacao set status = 0, motivo = 'Lotação inativada pois chegou na data de término' where '{data_atual}' > data_termino;")
        con.commit()

        cursor.execute(f"UPDATE secretaria.lotacao_servidor_contrato as con INNER JOIN secretaria.lotacao_servidor_contrato_aditivo as adit on con.id = adit.contrato_id set situacao = 'EXONERADO/RESCISO' where '{data_atual}' > adit.data_termino and adit.status = 1;")
        con.commit()

        cursor.execute(f"UPDATE secretaria.lotacao_servidor_contrato as con set con.situacao = 'EXONERADO/RESCISO' where id not in (select contrato_id from secretaria.lotacao_servidor_contrato_aditivo as adit WHERE adit.status = 1) and '{data_atual}' > con.data_termino;")
        con.commit()

        cursor.execute(f"UPDATE secretaria.lotacao_servidor_ocorrencia_funcional AS fun INNER JOIN secretaria.lotacao_servidor_lotacao AS lot ON fun.contrato_id = lot.contrato_id SET lot.status= 0, lot.motivo= 'LOTAÇÃO INATIVA POR CONTA DA OCORRÊNCIA FUNCIONAL.' WHERE '{data_atual}' between fun.data_inicio and fun.data_termino and lot.status= 1;")
        con.commit()

        cursor.execute(f"UPDATE secretaria.lotacao_servidor_ocorrencia_funcional AS fun INNER JOIN secretaria.lotacao_servidor_lotacao AS lot ON fun.contrato_id = lot.contrato_id SET lot.status= 1, lot.motivo= NULL WHERE '{data_atual}' not between fun.data_inicio and fun.data_termino and lot.motivo= 'LOTAÇÃO INATIVA POR CONTA DA OCORRÊNCIA FUNCIONAL.';")
        con.commit()

    if con.is_connected():
        cursor.close()
        con.close()
        print("Conex�o ao MySQL foi encerrada")


salvarBanco()
