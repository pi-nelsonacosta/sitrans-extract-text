# Archivo: app/db/base.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

# Configuración de SQLAlchemy para MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:user_password@mysql:3306/clean_architecture_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base para los modelos de SQLAlchemy
Base = declarative_base()

# Configuración de Motor para MongoDB
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017")
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client.clean_architecture_db
