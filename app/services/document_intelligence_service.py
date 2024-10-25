import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

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
