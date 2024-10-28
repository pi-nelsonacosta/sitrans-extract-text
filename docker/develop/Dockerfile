# Archivo: docker/develop/Dockerfile
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias, incluyendo Tesseract y Leptonica
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libmariadb-dev \
    pkg-config \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos del proyecto al contenedor
COPY ./app /app/app
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Exponer el puerto para la API de FastAPI
EXPOSE 8000

# Comando para ejecutar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

