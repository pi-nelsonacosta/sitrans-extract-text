# business/use_cases/extract_text.py
from fastapi import BackgroundTasks, HTTPException
from app.business.multiagents.multiagents import organize_extracted_text
from app.services.document_intelligence_service import PDFExtractor
import easyocr  # Importamos EasyOCR
import numpy as np
from PIL import Image
from io import BytesIO
import pytesseract

class ExtractTextFromPDF:
    def __init__(self, extractor: PDFExtractor):
        self.extractor = extractor

    def execute(self) -> str:
        """Ejecuta la extracción de texto y devuelve el resultado."""
        try:
            return self.extractor.extract_text()
        except ValueError as e:
            raise ValueError(f"Fallo en la extracción de texto: {str(e)}")

# Función para extraer texto de un PDF en segundo plano y luego procesarlo
async def extract_text_from_pdf_background(file_content: bytes, background_tasks: BackgroundTasks):
    pdf_extractor = PDFExtractor(file_stream=file_content)
    use_case = ExtractTextFromPDF(extractor=pdf_extractor)
    try:
        texto_extraido = use_case.execute()
        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Función para extraer texto de una imagen en segundo plano y luego procesarlo
async def extract_text_from_image_background(file_content: bytes, background_tasks: BackgroundTasks, use_easyocr: bool = False):
    try:
        if use_easyocr:
            reader = easyocr.Reader(['es', 'en'])
            imagen = Image.open(BytesIO(file_content)).convert('RGB')
            imagen_np = np.array(imagen)
            result = reader.readtext(imagen_np)
            texto_extraido = "\n".join([res[1] for res in result])
        else:
            imagen = Image.open(BytesIO(file_content))
            texto_ocr = pytesseract.image_to_string(imagen)
            texto_extraido = texto_ocr

        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")             
