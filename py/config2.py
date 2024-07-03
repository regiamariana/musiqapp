import pathlib
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os

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
  Recomende uma música baseada nessas imagens, com o link da música no spotify ou videoclipe no youtube.
  """


# quando se usa mais de um parâmetro, para o prompt, tem que ser uma lista
response = model.generate_content([prompt, image1, image2])
print(response.text)