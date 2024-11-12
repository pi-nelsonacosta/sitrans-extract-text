from datetime import datetime
import json
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response
from requests import Session
from app.business.tgr_processing import extract_text_from_tgr
from app.db.init_db import get_db
from app.db.models.mongo_log_model import ExtractionRequest
from app.services.document_intelligence_service import fetch_all_records, handle_din_extraction, handle_extract_aforo_text, handle_extract_text_tgr, remove_all_records

router = APIRouter()

db = get_db()

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-aforo-text/")
async def extract_text_from_image_aforo(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """
    Procesa una imagen para extraer texto de aforo mediante OCR.
    """
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

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
    
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

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
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        response = await handle_din_extraction(background_tasks, file_content, file.filename, use_easyocr)
        return Response(content=json.dumps(response), media_type="application/json", status_code=202)
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



# Document Intelligence Service

"""
This code sample shows Prebuilt Document operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs
https://learn.microsoft.com/azure/applied-ai-services/form-recognizer/quickstarts/get-started-v3-sdk-rest-api?view=doc-intel-3.1.0&pivots=programming-language-python
"""
"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
""" endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_KEY"

# sample document
formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", formUrl)
result = poller.result()

print("----Key-value pairs found in document----")
for kv_pair in result.key_value_pairs:
    if kv_pair.key and kv_pair.value:
        print("Key '{}': Value: '{}'".format(kv_pair.key.content, kv_pair.value.content))
    else:
        print("Key '{}': Value:".format(kv_pair.key.content))

print("----------------------------------------") """
    




