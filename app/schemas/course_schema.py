# Importa BaseModel de Pydantic para crear esquemas de validación
from pydantic import BaseModel


# Esquema utilizado para crear un curso
class CourseCreate(BaseModel):

    # Nombre del curso
    course_name: str