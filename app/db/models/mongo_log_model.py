from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Modelo para "bultos"
class Bulto(BaseModel):
    numero_bulto: str
    tipo_bulto: Optional[str] = None
    cant_tipo_bulto: Optional[str] = None


# Modelo principal
class ExtractionRequest(BaseModel):
    filename: str = Field(max_length=255)  # Campo obligatorio con validación de longitud
    status: str = Field(default="Pending", max_length=50)  # Campo con valor por defecto y validación de longitud
    extracted_text: Optional[str] = None  # Campo opcional
    error_message: Optional[str] = None  # Campo opcional
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Campo con valor generado dinámicamente
    completed_at: Optional[datetime] = None  # Campo opcional
    din: dict  # Campo obligatorio para almacenar el JSON
