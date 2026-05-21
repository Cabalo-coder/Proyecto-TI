# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa el servicio de reconocimiento facial con cálculo de similitud
from app.services.face_recognition_service import recognize_face_with_score


# Crea el router para las rutas relacionadas con reconocimiento facial
router = APIRouter(
    prefix="/recognition",   # Prefijo principal de las rutas
    tags=["Recognition"]     # Etiqueta para documentación automática
)


# Función auxiliar para calcular el porcentaje de confianza
def _build_confidence(distance, threshold):

    # Si no existe distancia o threshold, retorna 0
    if distance is None or not threshold:
        return 0.0

    # Calcula la relación de similitud
    ratio = 1 - (distance / threshold)

    # Limita el valor entre 0 y 1
    bounded = max(0.0, min(1.0, ratio))

    # Convierte el valor a porcentaje
    return round(bounded * 100, 2)


# Ruta para reconocer un estudiante mediante descriptor facial
@router.post("/")
def recognize(
    data: dict,
    db: Session = Depends(get_db)
):

    # Obtiene el descriptor facial enviado desde el frontend
    descriptor = data["descriptor"]

    # Ejecuta el reconocimiento facial
    result = recognize_face_with_score(db, descriptor)

    # Obtiene los datos retornados por el servicio
    student = result["student"]
    distance = result["distance"]
    threshold = result["threshold"]

    # Si el estudiante fue reconocido
    if student:

        # Retorna información del estudiante reconocido
        return {
            "message": "Estudiante reconocido",
            "verified": True,
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.last_name}",
            "distance": distance,
            "threshold": threshold,
            "confidence": _build_confidence(distance, threshold),
        }

    # Si no hubo coincidencia facial
    else:

        # Retorna respuesta indicando que no fue reconocido
        return {
            "message": "No reconocido",
            "verified": False,
            "distance": distance,
            "threshold": threshold,
            "confidence": _build_confidence(distance, threshold),
        }