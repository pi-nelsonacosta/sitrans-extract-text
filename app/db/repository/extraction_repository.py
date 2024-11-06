from sqlalchemy.orm import Session
from app.db.models.extraction_request import ExtractionRequest
from datetime import datetime

# Obtener todos los registros
def get_all_extraction_requests(db: Session):
    return db.query(ExtractionRequest).all()

# Obtener un registro específico por ID
def get_extraction_request(db: Session, request_id: int):
    return db.query(ExtractionRequest).filter(ExtractionRequest.id == request_id).first()

# Crear un nuevo registro
def create_extraction_request(db: Session, filename: str):
    db_request = ExtractionRequest(filename=filename, status="en proceso", created_at=datetime.utcnow())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

# Actualizar el estado de un registro
def update_extraction_request_status(db: Session, request_id: int, status: str, extracted_text: str = None, error_message: str = None):
    db_request = db.query(ExtractionRequest).filter(ExtractionRequest.id == request_id).first()
    if db_request:
        db_request.status = status
        db_request.extracted_text = extracted_text
        db_request.error_message = error_message
        if status == "completado":
            db_request.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(db_request)
    return db_request

# Eliminar un registro específico
def delete_extraction_request(db: Session, request_id: int):
    db_request = db.query(ExtractionRequest).filter(ExtractionRequest.id == request_id).first()
    if db_request:
        db.delete(db_request)
        db.commit()
    return db_request

# Eliminar todos los registros
def delete_all_extraction_requests(db: Session):
    try:
        db.query(ExtractionRequest).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error deleting records: {e}")