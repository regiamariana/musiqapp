import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os

# Antes de fazer qualquer chamada de API, você precisa importar e inicializar o modelo.

teste = genai.configure(api_key=os.environ["API_KEY"])

print(teste)

model = genai.GenerativeModel('gemini-1.5-flash')

print(model)

response = model.generate_content("Write a story about a AI and magic")
print(response.text)