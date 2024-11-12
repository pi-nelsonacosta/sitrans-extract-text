from fastapi import HTTPException
from app.business.multiagents.multiagents import organize_extracted_text_AFORO
import numpy as np
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string

async def extract_text_from_aforo(file_content):
    """
    Procesa la imagen con OCR y organiza el texto extraído.
    """
    try:
        # Verifica si file_content es bytes o una imagen ya cargada
        if isinstance(file_content, bytes):
            # Si es bytes, convierte a una imagen
            imagen = Image.open(BytesIO(file_content))
        elif isinstance(file_content, Image.Image):
            # Si ya es una imagen, úsala directamente
            imagen = file_content
        else:
            raise TypeError("file_content debe ser de tipo bytes o PIL.Image.Image.")

        # Extraer texto de la imagen con PyTesseract
        texto_ocr = image_to_string(imagen, lang="eng+spa")
        texto_extraido = texto_ocr

        # Llamar a la función para organizar el texto extraído
        await organize_extracted_text_AFORO(texto_extraido)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")