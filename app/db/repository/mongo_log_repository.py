import json

from fastapi import HTTPException
from app.db.models.mongo_log_model import ExtractionRequest
from app.db.base import mongo_db


async def insert_extraction_request(data: ExtractionRequest):
    """
    Inserta un documento en la colección `extraction_requests`.
    """
    collection = mongo_db["extraction_requests"]  # Acceso a la colección

    # Convierte el modelo Pydantic a un diccionario, excluyendo valores nulos
    document = data.dict(by_alias=True, exclude_none=True)

    # Inserta el documento en la colección
    result = await collection.insert_one(document)

    return str(result.inserted_id)


async def get_all_extraction_requests():
    """
    Recupera los campos `din`, `created_at` y `completed_at` de la colección `extraction_requests` en MongoDB.
    """
    try:
        collection = mongo_db["extraction_requests"]

        # Proyección: Incluye los campos `din`, `created_at`, y `completed_at`, excluye `_id`
        records = await collection.find({}, {"_id": 0, "din": 1, "created_at": 1, "completed_at": 1}).to_list(length=100)

        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los registros: {str(e)}")

async def delete_all_extraction_requests():
    """
    Elimina todos los documentos de la colección `extraction_requests` en MongoDB.
    """
    collection = mongo_db["extraction_requests"]
    result = await collection.delete_many({})  # Eliminar todos los documentos
    return {"deleted_count": result.deleted_count}  # Devuelve el número de documentos eliminados
