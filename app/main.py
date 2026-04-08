from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import *
from app.routes import teacher_routes
from app.routes import course_routes
from app.routes import class_section_routes
from app.routes import class_session_routes
from app.routes import student_routes
from app.routes import face_routes
from app.routes import recognition_routes
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(teacher_routes.router)
app.include_router(course_routes.router)
app.include_router(class_section_routes.router)
app.include_router(class_session_routes.router)
app.include_router(student_routes.router)
app.include_router(face_routes.router)
app.include_router(recognition_routes.router)

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