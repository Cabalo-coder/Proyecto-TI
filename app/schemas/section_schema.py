# Importa BaseModel de Pydantic para crear esquemas de validación
from pydantic import BaseModel


# Esquema utilizado para crear una sección
class SectionCreate(BaseModel):

    # Nombre de la sección
    section_name: str

    # ID del curso al que pertenece la sección
    course_id: int