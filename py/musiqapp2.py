import os
import pathlib
from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import webbrowser


load_dotenv()


genai.configure(api_key=os.getenv("API_KEY"))


model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})


app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Verifica se os arquivos de imagem foram enviados
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Duas imagens são necessárias'}), 400
       
        image1_file = request.files['image1']
        image2_file = request.files['image2']
       


       
        # Lê os bytes das imagens
        image1 = {
            'mime_type': image1_file.content_type,
            'data': image1_file.read()
        }
       
        image2 = {
            'mime_type': image2_file.content_type,
            'data': image2_file.read()
        }


        # Lê o texto do prompt
        prompt_template = request.form.get('prompt', 'Recomende uma música baseada nessas imagens.')


        prompt = f'Recomende uma música baseada nessas imagens e no seguinte gênero {prompt_template}';


        # Gera o conteúdo usando o modelo
        response = model.generate_content([prompt, image1, image2])
        nome_musica = response.text


        # Endpoint da API do Spotify para buscar músicas
        url = 'https://api.spotify.com/v1/search'
        access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")


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
        spotify_response = requests.get(url, headers=headers, params=params)


        # Verifica se a requisição foi bem-sucedida
        if spotify_response.status_code == 200:
            # Exibe o resultado da busca
            data = spotify_response.json()
            items = data['tracks']['items']
            link = items[0]['external_urls']['spotify']
           
            webbrowser.open(link)
           
            return jsonify({'response': 'ok'}), 200;
        else:
            return jsonify({'error': 'Erro na requisição Spotify', 'details': spotify_response.text}), spotify_response.status_code
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)