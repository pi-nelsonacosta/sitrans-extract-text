from app.db.base import Base, mysql_engine, SQLServerSessionLocal

def init_mysql_db():
    """
    Inicializa las tablas en la base de datos MySQL.
    Crea todas las tablas que aún no existen.
    """
    Base.metadata.create_all(bind=mysql_engine)

def get_db():
    """
    Dependencia para obtener la sesión de SQL Server.
    Maneja el cierre automático de la sesión al finalizar.
    """
    db = SQLServerSessionLocal()
    try:
        yield db
    finally:
        db.close()
