import base64
import json
import os
from fastapi import HTTPException
from app.business.convert_pdf_to_image import convert_pdf_image
from app.services.external_services.azure_openai_service import call_azure_openai
from pdf2image import convert_from_bytes
from app.business.prompts.prompts_extract import prompt_aforo
from dotenv import load_dotenv
from openai import OpenAI
import openai
import requests

# Cargar las variables del archivo .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

async def organize_extracted_text_AFORO(file_content: bytes):
    try:
        # Convertir el PDF en imágenes
        print("Convirtiendo PDF en imágenes...")
        image_base64 = await convert_pdf_image(file_content)
        
        # Llamada al modelo GPT-4o
        print("Enviando imagen a GPT-4o...")
        
        # Imprime la respuesta cruda para depuración
        ai_response = await call_azure_openai(prompt_aforo, image_base64)
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