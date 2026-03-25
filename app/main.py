from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import *

app = FastAPI()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Probar conexión
@app.get("/")
def test_connection():
    try:
        conn = engine.connect()
        return {"message": "✅ Conectado a la base de datos"}
    except:
        return {"message": "❌ Error de conexión"}