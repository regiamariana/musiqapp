import requests
import webbrowser

# Substitua 'your_access_token' pelo token de acesso obtido
access_token = 'BQAnPj3RRKy0J89yox-Mb4HA94D8yr9YB_JSWD74GJW7WoDX718AbnrwSdMxFUkZIkhhvgTdc1PToZFxRa0sYRvBn5q1SWucex2a4zlTNN4DBLiYAY0'

# Endpoint da API do Spotify para buscar músicas
url = 'https://api.spotify.com/v1/search'

nome_musica = input('digite o nome da musica: ')

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



