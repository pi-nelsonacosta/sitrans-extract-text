from dotenv import load_dotenv
from openai import OpenAI
import openai
import os

# Cargar las variables del archivo .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

async def call_azure_openai(prompt, image_base64):
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que analiza imágenes y extrae información estructurada."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0,  # Mayor precisión
        )

        # Imprime la respuesta cruda para depuración
    ai_response = response.choices[0].message.content
    return ai_response

async def call_azure_openai_DIN(prompt, texto_extraido):
    
    # Preparar el mensaje del usuario combinando el prompt y el texto extraído
    user_message = f"{prompt}\n\nTexto extraído: {texto_extraido}"
    
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente que analiza imágenes y extrae información estructurada."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0,  # Mayor precisión
        )

        # Imprime la respuesta cruda para depuración
    ai_response = response.choices[0].message.content
    return ai_response