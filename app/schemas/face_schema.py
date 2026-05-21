# Importa BaseModel de Pydantic para crear esquemas de validación
from pydantic import BaseModel


# Esquema utilizado para registrar un rostro
class FaceCreate(BaseModel):

    # Descriptor facial generado mediante reconocimiento facial
    facial_descriptor: str

    # ID del estudiante asociado al rostro
    student_id: int