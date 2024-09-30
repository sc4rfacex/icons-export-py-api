###############################################################################
################# Los "api" son intermediarios que consumen servicios externos
###############################################################################

import requests
from dotenv import load_dotenv
import os
from app.helpers.helpers import get_headers, log_request_info

# --------------------------------------------------- API CREDENTIALS
load_dotenv()

ENDPOINT_URL = os.getenv("ENDPOINT_URL")

# --------------------------------------------------- REQUEST FUNCTION
def get_request(endpoint: str, scope: str = 'reg') -> dict:
    """
    Realiza una solicitud GET a un endpoint específico con el ámbito dado.
    
    Args:
        endpoint (str): El endpoint relativo al que se le hará la solicitud.
        scope (str): El ámbito de la solicitud (puede ser 'reg' u 'org').

    Returns:
        dict: Un diccionario con el estatus y los datos de la respuesta.
    """
    headers = get_headers(scope)
    try:
        print("api_figma.py before request.get")
        print(f"{ENDPOINT_URL}/{endpoint}")
        response = requests.get(f"{ENDPOINT_URL}{endpoint}", headers=headers)
        print("after response.get")        
        response.raise_for_status()  # Levanta un error si la respuesta no es 2xx
        print(response)        
        response_data = response.json()
        print("api_figma.py after request.get")
    except requests.exceptions.RequestException as req_error:
        log_request_info(endpoint, response.status_code if response else 500, {})
        return {'status': response.status_code if response else 500, 'data': None, 'error': str(req_error)}
    except ValueError:
        return {'status': 200, 'data': None, 'error': 'Error parsing response JSON'}

    log_request_info(endpoint, response.status_code, response_data)
    return {'status': response.status_code, 'data': response_data}