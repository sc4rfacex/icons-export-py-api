import requests
import os
from app.services.methods import track_file_nodes
# from app.helpers.helpers import format_icon


# FIGMA_API_KEY = os.getenv("FIGMA_API_KEY")

# def export_icons():
#     headers = {"Authorization": f"Bearer {FIGMA_API_KEY}"}
#     try:
#         response = requests.get("https://api.figma.com/v1/icons/export", headers=headers)

#         if response.status_code == 200:
#             icons_data = response.json()
#             for icon in icons_data.get("icons", []):
#                 with open(f"/path/to/save/{icon['name']}.svg", 'w') as svg_file:
#                     svg_file.write(icon['svg'])
#             return True
#         return False
#     except Exception as e:
#         print(f"Error exporting icons: {str(e)}")
#         return False
      
      
def dls_update_components(file_key="file_key"):
    """ Archiva los componentes de un archivo Figma en el catálogo DLS """
    res = {
        'error': None,
        'meta': { 'length': 0 },
        'data': None
    }

    try:
        print("export_service.py before track_file_nodes")
        track_file_nodes(file_key)
    except Exception as ex:
        print(ex)
        res['error'] = ex

    return res