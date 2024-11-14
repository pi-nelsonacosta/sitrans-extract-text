from pydantic import BaseModel, Field
from typing import Optional

class AforoSchema(BaseModel):
    solicitud: Optional[str] = Field(default="", description="Solicitud del aforo")
    folioDIN: Optional[str] = Field(default="", description="Folio DIN asociado")
    fechaAceptacion: Optional[str] = Field(default="", description="Fecha de aceptación")
    numeroEncriptado: Optional[str] = Field(default="", description="Número encriptado")
    codigoAgente: Optional[str] = Field(default="", description="Código del agente")
    nombreAgente: Optional[str] = Field(default="", description="Nombre del agente")
    codigoAduanaTramitacion: Optional[str] = Field(default="", description="Código de la aduana de tramitación")
    tipoRevision: Optional[str] = Field(default="", description="Tipo de revisión")
    FirmaAgencia: Optional[str] = Field(default="", description="Firma de la agencia")

    class Config:
        schema_extra = {
            "example": {
                "solicitud": "12345",
                "folioDIN": "DIN20231101",
                "fechaAceptacion": "2024-11-14",
                "numeroEncriptado": "encrypted12345",
                "codigoAgente": "AG1234",
                "nombreAgente": "Agente Pérez",
                "codigoAduanaTramitacion": "ADU5678",
                "tipoRevision": "Completa",
                "FirmaAgencia": "firmaDigital"
            }
        }
