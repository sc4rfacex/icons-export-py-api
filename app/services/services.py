###############################################################################
################# Los "servicios" son intermediarios que consumen las APIs
###############################################################################

from app.api.api_figma import get_request

# ################################################################### FIGMA API

# --------------- Obtiene los componentes de un Figma file

def fetch_file_nodes(file_key: str, params: str = "") -> dict | None:

    result = {}
    query = f"/files/{file_key}?{params}&depth=3"

    print("services.py before get_request")
    response = get_request(query, "reg")
    if response['status'] != 200 or 'error' in response['data']: 
        print(response)
        return

    result = response['data']
    return result

# --------------- Obtiene una imágen de un nodo

def fetch_file_images(file_key: str, params: str) -> dict | None:

    query = f"/images/{file_key}?{params}"
    print(query)

    response = get_request(query, "reg")
    if response['status'] != 200 or 'error' in response['data']:
        print(response)
        return

    result = response['data']
    return result