# business/use_cases/extract_text.py
from fastapi import BackgroundTasks, HTTPException
from app.business.pdf_extractor import PDFExtractor
import easyocr  # Importamos EasyOCR
import numpy as np
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string
from PIL import Image, UnidentifiedImageError

class ExtractTextFromPDF:
    def __init__(self, extractor: PDFExtractor):
        self.extractor = extractor

    def execute(self) -> str:
        """Ejecuta la extracción de texto y devuelve el resultado."""
        try:
            return self.extractor.extract_text()
        except ValueError as e:
            raise ValueError(f"Fallo en la extracción de texto: {str(e)}")

def validate_image_format(file_content):
    try:
        # Intentar abrir como imagen para verificar el formato
        imagen = Image.open(BytesIO(file_content))
        imagen.verify()  # Verifica si es una imagen válida
        return True
    except UnidentifiedImageError:
        return False
    except Exception:
        return False        

async def extract_text_from_image_background(file_content, document_id: str, use_easyocr: bool):
    """
    Procesa la imagen con OCR y organiza el texto extraído.
    """
    try:
        if isinstance(file_content, Image.Image):
            imagen = file_content  # Si ya es una imagen, úsala directamente
        else:
            raise TypeError("file_content debe ser de tipo PIL.Image.Image.")

        if use_easyocr:
            reader = easyocr.Reader(['es', 'en'])
            imagen_np = np.array(imagen)
            result = reader.readtext(imagen_np)
            texto_extraido = "\n".join([res[1] for res in result])
            ocr_engine = "EASY-OCR"
        else:
            texto_extraido = image_to_string(imagen, lang="eng+spa")
            ocr_engine = "PyTesseract"

        await organize_extracted_text(texto_extraido, document_id, ocr_engine)

    except Exception as e:
        # Registrar el error y no interrumpir el flujo de la tarea
        print(f"Error al procesar la imagen en segundo plano: {str(e)}")

""" # Función para extraer texto de un PDF en segundo plano y luego procesarlo
async def extract_text_from_pdf_background(file_content: bytes, background_tasks: BackgroundTasks):
    pdf_extractor = PDFExtractor(file_stream=file_content)
    use_case = ExtractTextFromPDF(extractor=pdf_extractor)
    try:
        texto_extraido = use_case.execute()
        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) """

   


            
