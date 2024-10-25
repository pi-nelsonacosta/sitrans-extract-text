from sqlalchemy.orm import Session
from app.db.models.mysql_model import MySQLModel

def get_all_mysql_records(db: Session):
    return db.query(MySQLModel).all()

def get_mysql_record(db: Session, record_id: int):
    return db.query(MySQLModel).filter(MySQLModel.id == record_id).first()

def create_mysql_record(db: Session, description: str = None):
    db_record = MySQLModel(name='Log', description=description)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_mysql_record(db: Session, record_id: int, name: str = None, description: str = None):
    db_record = db.query(MySQLModel).filter(MySQLModel.id == record_id).first()
    if db_record:
        if name:
            db_record.name = name
        if description:
            db_record.description = description
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_mysql_record(db: Session, record_id: int):
    db_record = db.query(MySQLModel).filter(MySQLModel.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

def delete_all_mysql_records(db: Session):
    try:
        db.query(MySQLModel).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error deleting records: {e}")
