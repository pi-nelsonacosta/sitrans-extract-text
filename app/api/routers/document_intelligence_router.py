from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, Query, UploadFile, File, Form
from enum import Enum
import httpx
from app.services.document_intelligence_service import organize_extracted_text_AFORO
from app.services.document_intelligence_service import organize_extracted_text_DIN
from app.services.document_intelligence_service import organize_extracted_text_TGR

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
        # Verificar si se proporcionó una URL o se cargó un archivo
        if url and uploaded_file:
            raise HTTPException(
                status_code=400,
                detail="No se puede procesar ambos: URL y archivo cargado. Proporcione solo uno."
            )
        elif not url and not uploaded_file:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar una URL o subir un archivo."
            )

        # Obtener el contenido del archivo desde la URL
        if url:
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
        # Obtener el contenido del archivo subido
        elif uploaded_file:
            file_content = await uploaded_file.read()

            # Validar si el archivo subido es un PDF
            if not file_content.startswith(b"%PDF"):
                raise HTTPException(
                    status_code=400,
                    detail="El archivo subido no es un PDF válido."
                )

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
