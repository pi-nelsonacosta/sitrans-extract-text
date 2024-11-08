from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File, HTTPException, Response
from requests import Session
from app.business.document_extract_values.extract_text import extract_text_from_image_background, extract_text_from_pdf_background
from app.db.init_db import get_db
from app.db.models.mongo_log_model import ExtractionRequest
from app.db.repository.mongo_log_repository import get_all_extraction_requests, insert_extraction_request

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
        #insert_extraction_request(ExtractionRequest(filename='Testing', status="En proceso", created_at=datetime.utcnow()))
        return Response(content='{"status": "El texto OCR está siendo extraído con EasyOCR y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")

@router.get("/mongo/records", response_model=list[dict])
def get_all_records(db: Session = Depends(get_db)):
    try:
        records = get_all_extraction_requests(db)
        # Convertir los objetos SQLAlchemy a un formato JSON-serializable
        return [{"id": r.id, "name": r.name, "description": r.description} for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los registros: {str(e)}")




