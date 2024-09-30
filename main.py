from fastapi import FastAPI
from app.api import icons_export

app = FastAPI()

# Incluir los endpoints del módulo de exportación
app.include_router(icons_export.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Icon Export API"}