import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

LLM_CONFIG = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": [
        {
            'api_key': os.getenv("OPENAI_API_KEY"),  # Clave de API desde el entorno
            'azure_endpoint': os.getenv("AZURE_OPENAI_ENDPOINT"),  # Endpoint de Azure OpenAI
            'api_type': "azure",  # Tipo de API (Azure)
            'api_version': "2023-03-15-preview",  # Versión de la API
            'model': os.getenv("MODEL")  # Nombre del despliegue
        }
    ],
    "timeout": 120  # Tiempo de espera
}
