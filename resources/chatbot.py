!pip install google-genai

import os
from google.colab import userdata
os.environ['GOOGLE_API_KEY'] = userdata.get('GOOGLE_API_KEY')

from google import genai

client = genai.Client()
#for model in client.models.list():
#  print(model.name)

genai_model = "gemini-2.0-flash"
request = "Quem é a empresa por trás dos modelos Gemini?"
response = client.models.generate_content(model=genai_model, contents=request)
print(response.text)

from google.genai import types

chat_config = types.GenerateContentConfig(system_instruction="Você é um assistente pessoal e você sempre responde de forma sucinta.")

chat = client.chats.create(model=genai_model,config=chat_config)

question = "O que é computação quantica?"

response = chat.send_message(question)
print(response.text)

prompt = input("Digite sua opção: ")
while (prompt != "sim"):
  response = chat.send_message(prompt)
#  response = client.models.generate_content(model=genai_model, contents=prompt)
  print("Resposta: ", response.text)
  print("\r\n\r\n")
  prompt = input("Digite sua opção: ")

chat_config2 = types.GenerateContentConfig(system_instruction="Você é um assistente que sempre responde de forma sarcástica.")

chat2 = client.chats.create(model=genai_model,config=chat_config2)

question = "O que é computação quantica?"

response = chat2.send_message(question)
print(response.text)
