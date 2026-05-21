# Importa BaseModel de Pydantic para crear esquemas de validación
from pydantic import BaseModel

# Importa los tipos de dato date y time
from datetime import date, time


# Esquema utilizado para crear una sesión de clase
class ClassSessionCreate(BaseModel):

    # ID del curso al que pertenece la sesión
    course_id: int

    # Fecha en la que se realizará la sesión
    session_date: date

    # Hora de inicio de la sesión (opcional)
    start_time: time | None = None

    # Hora de finalización de la sesión (opcional)
    end_time: time | None = None