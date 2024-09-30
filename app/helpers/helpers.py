

###############################################################################
################# Los "helpers" son funciones ajenas a la lógica principal
###############################################################################

import os
import requests
import re

# --------------- Remueve or reemplaza los caracteres no válidos en la ruta

def sanitize_folder_path(raw_path):
    return re.sub(r'[^a-zA-Z]+', '', raw_path)

def sanitize_file_path(raw_path):
    invalid_chars = r'[<>:"/\.\\|?*]'
    return re.sub(invalid_chars, '-', raw_path).lower()

def sanitize_path_b(raw_path):
    # Reemplazar puntos y espacios por guiones
    sanitized = re.sub(r'[. ]', '-', raw_path)
    # Eliminar caracteres no válidos (dejar solo alfanuméricos, guiones y barras)
    sanitized = re.sub(r'[^\w/-]', '', sanitized)
    # Eliminar cualquier guion al inicio de la cadena
    sanitized = sanitized.lstrip('-')
    return sanitized

# --------------- Valida o crea las carpetas en órden obtenidas en un arreglo

def check_and_create_folders(path_parts: list):
    current_path = os.getcwd()
    for part in path_parts:
        current_path = os.path.join(current_path, part)
        if not os.path.splitext(current_path)[1]:
            if not os.path.exists(current_path):
                os.makedirs(current_path)
    return current_path

# Descarga de una URL externa un archivo y lo almacena de forma local

def store_file(source_url: str, local_file_path: str):
    response = requests.get(source_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(source_url)

# --------------- Divide la lista en bloques de tamaño dado

def chunkify(raw_list, chunk_size):
    for i in range(0, len(raw_list), chunk_size):
        yield raw_list[i:i + chunk_size]
        
# --------------------------------------------------- REQUEST HELPER FUNCTIONS
def get_headers(scope: str = 'reg') -> dict:
    """Genera los headers de la solicitud con base en el ámbito especificado."""
    ORG_API_KEY = os.getenv("ORG_API_KEY")
    REG_API_KEY = os.getenv("REG_API_KEY")
    api_key = REG_API_KEY if scope == 'reg' else ORG_API_KEY
    return {"Authorization": f"Bearer {api_key}"}

def log_request_info(endpoint: str, status: int, response_data: dict):
    """Registra la información de las solicitudes."""
    print(f"Request to {endpoint} returned status {status}. Response: {response_data}")