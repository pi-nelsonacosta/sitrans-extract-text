from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from app.business.use_cases.extract_text import ExtractTextFromPDF
import pytesseract
from io import BytesIO
from app.services.document_intelligence_service import PDFExtractor  # Para PDF exclusivamente
import easyocr  # Importamos EasyOCR
import numpy as np

router = APIRouter()

# Ruta para extraer texto de PDFs
@router.post("/extract-text/")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    # Leer el archivo PDF subido en memoria
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    
    # Crear el servicio extractor para PDFs
    pdf_extractor = PDFExtractor(file_stream=file_content)
    
    # Crear el caso de uso y ejecutarlo
    use_case = ExtractTextFromPDF(extractor=pdf_extractor)
    
    try:
        texto_extraido = use_case.execute()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"texto": texto_extraido}    


# Ruta para extraer texto con OCR desde imágenes (.png, .jpg) usando pytesseract
@router.post("/extract-ocr/")
async def extract_text_from_image(file: UploadFile = File(...)):
    # Verificar si el archivo es una imagen válida
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    # Leer el archivo de imagen subido
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    
    try:
        # Cargar la imagen con PIL
        imagen = Image.open(BytesIO(file_content))

        # Aplicar OCR a la imagen con pytesseract
        texto_ocr = pytesseract.image_to_string(imagen)

        return {"texto_ocr": texto_ocr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")


# Nueva ruta para extraer texto con OCR desde imágenes (.png, .jpg) usando EasyOCR
@router.post("/extract-ocr-easy/")
async def extract_text_with_easyocr(file: UploadFile = File(...)):
    # Verificar si el archivo es una imagen válida
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    # Leer el archivo de imagen subido
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")

    try:
        # Inicializar el lector de EasyOCR
        reader = easyocr.Reader(['es'])  # Cambia 'en' si necesitas otros idiomas

        # Cargar la imagen con PIL
        imagen = Image.open(BytesIO(file_content)).convert('RGB')  # Convertir a RGB
        imagen_np = np.array(imagen)  # Convertir la imagen a un array de numpy para EasyOCR

        # Aplicar OCR con EasyOCR
        result = reader.readtext(imagen_np)

        # Extraer solo el texto del resultado de EasyOCR
        texto_extraido = "\n".join([res[1] for res in result])

        return {"texto_ocr_easy": texto_extraido}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen con EasyOCR: {str(e)}")



