from fastapi import APIRouter, HTTPException
from app.services import export_service
from app.services.export_service import dls_update_components
import pdb

router = APIRouter()

@router.get("/export-icons")
def export_icons():
    result = export_service.export_icons()
    if not result:
        raise HTTPException(status_code=500, detail="Error exporting icons")
    return {"message": "Icons exported successfully"}
  
  
@router.post("/update-components")
def update_dls_components(file_key: str = "file_key"):
    """ Actualiza los componentes de DLS con el archivo de Figma especificado """
    print("icons_export.py before dls_update_components")
    result = dls_update_components(file_key)
    if result['error']:
        raise HTTPException(status_code=500, detail=f"Error updating components: {result['error']}")
    return {"message": "Components updated successfully", "meta": result['meta']}