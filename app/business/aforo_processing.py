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

async def extract_text_from_aforo():
    """
    Procesa la imagen con OCR y organiza el texto extraído.
    """
    try:
        # Llamar a la función para organizar el texto extraído
        result = await organize_extracted_text_AFORO()
        return result

    except Exception as e:
        print(f"Error en extract_text_from_aforo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

async def organize_extracted_text_AFORO():
    """
    Procesa un archivo PDF desde una URL, convierte las páginas a imágenes compatibles,
    y utiliza GPT para mapear su contenido al esquema JSON.
    """
    try:
        # URL del PDF
        hardcoded_url = "https://drive.google.com/uc?id=1AgBj7R8EfvpTEsaZJJQJSrE4cdoLUqd_&export=download"

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

        # Prompt simplificado
        prompt = """
        Analiza el contenido de esta imagen estructurada y extrae los datos en el siguiente formato JSON:
        {
            "solicitud":"", 
            "folioDIN":"", 
            "fechaAceptacion":"””", 
            "numeroEncriptado":"", 
            "codigoAgente":"””", 
            "nombreAgente":"””", 
            "codigoAduanaTramitacion":"””", 
            "tipoRevision":"””", 
            "FirmaAgencia":"””" 
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

        # Imprime la respuesta cruda para depuración
        ai_response = response.choices[0].message.content
        print("Respuesta cruda de GPT:", ai_response)

        # Validar si la respuesta está vacía
        if not ai_response.strip():
            raise HTTPException(status_code=500, detail="El modelo GPT devolvió una respuesta vacía.")

        # Intentar convertir la respuesta en JSON
        try:
            parsed_json = json.loads(ai_response)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Error al procesar el JSON. Respuesta cruda: {ai_response}")

        # Validar campos del JSON
        expected_keys = [
            "solicitud", "rutConsignatario", "formularioConsignatario", "folioDIN",
            "vencimientoDIN", "monedaPago", "totalPagado", "fechaPago",
            "institucionRecaudadora", "identificadorTransaccion"
        ]
        for key in expected_keys:
            if key not in parsed_json:
                parsed_json[key] = ""

        print("Resultados del procesamiento:", json.dumps(parsed_json, indent=4, ensure_ascii=False))
        return parsed_json

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el archivo: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")   