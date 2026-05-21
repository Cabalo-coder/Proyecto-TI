# Importa BaseModel y EmailStr de Pydantic
# BaseModel permite crear esquemas de validación
# EmailStr valida automáticamente el formato del correo electrónico
from pydantic import BaseModel, EmailStr


# Esquema utilizado para registrar un docente
class TeacherCreate(BaseModel):

    # Nombre completo del docente
    name: str

    # Correo electrónico del docente
    email: EmailStr

    # Contraseña del docente
    password: str


# Esquema utilizado para iniciar sesión
class TeacherLogin(BaseModel):

    # Correo electrónico del docente
    email: EmailStr

    # Contraseña del docente
    password: str