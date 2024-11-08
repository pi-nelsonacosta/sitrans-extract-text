from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# **Configuración de SQLAlchemy para MySQL**
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:user_password@mysql:3306/clean_architecture_db")
mysql_engine = create_engine(DATABASE_URL)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

# **Configuración de SQLAlchemy para SQL Server**
SQLSERVER_URL = os.getenv("SQLSERVER_URL", "mssql+pymssql://sa:Development123!@sqlserver:1433/tempdb")
sqlserver_engine = create_engine(SQLSERVER_URL)
SQLServerSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlserver_engine)

# **Definir Base para los modelos de SQLAlchemy**
Base = declarative_base()

# **Configuración de Motor para MongoDB**
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017")
mongo_client = AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client["clean_architecture_db"]  # Base de datos MongoDB

# Mensajes para depuración
print(f"MySQL Engine: {mysql_engine}")
print(f"SQL Server Engine: {sqlserver_engine}")
print(f"MongoDB Client: {mongo_client}")
