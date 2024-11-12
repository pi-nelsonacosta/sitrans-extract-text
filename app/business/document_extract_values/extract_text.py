# business/use_cases/extract_text.py
from fastapi import BackgroundTasks, HTTPException
from app.business.multiagents.multiagents import organize_extracted_text
from app.business.pdf_extractor import PDFExtractor
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

""" # Función para extraer texto de un PDF en segundo plano y luego procesarlo
async def extract_text_from_pdf_background(file_content: bytes, background_tasks: BackgroundTasks):
    pdf_extractor = PDFExtractor(file_stream=file_content)
    use_case = ExtractTextFromPDF(extractor=pdf_extractor)
    try:
        texto_extraido = use_case.execute()
        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) """

async def extract_text_from_image_background(file_content: bytes, document_id: str, use_easyocr: bool):
    """
    Procesa la imagen con OCR y llama a la función de procesamiento del texto extraído.
    """
    try:
        if use_easyocr:
            # Procesar la imagen con EasyOCR
            reader = easyocr.Reader(['es', 'en'])
            imagen = Image.open(BytesIO(file_content)).convert('RGB')
            imagen_np = np.array(imagen)
            result = reader.readtext(imagen_np)
            texto_extraido = "\n".join([res[1] for res in result])
            ocr_engine = "EASY-OCR"
        else:
            # Procesar la imagen con PyTesseract
            imagen = Image.open(BytesIO(file_content))
            texto_ocr = pytesseract.image_to_string(imagen)
            texto_extraido = texto_ocr
            ocr_engine = "PyTesseract"

        # Llamar a la función para organizar el texto extraído
        await organize_extracted_text(texto_extraido, document_id, ocr_engine)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

   


            
