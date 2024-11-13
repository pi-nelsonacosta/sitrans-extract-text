from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response
from app.services.document_intelligence_service import fetch_all_records 
from app.services.document_intelligence_service import handle_din_extraction 
from app.services.document_intelligence_service import handle_extract_aforo_text 
from app.services.document_intelligence_service import handle_extract_text_tgr 
from app.services.document_intelligence_service import remove_all_records
import json

router = APIRouter()

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-aforo-text/")
async def extract_text_from_image_aforo(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
):
    """
    Procesa un archivo PDF para extraer texto de aforo mediante OCR.
    """
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg) o un PDF.")

    try:
        file_content = await file.read()
        await handle_extract_aforo_text(background_tasks, file_content)
        return Response(
            content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', 
            media_type="application/json", 
            status_code=202
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
    

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-tgr-text/")
async def extract_text_from_image_tgr( 
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)):
    """
    Procesa una imagen para extraer texto de TGR mediante OCR.
    """
    
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg) o un PDF.")

    try:
        file_content = await file.read()
        await handle_extract_text_tgr(background_tasks, file_content)
        return Response(
            content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', 
            media_type="application/json", 
            status_code=202
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")     
    
# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con EasyOCR
@router.post("/extract-din-text/")
async def extract_din_text(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    use_easyocr: bool = True
):
    """
    Ruta para manejar la subida de imágenes y ejecutar la extracción OCR en segundo plano.
    """
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg) o un PDF.")

    try:
        file_content = await file.read()
        response = await handle_din_extraction(background_tasks, 
                                               file_content, 
                                               file.filename, 
                                               use_easyocr)
        
        return Response(content=json.dumps(response), 
                        media_type="application/json", 
                        status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/mongo/records", response_model=list[dict])
async def get_all_records():
    """
    Recupera los campos `din`, `created_at`, y `completed_at` de MongoDB.
    """
    try:
        records = await fetch_all_records()

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
        result = await remove_all_records()
        return {"status": "success", "deleted_count": result["deleted_count"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al borrar los registros: {str(e)}")   
