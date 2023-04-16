import requests

def autenticarAPI(username, senha):
    # usuariosAtivos = ['ylanna.santos', 'joaoteixeira.netto', 'ana.marina', 'fabio.santos', 'erick.nascimento', 'tiago.diel', 'josecarlos.souza', 'marilson.braga', 'crisnayra.almeida', 'carlos.gondim', 'eslley.johny']

    try:
        path = "https://api.token-auth.ac.gov.br"
        # path = "http://10.1.4.135:80"

        headers = {
                'Accept': 'application/vnd.token_auth.v1; */*',
                'Requirer': 'auxilio-professores'
        }

        requisicao = {
            'session':{
                'uid': username,
                'password': senha
            }
        }


        secret = 'RXyzAjhSV-QYrf8UG93s'
        response = requests.post(path+'/login', headers= headers, json= requisicao)

        resultado = response.json()

        if resultado['user']['position'] == '':
            resultado['user']['position'] = 'Terceirizado'

        dadosUsuario = {
            'id': resultado['user']['id'],
            'username': resultado['user']['uid'],
            'cpf': resultado['user']['cpf'],
            'nome': resultado['user']['name'],
            'email': resultado['user']['email'],
            'status': True,
        }

        if response.status_code == 200:
            return dadosUsuario
        else:
            return { 'username': '','status' : False }

    except:
        return { 'username': '','status' : False }
