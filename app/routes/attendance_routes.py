# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa BaseModel de Pydantic para validar datos recibidos
from pydantic import BaseModel

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa el servicio encargado del reconocimiento facial
from app.services.face_recognition_service import recognize_face

# Importa el servicio encargado de registrar la asistencia
from app.services.attendance_service import mark_attendance

# Importa el modelo Student
from app.models.student import Student


# Crea el router para las rutas relacionadas con asistencia
router = APIRouter(
    prefix="/attendance",   # Prefijo principal de las rutas
    tags=["Attendance"]     # Etiqueta para documentación automática
)


# Modelo para validar el ID del estudiante recibido en el body
class AttendanceMarkRequest(BaseModel):
    student_id: int


# Ruta para reconocer un rostro y registrar asistencia automáticamente
@router.post("/recognize")
def recognize_and_mark(data: dict, db: Session = Depends(get_db)):

    # Obtiene el descriptor facial enviado desde el frontend
    descriptor = data["descriptor"]

    # Busca al estudiante mediante reconocimiento facial
    student = recognize_face(db, descriptor)

    # Si no se reconoce el rostro, retorna mensaje de error
    if not student:
        return {"message": "No reconocido"}

    # Registra la asistencia del estudiante reconocido
    result = mark_attendance(db, student.student_id)

    # Retorna información del estudiante y resultado de asistencia
    return {
        "student": {
            "id": student.student_id,
            "name": f"{student.first_name} {student.last_name}"
        },
        "attendance": result
    }


# Ruta para registrar asistencia manual utilizando el ID del estudiante
@router.post("/mark")
def mark_by_student(
    data: AttendanceMarkRequest,
    db: Session = Depends(get_db)
):

    # Busca al estudiante en la base de datos
    student = db.query(Student).filter(
        Student.student_id == data.student_id
    ).first()

    # Si el estudiante no existe, genera error 404
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    # Registra la asistencia del estudiante
    result = mark_attendance(db, student.student_id)

    # Retorna información del estudiante y resultado de asistencia
    return {
        "student": {
            "id": student.student_id,
            "name": f"{student.first_name} {student.last_name}"
        },
        "attendance": result
    }