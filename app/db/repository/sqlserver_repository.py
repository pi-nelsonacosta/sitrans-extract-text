from sqlalchemy.orm import Session
from app.db.models.sqlserver_model import SQLServerModel

def get_all_sqlserver_records(db: Session):
    return db.query(SQLServerModel).all()

def get_sqlserver_record(db: Session, record_id: int):
    return db.query(SQLServerModel).filter(SQLServerModel.id == record_id).first()

def create_sqlserver_record(db: Session, description: str = None):
    db_record = SQLServerModel(name='Log', description=description)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_sqlserver_record(db: Session, record_id: int, name: str = None, description: str = None):
    db_record = db.query(SQLServerModel).filter(SQLServerModel.id == record_id).first()
    if db_record:
        if name:
            db_record.name = name
        if description:
            db_record.description = description
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_sqlserver_record(db: Session, record_id: int):
    db_record = db.query(SQLServerModel).filter(SQLServerModel.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

def delete_all_sqlserver_records(db: Session):
    try:
        db.query(SQLServerModel).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error deleting records: {e}")
