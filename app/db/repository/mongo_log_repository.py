from app.db.models.mongo_log_model import ExtractionRequest
from app.db.base import mongo_db


async def insert_extraction_request(data: ExtractionRequest):
    collection = mongo_db["extraction_requests"]  # Colección específica
    result = await collection.insert_one(collection)
    return str(result.inserted_id)

async def get_all_extraction_requests():
    collection = mongo_db["extraction_requests"]  # Colección específica
    cursor = collection.find({})
    records = []
    async for document in cursor:
        # Convertir `_id` de ObjectId a string para que sea serializable
        document["id"] = str(document["_id"])
        del document["_id"]
        records.append(document)
    return records