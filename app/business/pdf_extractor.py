import fitz  # PyMuPDF

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