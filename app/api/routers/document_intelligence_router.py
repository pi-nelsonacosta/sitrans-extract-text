from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, Query, UploadFile, File, Form
from enum import Enum
from app.services.document_intelligence_service import organize_extracted_text_AFORO 
from app.services.document_intelligence_service import organize_extracted_text_DIN
from app.services.document_intelligence_service import organize_extracted_text_TGR
from app.services.document_intelligence_service import process_file_input
from typing import List

router = APIRouter()

# Definir una enumeración para los tipos de archivo permitidos
class FileType(str, Enum):
    AFORO = "AFORO"
    TGR = "TGR"
    DIN = "DIN"

# Ruta para manejar la subida de imágenes o la descarga desde una URL
@router.post("/extract-text-sitrans/")
async def extract_text_sitrans(
    background_tasks: BackgroundTasks,
    file_type: FileType = Form(..., description="Tipo de archivo"),  # Tipo de archivo requerido como Enum
    url: str = Form(None, description="URL directa del archivo PDF o imagen (opcional)"),  # URL opcional
    uploaded_file: UploadFile = File(None, description="Archivo PDF o imagen (opcional)"),  # Archivo opcional
):
    """
    Procesa un archivo PDF o imagen descargado desde una URL o subido directamente para extraer texto.
    """
    try:
        # Obtener el contenido del archivo desde la URL o subido
        file_content = await process_file_input(url, uploaded_file)
        
        # Procesar el archivo dependiendo del tipo
        if file_type == FileType.AFORO:
            response = await organize_extracted_text_AFORO(file_content)
            return response
        elif file_type == FileType.TGR:
            response = await organize_extracted_text_TGR(file_content)
            return response
        elif file_type == FileType.DIN:
           response = await organize_extracted_text_DIN(file_content)
           return response
        else:
            raise HTTPException(status_code=400, detail="Tipo de archivo no soportado.")
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud para {file_type}: {str(e)}"
        )
