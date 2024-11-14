import base64
import json
import os
from fastapi import HTTPException
from io import BytesIO
from pdf2image import convert_from_bytes
from dotenv import load_dotenv
from openai import OpenAI
import openai
import requests

# Cargar las variables del archivo .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

async def extract_text_from_tgr():
    """
    Procesa la imagen con OCR y organiza el texto extraído para TGR.
    """
    try:
        # Llamar a la función para organizar el texto extraído
        await organize_extracted_text_TGR()

    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no soportado: {str(te)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

async def organize_extracted_text_TGR():
    try:
        # URL del PDF
        hardcoded_url = "https://drive.google.com/uc?id=1gH9cPVooRy1mgsGjrnSqatyEXjQiL0TT&export=download"

        # Descargar el archivo PDF
        print(f"Descargando archivo desde URL: {hardcoded_url}")
        response = requests.get(hardcoded_url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"No se pudo descargar el archivo desde la URL. Código de estado: {response.status_code}"
            )

        # Convertir el PDF en imágenes
        print("Convirtiendo PDF en imágenes...")
        images = convert_from_bytes(response.content, dpi=300)

        # Tomar solo la primera página del PDF
        first_page = images[0]

        # Convertir la primera página a Base64
        buffered = BytesIO()
        first_page.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Verificar longitud de la imagen codificada
        print("Longitud de la imagen en Base64:", len(image_base64))

        # Prompt para GPT
        prompt = """
        Analiza el contenido de esta imagen y devuelve únicamente los datos en el siguiente formato JSON:
        {
            "solicitud": "", 
            "rutConsignatario": "", 
            "formularioConsignatario": "", 
            "folioDIN": "", 
            "vencimientoDIN": "", 
            "monedaPago": "", 
            "totalPagado": "",
            "fechaPago": "", 
            "institucionRecaudadora": "", 
            "identificadorTransaccion": ""
        }
        """

        # Llamada al modelo GPT-4o
        print("Enviando imagen a GPT-4o...")
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

        # Respuesta cruda
        ai_response = response.choices[0].message.content
        print(ai_response)
        
        return ai_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")    