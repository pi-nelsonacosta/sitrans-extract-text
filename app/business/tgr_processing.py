from fastapi import HTTPException
from app.business.multiagents.multiagents import organize_extracted_text_TGR
import numpy as np
from PIL import Image
from io import BytesIO
import pytesseract

async def extract_text_from_tgr(file_content: bytes):
    """
    Procesa la imagen con OCR y llama a la función de procesamiento del texto extraído.
    """
    try:
        # Procesar la imagen con PyTesseract
        imagen = Image.open(BytesIO(file_content))
        texto_ocr = pytesseract.image_to_string(imagen)
        texto_extraido = texto_ocr
        
        # Llamar a la función para organizar el texto extraído
        await organize_extracted_text_TGR(texto_extraido)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}") 