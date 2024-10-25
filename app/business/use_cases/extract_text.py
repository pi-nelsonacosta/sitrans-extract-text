# business/use_cases/extract_text.py
from app.services.document_intelligence_service import PDFExtractor

class ExtractTextFromPDF:
    def __init__(self, extractor: PDFExtractor):
        self.extractor = extractor

    def execute(self) -> str:
        """Ejecuta la extracción de texto y devuelve el resultado."""
        try:
            return self.extractor.extract_text()
        except ValueError as e:
            raise ValueError(f"Fallo en la extracción de texto: {str(e)}")
