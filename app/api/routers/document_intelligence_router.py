from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response
from app.services.document_intelligence_service import fetch_all_records 
from app.services.document_intelligence_service import handle_din_extraction 
from app.services.document_intelligence_service import handle_extract_aforo_text 
from app.services.document_intelligence_service import handle_extract_text_tgr 
from app.services.document_intelligence_service import remove_all_records
import json

router = APIRouter()

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-text-sitrans/")
async def extract_text_sitrans(
    background_tasks: BackgroundTasks, 
    file: UploadFile,
    file_type: str
):
    """
    Procesa un archivo PDF para extraer texto de aforo mediante OCR.
    """
    if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg) o un PDF.")

    try:
        file_content = await file.read()
        if file_type == "AFORO":
            await handle_extract_aforo_text(background_tasks, file_content)
        elif file_type == "TGR":
            await handle_extract_text_tgr(background_tasks, file_content)
        elif file_type == "DIN":
            await handle_din_extraction(background_tasks, 
                                               file_content, 
                                               file.filename, 
                                               True)
        else:
            raise HTTPException(status_code=400, detail="Tipo de archivo no soportado.")

        return Response(
            content=f'{{"status": "El texto OCR de tipo {file_type} está siendo extraído y procesado en segundo plano."}}', 
            media_type="application/json", 
            status_code=202
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud para {file_type}: {str(e)}")
   
