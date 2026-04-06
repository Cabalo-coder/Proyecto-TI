from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import *
from app.routes import teacher_routes
from app.routes import course_routes
from app.routes import class_section_routes
from app.routes import class_session_routes

app = FastAPI()

app.include_router(teacher_routes.router)
app.include_router(course_routes.router)
app.include_router(class_section_routes.router)
app.include_router(class_session_routes.router)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Probar conexión
@app.get("/")
def test_connection():
    try:
        conn = engine.connect()
        return {"message": "Conectado a la base de datos"}
    except:
        return {"message": "Error de conexión"}