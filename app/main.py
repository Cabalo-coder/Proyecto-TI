# Importa FastAPI para crear la aplicación backend
from fastapi import FastAPI

# Importa middleware CORS para permitir conexiones desde el frontend
from fastapi.middleware.cors import CORSMiddleware

# Importa el motor de base de datos y la clase Base de SQLAlchemy
from app.config.database import engine, Base

# Importa todos los modelos registrados
from app.models import *

# Importa los routers de cada módulo del sistema
from app.routes import teacher_routes
from app.routes import course_routes
from app.routes import class_section_routes
from app.routes import class_session_routes
from app.routes import student_routes
from app.routes import face_routes
from app.routes import recognition_routes
from app.routes import attendance_routes
from app.routes import group_attendance_routes
from app.routes import report_routes
from app.routes import video_attendance

# Importa StaticFiles para manejo de archivos estáticos
from fastapi.staticfiles import StaticFiles


# Crea la instancia principal de la aplicación FastAPI
app = FastAPI()


# Lista de orígenes permitidos para conexión CORS
# Normalmente corresponde al frontend del sistema
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# Configura el middleware CORS
app.add_middleware(
    CORSMiddleware,

    # Permite solicitudes desde los orígenes definidos
    allow_origins=origins,

    # Permite envío de cookies y autenticación
    allow_credentials=True,

    # Permite todos los métodos HTTP
    allow_methods=["*"],

    # Permite todos los encabezados HTTP
    allow_headers=["*"],
)


# Registra todas las rutas del sistema
app.include_router(teacher_routes.router)
app.include_router(course_routes.router)
app.include_router(class_section_routes.router)
app.include_router(class_session_routes.router)
app.include_router(student_routes.router)
app.include_router(face_routes.router)
app.include_router(recognition_routes.router)
app.include_router(attendance_routes.router)
app.include_router(group_attendance_routes.router)
app.include_router(report_routes.router)
app.include_router(video_attendance.router)


# Crea automáticamente las tablas en la base de datos
# utilizando los modelos definidos
Base.metadata.create_all(bind=engine)


# Ruta principal para probar conexión con la base de datos
@app.get("/")
def test_connection():

    try:

        # Intenta abrir conexión con la base de datos
        conn = engine.connect()

        # Retorna mensaje de conexión exitosa
        return {
            "message": "Conectado a la base de datos"
        }

    # Si ocurre un error de conexión
    except:

        # Retorna mensaje de error
        return {
            "message": "Error de conexión"
        }