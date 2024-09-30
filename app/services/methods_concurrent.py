###############################################################################
################# Los "métodos" son funciones que procesan la lógica de negocio
###############################################################################

import concurrent.futures

from app.services.services import fetch_file_nodes, fetch_file_images
from app.helpers.helpers import sanitize_path, check_and_create_folders, store_file

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

def download_file(file_key: str, node: dict, format: str):
    
    node_id = node.get('node_id')
    params = f"format={format}&ids={node_id}"
    result = fetch_file_images(file_key, params)
    if result == None: return

    page_name = sanitize_path(node['page_name'])
    file_name = sanitize_path(f"{node['name']}.{format}")
    path_parts = ["Pages", page_name, file_name]
    local_file_path = check_and_create_folders(path_parts)

    store_file(result['images'][node_id], local_file_path)

# --------------- Obtiene el arbol del archivo y devuelve los datos formateados

def track_file_nodes(file_key: str):

    result = fetch_file_nodes(file_key)
    if result == None: return []

    document = result['document']
    flatted_tree = flat_tree(None, document, 0, [])

    node_ids = [node['node_id'] for node in flatted_tree]
    node_ids_str = ','.join(map(str, node_ids))
    
    params = f"format={format}&ids={node_ids_str}"
    result = fetch_file_images(file_key, params)
    if result == None: return

    images_dict = list(result['images'].values())

    for idx, node in enumerate(flatted_tree):

        page_name = sanitize_path(node['page_name'])
        file_name = sanitize_path(f"{node['name']}.{format}")
        path_parts = ["Pages", page_name, file_name]
        local_file_path = check_and_create_folders(path_parts)

        store_file(images_dict[idx], local_file_path)


    # if len(flatted_tree):
    #     executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    #     try:
    #         futures = [executor.submit(download_file, *(file_key, node, "svg")) for node in flatted_tree]
    #         for thread in concurrent.futures.as_completed(futures):
    #             team = thread.result()
    #     except Exception as e:
    #         print(e)
    #     finally: executor.shutdown(wait=True)

    # return flatted_tree
