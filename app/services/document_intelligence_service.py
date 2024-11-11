from fastapi import BackgroundTasks, HTTPException
from app.business.aforo_processing import extract_text_from_aforo
from app.business.tgr_processing import extract_text_from_tgr
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from pymongo import ReturnDocument
from app.db.base import mongo_db
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


class PDFExtractor:
    def __init__(self, file_stream):
        """Inicializa el extractor con un archivo PDF en memoria."""
        self.file_stream = file_stream

    def extract_text(self) -> str:
        """Extrae el texto de todas las páginas del PDF que ya contienen una capa de texto."""
        try:
            documento = fitz.open(stream=self.file_stream, filetype="pdf")
        except Exception as e:
            raise ValueError(f"Error al abrir el archivo PDF: {str(e)}")
        
        textos = []
        for num_pagina in range(documento.page_count):
            pagina = documento.load_page(num_pagina)  # Cargar cada página
            texto = pagina.get_text("text")  # Extraer el texto en formato de texto plano
            textos.append(f"--- Página {num_pagina + 1} ---\n{texto}")
        
        documento.close()  # Cerrar el PDF al final
        return "\n".join(textos)


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
    Maneja la extracción de texto OCR para aforo en segundo plano.
    """
    try:
        # Valida que el contenido no esté vacío
        if not file_content:
            raise HTTPException(status_code=400, detail="El contenido del archivo está vacío.")
        
        # Añade la tarea en segundo plano
        background_tasks.add_task(extract_text_from_aforo, file_content)
    except Exception as e:
        raise Exception(f"Error al procesar el archivo: {str(e)}")

async def handle_extract_aforo_tgr(background_tasks: BackgroundTasks, file_content: bytes):
    """
    Maneja la extracción de texto OCR para aforo en segundo plano.
    """
    try:
        # Valida que el contenido no esté vacío
        if not file_content:
            raise HTTPException(status_code=400, detail="El contenido del archivo está vacío.")
        
        # Añade la tarea en segundo plano
        background_tasks.add_task(extract_text_from_tgr, file_content)
    except Exception as e:
        raise Exception(f"Error al procesar el archivo: {str(e)}")
    


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
