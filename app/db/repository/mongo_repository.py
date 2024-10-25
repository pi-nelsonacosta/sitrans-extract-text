import motor.motor_asyncio
from bson import ObjectId
from app.db.models.mongo_model import MongoModel
from pymongo import MongoClient

MONGO_URI = "mongodb://mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
client_sync = sync_client = MongoClient(MONGO_URI) 
db = client.clean_architecture_db
db_sync = client_sync.clean_architecture_db

async def get_mongo_record(record_id: str):
    if not ObjectId.is_valid(record_id):
        raise ValueError(f"'{record_id}' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string")
    
    record = await db["mongo_collection"].find_one({"_id": ObjectId(record_id)})

    if record:
        # Convertir el `_id` de ObjectId a string para que sea serializable
        record["id"] = str(record["_id"])
        del record["_id"]
    
    return record

async def get_all_mongo_records():
    cursor = db["mongo_collection"].find({})
    records = []
    async for document in cursor:
        # Convertir `_id` de ObjectId a string para que sea serializable
        document["id"] = str(document["_id"])
        del document["_id"]
        records.append(document)
    return records

async def create_mongo_record(data):
    # Insertar directamente ya que `data` es un diccionario
    record = await db["mongo_collection"].insert_one(data)
    # Convertir el ObjectId del registro creado a string para devolverlo
    return str(record.inserted_id)

def create_mongo_record_sync(data):
    # Insertar el registro en la colección de MongoDB usando el cliente sincrónico
    record = db_sync["mongo_collection"].insert_one(data)
    # Convertir el ObjectId del registro creado a string para devolverlo
    return str(record.inserted_id)

async def update_mongo_record(record_id: str, data: dict):
    try:
        await db["mongo_collection"].update_one({"_id": ObjectId(record_id)}, {"$set": data})
        return await get_mongo_record(record_id)
    except Exception as e:
        raise ValueError(f"Invalid ObjectId: {e}")

async def delete_mongo_record(record_id: str):
    try:
        result = await db["mongo_collection"].delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count
    except Exception as e:
        raise ValueError(f"Invalid ObjectId: {e}")

async def delete_all_mongo_records():
    try:
        result = await db["mongo_collection"].delete_many({})
        return result.deleted_count
    except Exception as e:
        raise ValueError(f"Error deleting records: {e}")    