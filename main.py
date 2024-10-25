# Archivo: main.py
from fastapi import FastAPI
from app.api.routers import document_intelligence_router

app = FastAPI()

# Registrar el router de /send-log/
app.include_router(document_intelligence_router.router, prefix="/api", tags=["API Sitrans"])

# Para correr la aplicación
# uvicorn main:app --reload
