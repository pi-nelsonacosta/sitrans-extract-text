from datetime import datetime
from fastapi import BackgroundTasks, HTTPException
import pdfplumber
from app.business.aforo_processing import extract_text_from_aforo
from app.business.document_extract_values.extract_text import extract_text_from_image_background
from app.business.tgr_processing import extract_text_from_tgr
from app.business.pdf_extractor import PDFExtractor
from app.db.models.mongo_log_model import ExtractionRequest
from app.db.repository.mongo_log_repository import insert_extraction_request
import fitz  # PyMuPDF
import pytesseract
import io
from app.db.base import mongo_db
from pdf2image import convert_from_bytes
from PIL import Image, UnidentifiedImageError
from io import BytesIO

class PDFOCRExtractor:
    def __init__(self, file_stream):
        """Inicializa el extractor con un archivo PDF en memoria."""
        self.file_stream = file_stream

    def extract_text_with_ocr(self) -> str:
        """Extrae texto de las imágenes contenidas en las páginas del PDF usando OCR."""
        try:
            documento = fitz.open(stream=self.file_stream, filetype="pdf")
        except Exception as e:
            raise ValueError(f"Error al abrir el archivo PDF: {str(e)}")

        textos = []
        for num_pagina in range(documento.page_count):
            pagina = documento.load_page(num_pagina)  # Cargar la página
            imagenes = pagina.get_images(full=True)  # Obtener todas las imágenes de la página

            if not imagenes:
                # Si no hay imágenes, continuar con la siguiente página
                continue

            for img_index, img in enumerate(imagenes):
                xref = img[0]  # Referencia a la imagen en el PDF
                base_image = documento.extract_image(xref)  # Extraer la imagen
                image_bytes = base_image["image"]  # Obtener los bytes de la imagen
                image_ext = base_image["ext"]  # Obtener la extensión del archivo de imagen

                # Cargar la imagen con PIL
                imagen = Image.open(io.BytesIO(image_bytes))

                # Aplicar OCR a la imagen extraída
                texto_ocr = pytesseract.image_to_string(imagen)
                textos.append(f"--- OCR Imagen {img_index + 1} en la página {num_pagina + 1} ---\n{texto_ocr}")

        documento.close()  # Cerrar el PDF al finalizar
        return "\n".join(textos)

async def fetch_all_records():
    """
    Recupera todos los registros de la colección `extraction_requests`.
    """
    try:
        collection = mongo_db["extraction_requests"]
        records = await collection.find({}, {"din": 1, "created_at": 1, "completed_at": 1}).to_list(length=None)
        return records
    except Exception as e:
        raise Exception(f"Error al recuperar registros: {str(e)}")


async def remove_all_records():
    """
    Elimina todos los registros de la colección `extraction_requests`.
    """
    try:
        collection = mongo_db["extraction_requests"]
        result = await collection.delete_many({})
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        raise Exception(f"Error al eliminar registros: {str(e)}")

async def handle_extract_aforo_text(background_tasks: BackgroundTasks, file_content: bytes):
    """
    Maneja la extracción de texto OCR para aforo en segundo plano, procesando PDFs e imágenes.
    """
    try:
        if not file_content:
            raise HTTPException(status_code=400, detail="El contenido del archivo está vacío.")

        # Intenta verificar si el archivo es un PDF con texto seleccionable
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:  # Si el texto seleccionable está presente
                        full_text += text + "\n"

                # Si se encontró texto seleccionable, procesa directamente
                if full_text.strip():
                    print("Texto seleccionable encontrado en el PDF.")
                    return {"status": "success", "text": full_text}

        except Exception:
            print("El archivo no es un PDF seleccionable. Se procederá con OCR.")

        # Si no es seleccionable, convertir PDF a imágenes
        images = convert_from_bytes(file_content, dpi=300)

        # Agregar cada imagen como tarea en segundo plano para el procesamiento
        for image in images:
            background_tasks.add_task(extract_text_from_aforo, image)

        return {"status": "El texto OCR está siendo extraído y procesado en segundo plano."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

async def handle_extract_text_tgr(background_tasks: BackgroundTasks, file_content: bytes):
    """
    Maneja la extracción de texto OCR para documentos TGR en segundo plano.
    """
    try:
        if not file_content:
            raise HTTPException(status_code=400, detail="El contenido del archivo está vacío.")

        # Intenta verificar si el archivo es un PDF con texto seleccionable
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:  # Si el texto seleccionable está presente
                        full_text += text + "\n"

                # Si se encontró texto seleccionable, procesa directamente
                if full_text.strip():
                    print("Texto seleccionable encontrado en el PDF.")
                    return {"status": "success", "text": full_text}

        except Exception:
            print("El archivo no es un PDF seleccionable. Se procederá con OCR.")

        # Si no es seleccionable, convertir PDF a imágenes
        images = convert_from_bytes(file_content, dpi=300)

        # Agregar cada imagen como tarea en segundo plano para el procesamiento
        for image in images:
            background_tasks.add_task(extract_text_from_tgr, image)

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