# Archivo: app/db/init_db.py
from app.db.base import Base, engine  # Asegúrate de que engine está importado
from app.db.models.extraction_request import ExtractionRequest  # Importa el modelo para que sea reconocido
from app.db.base import SQLServerSessionLocal

def init_db():
    # Esto crea todas las tablas que aún no existen en la base de datos
    Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de SQL Server
def get_db():
    db = SQLServerSessionLocal()
    try:
        yield db
    finally:
        db.close()