import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Configuración para Azure OpenAI utilizando las variables del entorno
LLM_CONFIG = {
    "cache_seed": int(os.getenv("CACHE_SEED", 42)),  # Valor por defecto: 42
    "temperature": float(os.getenv("TEMPERATURE", 0)),  # Valor por defecto: 0
    "config_list": [
        {
            'model': os.getenv("MODEL"),
            'api_key': os.getenv("API_KEY"),
            'azure_endpoint': os.getenv("AZURE_ENDPOINT"),
            'api_type': os.getenv("API_TYPE"),
            'api_version': os.getenv("API_VERSION")
        }
    ],
    "timeout": int(os.getenv("TIMEOUT", 120))  # Valor por defecto: 120
}

# Verifica la configuración
print(LLM_CONFIG)
