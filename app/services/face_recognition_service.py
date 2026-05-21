# Importa NumPy para realizar cálculos matemáticos y manejo de vectores
import numpy as np

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa el modelo Face
from app.models.face import Face

# Importa el modelo Student
from app.models.student import Student


# Umbral máximo permitido para considerar una coincidencia facial válida
MATCH_THRESHOLD = 0.6


# Función que realiza reconocimiento facial y devuelve información detallada
def recognize_face_with_score(db: Session, new_descriptor):

    # Obtiene todos los rostros almacenados en la base de datos
    faces = db.query(Face).all()

    # Variable para almacenar la mejor coincidencia encontrada
    best_match = None

    # Inicializa la distancia mínima con infinito
    min_distance = float("inf")

    # Recorre todos los rostros registrados
    for face in faces:

        try:

            # Obtiene el descriptor facial almacenado
            stored_descriptor = face.facial_descriptor

            # Si el descriptor está vacío, continúa con el siguiente
            if not stored_descriptor:
                continue

            # Calcula la distancia euclidiana entre descriptores
            distance = np.linalg.norm(
                np.array(stored_descriptor) -
                np.array(new_descriptor)
            )

            # Si la distancia es menor a la actual, guarda la coincidencia
            if distance < min_distance:
                min_distance = distance
                best_match = face

        # Manejo de errores durante el procesamiento
        except Exception as e:

            # Muestra el error en consola
            print(f"Error con face_id {face.face_id}: {e}")

            continue

    # Si no se encontró ninguna coincidencia
    if best_match is None:
        return {
            "student": None,
            "distance": None,
            "threshold": MATCH_THRESHOLD,
        }

    # Si la distancia está dentro del umbral permitido
    if min_distance < MATCH_THRESHOLD:

        # Busca al estudiante relacionado con el rostro encontrado
        student = db.query(Student).filter(
            Student.student_id == best_match.student_id
        ).first()

        # Retorna información del estudiante reconocido
        return {
            "student": student,
            "distance": float(min_distance),
            "threshold": MATCH_THRESHOLD,
        }

    # Si la distancia supera el umbral, no se considera coincidencia
    return {
        "student": None,
        "distance": float(min_distance),
        "threshold": MATCH_THRESHOLD,
    }


# Función simplificada para reconocimiento facial
# Retorna únicamente el estudiante encontrado
def recognize_face(db: Session, new_descriptor):

    # Ejecuta el reconocimiento con cálculo de similitud
    result = recognize_face_with_score(
        db,
        new_descriptor
    )

    # Retorna únicamente el estudiante reconocido
    return result["student"]