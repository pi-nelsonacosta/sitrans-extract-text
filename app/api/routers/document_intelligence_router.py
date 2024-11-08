from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response
from app.business.document_extract_values.extract_text import extract_text_from_image_background, extract_text_from_pdf_background
from app.db.init_db import get_db

router = APIRouter()

db = get_db()

@router.post("/extract-text/")
async def extract_text_from_pdf(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_pdf_background, file_content, background_tasks)
        return Response(content='{"status": "El texto está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")   

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-ocr/")
async def extract_text_from_image( background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_image_background, file_content, background_tasks, False)
        return Response(content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con EasyOCR
@router.post("/extract-ocr-easy/")
async def extract_text_with_easyocr(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_image_background, file_content, background_tasks, True)
        return Response(content='{"status": "El texto OCR está siendo extraído con EasyOCR y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")





