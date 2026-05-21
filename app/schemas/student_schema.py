# Importa BaseModel de Pydantic para crear esquemas de validación
from pydantic import BaseModel


# Esquema utilizado para crear un estudiante
class StudentCreate(BaseModel):

    # Nombre del estudiante
    first_name: str

    # Apellido del estudiante
    last_name: str

    # Número de carné del estudiante
    carne: str

    # ID de la sección a la que pertenece el estudiante
    section_id: int