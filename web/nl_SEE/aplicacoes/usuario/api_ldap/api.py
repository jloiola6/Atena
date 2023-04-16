import dotenv
import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Carrega as variaveis de Ambiente
dotenv.load_dotenv(dotenv.find_dotenv())
client = os.getenv('CLIENT_ID')
key = os.getenv('KEY_SECRET')
url_token = os.getenv('URL_TOKEN')



class Contracheque: 
    def __init__(self):
        self.headers = {
            'Content-Type':'application/json',
            'Accept':'application/vnd',
            
        }