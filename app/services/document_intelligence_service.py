from PIL import Image
from pdf2image import convert_from_bytes
import easyocr
import numpy as np
import os
from fastapi import HTTPException
from app.business.convert_pdf_to_image import convert_pdf_image
from app.services.external_services.azure_openai_service import call_azure_openai, call_azure_openai_DIN
from app.business.prompts.prompts_extract import prompt_aforo, prompt_tgr, prompt_din

async def organize_extracted_text_AFORO(file_content: bytes):
    try:
        # Convertir el PDF en imágenes
        image_base64 = await convert_pdf_image(file_content)
       
        # Imprime la respuesta cruda para depuración
        response = await call_azure_openai(prompt_aforo, image_base64)
        print("Respuesta cruda de GPT:", response)

        # Validar si la respuesta está vacía
        if not response.strip():
            raise HTTPException(status_code=500, detail="El modelo GPT devolvió una respuesta vacía.")
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

async def organize_extracted_text_TGR(file_content: bytes):
    try:
        # Convertir el PDF en imágenes
        image_base64 = await convert_pdf_image(file_content)
                
        # Imprime la respuesta cruda para depuración
        response = await call_azure_openai(prompt_tgr, image_base64)
        print("Respuesta cruda de GPT:", response)

        # Validar si la respuesta está vacía
        if not response.strip():
            raise HTTPException(status_code=500, detail="El modelo GPT devolvió una respuesta vacía.")
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")       

async def organize_extracted_text_DIN(file_content):
    """
    Procesa un PDF con OCR y organiza el texto extraído.
    """
    try:
        # Convertir el contenido del PDF en una lista de imágenes
        try:
            images = convert_from_bytes(file_content)
        except Exception as e:
            raise TypeError(f"El contenido no se pudo convertir en imágenes: {str(e)}")

        texto_extraido = []

        # Inicializar EasyOCR una vez
        reader = easyocr.Reader(['es', 'en'])

        # Procesar cada página convertida en imagen
        for imagen in images:
            # Convertir a numpy array
            imagen_np = np.array(imagen)
            result = reader.readtext(imagen_np)
            texto_extraido.extend([res[1] for res in result])

        # Combinar el texto extraído de todas las páginas
        texto_final = "\n".join(texto_extraido)
        
        # Imprime la respuesta cruda para depuración
        response = await call_azure_openai_DIN(prompt_din, texto_final)
        print("Respuesta cruda de GPT:", response)
      
        return response

    except Exception as e:
        # Registrar el error y no interrumpir el flujo de la tarea
        print(f"Error al procesar el PDF en segundo plano: {str(e)}")
        return None



