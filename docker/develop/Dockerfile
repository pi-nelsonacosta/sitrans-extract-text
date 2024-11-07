# Archivo: docker/develop/Dockerfile
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias, incluyendo ODBC Driver y Tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libmariadb-dev \
    pkg-config \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo el archivo de dependencias y luego instalarlas
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copiar los archivos del proyecto al contenedor
COPY ./app /app/app
COPY ./main.py /app/main.py

# Exponer el puerto para la API de FastAPI
EXPOSE 8000

# Comando para ejecutar la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

