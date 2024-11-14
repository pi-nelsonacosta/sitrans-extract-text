from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response, Query
from app.services.document_intelligence_service import handle_din_extraction 
from app.services.document_intelligence_service import handle_extract_aforo_text 
from app.services.document_intelligence_service import handle_extract_text_tgr 
import json
import httpx
from typing import Optional
from enum import Enum

router = APIRouter()

# Definir los tipos de archivo como un Enum
class FileType(str, Enum):
    AFORO = "AFORO"
    TGR = "TGR"
    DIN = "DIN"

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-text-sitrans/")
async def extract_text_sitrans(
    background_tasks: BackgroundTasks,
    url: str = Query(..., description="URL directa del archivo PDF o imagen"),  # URL requerida
    file_type: str = Query(..., description="Tipo de archivo: AFORO, TGR, DIN")  # Tipo de archivo requerido
):
    """
    Procesa un archivo PDF o imagen descargado desde una URL para extraer texto.
    """
    try:
        print(f"Intentando descargar archivo desde URL: {url}")

        async with httpx.AsyncClient(follow_redirects=True) as client:  # Seguir redirecciones
            response = await client.get(url)

            # Manejar errores HTTP
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo descargar el archivo desde la URL."
                )

            # Obtener el contenido descargado
            file_content = response.content

            # Validar si el archivo descargado es un PDF
            if not file_content.startswith(b"%PDF"):
                raise HTTPException(
                    status_code=400,
                    detail="El archivo descargado no es un PDF válido. Verifique la URL."
                )

        # Procesar el archivo dependiendo del tipo
        if file_type == "AFORO":
            await handle_extract_aforo_text()
        elif file_type == "TGR":
            await handle_extract_text_tgr()
        elif file_type == "DIN":
            await handle_din_extraction(
                background_tasks,
                file_content,
                "archivo_descargado.pdf",
                True
            )
        else:
            raise HTTPException(status_code=400, detail="Tipo de archivo no soportado.")

        return Response(
            content=f'{{"status": "El texto OCR de tipo {file_type} está siendo extraído y procesado en segundo plano."}}',
            media_type="application/json",
            status_code=202
        )
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar la solicitud para {file_type}: {str(e)}"
        )