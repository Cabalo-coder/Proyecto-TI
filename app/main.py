from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.models import *
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
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

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