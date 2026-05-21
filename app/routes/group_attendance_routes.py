# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, UploadFile, File, Depends

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la función encargada de generar múltiples descriptores faciales
from app.utils.face_utils import generate_multiple_descriptors

# Importa el servicio encargado del reconocimiento facial
from app.services.face_recognition_service import recognize_face

# Importa el servicio encargado de registrar asistencias
from app.services.attendance_service import mark_attendance


# Crea el router para las rutas relacionadas con reconocimiento grupal
router = APIRouter(
    prefix="/group",               # Prefijo principal de las rutas
    tags=["Group Recognition"]     # Etiqueta para documentación automática
)


# Ruta para reconocer múltiples rostros en una imagen grupal
@router.post("/recognize")
def recognize_group(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Lee el archivo de imagen recibido en bytes
    image_bytes = file.file.read()

    # Genera los descriptores faciales de todos los rostros detectados
    descriptors = generate_multiple_descriptors(image_bytes)

    # Si no se detectan rostros, retorna mensaje
    if not descriptors:
        return {"message": "No se detectaron rostros"}

    # Lista donde se almacenarán los estudiantes reconocidos
    results = []

    # Recorre cada descriptor facial detectado
    for descriptor in descriptors:

        # Busca coincidencia facial en la base de datos
        student = recognize_face(db, descriptor)

        # Si el estudiante fue reconocido
        if student:

            # Registra la asistencia del estudiante
            attendance = mark_attendance(
                db,
                student.student_id
            )

            # Agrega los datos del estudiante reconocido
            results.append({
                "student_id": student.student_id,
                "name": f"{student.first_name} {student.last_name}",
                "attendance": attendance
            })

    # Retorna el total de rostros detectados y reconocidos
    return {
        "total_faces_detected": len(descriptors),
        "recognized": results
    }