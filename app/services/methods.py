###############################################################################
################# Los "métodos" son funciones que procesan la lógica de negocio
###############################################################################

import concurrent.futures

from app.services.services import fetch_file_nodes, fetch_file_images
from app.helpers.helpers import (
    chunkify,
    sanitize_folder_path,
    sanitize_file_path,
    check_and_create_folders,
    store_file
)

# --------------- Formatea los componentes con los parámetros necesarios

def flat_tree(page_name, node, depth, acc) -> list:

    children = node.pop('children') if 'children' in node else []
    node_id = node.get('id')

    if node.get('type') in ('COMPONENT', 'INSTANCE'):
        acc.append({
            'node_id': node_id,
            'page_name': page_name,
            'depth': depth,
            'name': node.get('name'),
            'type': node.get('type'),
            'reference_id': node.get('componentId')
        })

    if len(children):
        depth += 1

        if node.get('type') == "CANVAS":
            page_name = node.get('name')

        for child in children:
            flat_tree(page_name, child, depth, acc)

    return acc

# --------------- Descarga un archivo de Figma y lo almacena de forma local

def download_files(file_key: str, chunk: list, format: str):
    
    node_ids = [node['node_id'] for node in chunk]
    node_ids_str = ','.join(map(str, node_ids))
    
    params = f"format={format}&ids={node_ids_str}"
    result = fetch_file_images(file_key, params)
    if result == None: return

    images_dict = result['images']
    images_list = list(images_dict.values())

    for idx, node in enumerate(chunk):

        page_name = sanitize_folder_path(node['page_name'])
        file_name = sanitize_file_path(node['name'])
        path_parts = ["Pages", page_name, f"{file_name}.{format}"]
        local_file_path = check_and_create_folders(path_parts)

        store_file(images_list[idx], local_file_path)

# --------------- Obtiene el arbol del archivo y devuelve los datos formateados
def track_file_nodes(file_key: str):

    print("methods.py before fetch_file_nodes")
    result = fetch_file_nodes(file_key)
    if result == None: return []

    document = result['document']
    flatted_tree = flat_tree(None, document, 0, [])
    chunks = list(chunkify(flatted_tree, 250))

    download_files(file_key, list(chunks[0]), "svg")

    # if len(chunks):
    #     executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
    #     try:
    #         futures = [executor.submit(download_files, *(file_key, list(chunk), "svg")) for chunk in chunks]
    #         for thread in concurrent.futures.as_completed(futures):
    #             future = thread.result()
    #     except Exception as e:
    #         print(e)
    #     finally: executor.shutdown(wait=True)
