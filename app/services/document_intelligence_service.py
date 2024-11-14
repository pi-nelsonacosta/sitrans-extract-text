import base64
from datetime import datetime
from fastapi import BackgroundTasks, HTTPException
from app.business.aforo_processing import organize_extracted_text_AFORO
from app.business.document_extract_values.extract_text import extract_text_from_image_background
from app.business.tgr_processing import organize_extracted_text_TGR
from app.db.models.mongo_log_model import ExtractionRequest
from app.db.repository.mongo_log_repository import insert_extraction_request
from app.db.base import mongo_db
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO

async def handle_extract_aforo_text(file_content: bytes):
    """
    Maneja la extracción de texto OCR para documentos TGR en segundo plano.
    """
    try:
    
        await organize_extracted_text_AFORO(file_content)
        return {"status": "El texto OCR está siendo extraído y procesado en segundo plano."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

async def handle_extract_text_tgr(file_content: bytes):
    """
    Maneja la extracción de texto OCR para documentos TGR en segundo plano.
    """
    try:
    
        await organize_extracted_text_TGR(file_content)
        return {"status": "El texto OCR está siendo extraído y procesado en segundo plano."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")


def validate_and_process_file(file_content: bytes) -> list[Image.Image]:
    """
    Valida si el archivo es un PDF o una imagen válida.
    Convierte PDFs a imágenes y devuelve una lista de imágenes.
    """
    try:
        if file_content[:4] == b"%PDF":
            # Convertir PDF a imágenes
            return convert_from_bytes(file_content, dpi=300)
        else:
            # Validar y procesar como imagen
            imagen = Image.open(BytesIO(file_content)).convert("RGB")
            return [imagen]  # Devuelve la imagen envuelta en una lista
    except Exception:
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es un PDF o una imagen válida.")

async def handle_din_extraction(background_tasks: BackgroundTasks, file_content: bytes, filename: str, use_easyocr: bool):
    """
    Maneja la extracción de texto DIN desde un PDF o imagen.
    """
    try:
        # Validar y convertir el archivo
        images = validate_and_process_file(file_content)

        # Insertar documento en MongoDB con estado inicial
        extraction_request = ExtractionRequest(
            filename=filename,
            status="En proceso",
            created_at=datetime.utcnow(),
            din={}  # Inicialmente vacío, se llenará al completar OCR
        )
        inserted_id = await insert_extraction_request(extraction_request)
        print(f"Documento DIN insertado con ID: {inserted_id}")

        # Procesar cada imagen en segundo plano
        for image in images:
            background_tasks.add_task(
                extract_text_from_image_background,
                image,  # Pasar la imagen directamente
                str(inserted_id),  # El ID del documento en MongoDB
                use_easyocr  # Si se utiliza EasyOCR o no
            )

        return {"status": "El texto OCR está siendo extraído con EasyOCR y procesado en segundo plano."}

    except HTTPException as http_ex:
        raise http_ex  # Propagar excepciones específicas
    except Exception as e:
        print(f"Error inesperado en handle_din_extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

