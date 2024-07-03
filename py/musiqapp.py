import pathlib
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os
import requests
import webbrowser
import pathlib
import base64
import json


# Antes de fazer qualquer chamada de API, você precisa importar e inicializar o modelo.

teste = genai.configure(api_key=os.environ["API_KEY"])


model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"}, system_instruction="Você é um crítico de arte.")

image1 = {
    'mime_type': 'image/jpeg',
    'data': pathlib.Path('image1.jpg').read_bytes()
}

image2 = {
    'mime_type': 'image/jpeg',
    'data': pathlib.Path('image2.jpg').read_bytes()
}

prompt = """
  Recomende uma música baseada nessas imagens.
  """


# quando se usa mais de um parâmetro, para o prompt, tem que ser uma lista
response = model.generate_content([prompt, image1, image2])
print(response.text)



access_token = 'BQAsWi_zSwcjCl-UVtiAeDbfAUmhroWN5LxOdwDKhdXHwUW8xPNCW9QR4bhDu0Bh5TaeceS7Gkf2pgLRvVWeUdHpKHuNJQUENTDg9kRtRAIu7YFSwOQ'

# Endpoint da API do Spotify para buscar músicas
url = 'https://api.spotify.com/v1/search'

nome_musica = response.text

# Parâmetros da requisição (busca por tipo 'track' e nome da música 'Post')
params = {
    'q': nome_musica,
    'type': 'track',
    'market': 'US',
    'limit': 1,

}

# Cabeçalho da requisição com o token de acesso
headers = {
    'Authorization': 'Bearer ' + access_token
}

# Fazendo a requisição GET
response = requests.get(url, headers=headers, params=params)

# Verifica se a requisição foi bem-sucedida

link = ''
if response.status_code == 200:
    # Exibe o resultado da busca
    data = response.json()
    items = data['tracks']['items']
    link = items[0]['external_urls']['spotify']
    
    print(link)
    webbrowser.open(link)
else:
    print('Erro na requisição:', response.status_code, response.text)