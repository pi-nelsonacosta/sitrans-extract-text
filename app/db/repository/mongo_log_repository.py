from app.db.models.mongo_log_model import ExtractionRequest
from app.db.base import mongo_db


async def insert_extraction_request(data: ExtractionRequest):
    """
    Inserta un documento en la colección `extraction_requests`.
    """
    collection = mongo_db["extraction_requests"]  # Acceso a la colección
    document = data.dict(by_alias=True)  # Convierte el modelo Pydantic a un diccionario
    result = await collection.insert_one(document)  # Inserta el documento
    return str(result.inserted_id)


async def get_all_extraction_requests():
    """
    Recupera todos los documentos de la colección `extraction_requests` en MongoDB.
    """
    collection = mongo_db["extraction_requests"]
    records = await collection.find().to_list(length=100)  # Traer hasta 100 registros
    return records

async def delete_all_extraction_requests():
    """
    Elimina todos los documentos de la colección `extraction_requests` en MongoDB.
    """
    collection = mongo_db["extraction_requests"]
    result = await collection.delete_many({})  # Eliminar todos los documentos
    return {"deleted_count": result.deleted_count}  # Devuelve el número de documentos eliminados
