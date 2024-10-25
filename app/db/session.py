from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base  # Asegúrate de importar el Base correcto
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:user_password@mysql:3306/clean_architecture_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

