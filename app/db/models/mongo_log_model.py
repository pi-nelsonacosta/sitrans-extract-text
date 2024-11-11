from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Modelo para "bultos"
class Bulto(BaseModel):
    numeroBulto: str
    tipoBulto: Optional[str] = None
    cantTipoBulto: Optional[str] = None


# Modelo para el campo "DIN"
class DIN(BaseModel):
    solicitud: Optional[str] = Field(default="")
    numeroDin: Optional[str] = Field(default="")
    fechaDin: Optional[str] = Field(default="")
    aduana: Optional[str] = Field(default="")
    consignatarioOimportador: Optional[str] = Field(default="")
    rutConsignatario: Optional[str] = Field(default="")
    paisOrigen: Optional[str] = Field(default="")
    puertoEmbarque: Optional[str] = Field(default="")
    puertoDesembarque: Optional[str] = Field(default="")
    manifiesto: Optional[str] = Field(default="")
    doctoTransporte: Optional[str] = Field(default="")
    bultos: List[Bulto] = Field(default=[])
    totalBultos: Optional[str] = Field(default="")
    pesoBruto: Optional[str] = Field(default="")
    observacionesBultos: Optional[str] = Field(default="")
    totalEnPesos: Optional[str] = Field(default="")
    tipoInspeccion: Optional[str] = Field(default="")
    resultado: Optional[str] = Field(default="")
    direccionConsignatario: Optional[str] = Field(default="")


# Modelo principal
class ExtractionRequest(BaseModel):
    id: Optional[str] = None  # Incluye el ID de MongoDB como string
    filename: str = Field(max_length=255)
    status: str = Field(default="Pending", max_length=50)
    extracted_text: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    din: DIN