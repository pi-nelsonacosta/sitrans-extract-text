from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File, HTTPException, Response
from requests import Session
from app.business.document_extract_values.extract_text import extract_text_from_aforo, extract_text_from_image_background, extract_text_from_pdf_background, extract_text_from_tgr
from app.db.init_db import get_db
from app.db.models.mongo_log_model import ExtractionRequest
from app.db.repository.mongo_log_repository import delete_all_extraction_requests, get_all_extraction_requests, insert_extraction_request

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

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-aforo-text/")
async def extract_text_from_image_aforo( background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_aforo, file_content)
        return Response(content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")    

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-tgr-text/")
async def extract_text_from_image_tgr( background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_tgr, file_content)
        return Response(content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")    
    

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con EasyOCR
@router.post("/extract-ocr-easy/")
async def extract_text_with_easyocr(background_tasks: BackgroundTasks, file: UploadFile = File(...), use_easyocr: bool = True):
    """
    Ruta para manejar la subida de imágenes y ejecutar la extracción OCR en segundo plano.
    """
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()

        # Insertar documento en MongoDB con estado inicial
        extraction_request = ExtractionRequest(
            filename=file.filename,
            status="En proceso",
            created_at=datetime.utcnow(),
            din={}  # Inicialmente vacío, puedes llenarlo cuando el OCR termine
        )
        inserted_id = await insert_extraction_request(extraction_request)
        print(f"Documento insertado con ID: {inserted_id}")

        # Agregar tarea en segundo plano para procesar OCR
        background_tasks.add_task(
            extract_text_from_image_background,
            file_content,  # El contenido del archivo
            str(inserted_id),  # El ID del documento en MongoDB
            use_easyocr  # Si se utiliza EasyOCR o no
        )

        return Response(
            content='{"status": "El texto OCR está siendo extraído con EasyOCR y procesado en segundo plano."}',
            media_type="application/json",
            status_code=202
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    
@router.get("/mongo/records", response_model=list[dict])
async def get_all_records():
    """
    Recupera los campos `din`, `created_at`, y `completed_at` de MongoDB.
    """
    try:
        records = await get_all_extraction_requests()

        # Incluye los campos requeridos en la respuesta
        return [
            {
                "din": r.get("din"),
                "created_at": r.get("created_at"),
                "completed_at": r.get("completed_at"),
            }
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los registros: {str(e)}")

@router.delete("/mongo/records")
async def delete_all_records():
    """
    Elimina todos los registros de la colección `extraction_requests` en MongoDB.
    """
    try:
        result = await delete_all_extraction_requests()
        return {"status": "success", "deleted_count": result["deleted_count"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al borrar los registros: {str(e)}")    




