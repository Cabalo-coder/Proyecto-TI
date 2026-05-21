# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa el modelo Teacher
from app.models.teacher import Teacher

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa funciones de seguridad para verificar y cifrar contraseñas
from app.utils.security import verify_password, hash_password

# Importa la función para generar tokens JWT
from app.utils.jwt import create_access_token

# Importa los esquemas para validación de datos
from app.schemas.teacher_schema import TeacherCreate, TeacherLogin


# Crea el router para las rutas relacionadas con docentes
router = APIRouter(
    prefix="/teachers",   # Prefijo principal de las rutas
    tags=["Teachers"]     # Etiqueta para documentación automática
)


# Ruta para registrar un nuevo docente
@router.post("/register")
def register(
    data: TeacherCreate,
    db: Session = Depends(get_db)
):

    # Verifica si el correo ya está registrado
    existing = db.query(Teacher).filter(
        Teacher.email == data.email
    ).first()

    # Si el correo ya existe, retorna mensaje de error
    if existing:
        return {"error": "El correo ya está registrado"}

    # Crea una nueva instancia del docente
    new_teacher = Teacher(
        name=data.name,
        email=data.email,

        # La contraseña se almacena cifrada
        password=hash_password(data.password)
    )

    # Guarda el docente en la base de datos
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    # Retorna mensaje de éxito
    return {
        "message": "Profesor creado correctamente"
    }


# Ruta para iniciar sesión
@router.post("/login")
def login(
    data: TeacherLogin,
    db: Session = Depends(get_db)
):

    # Busca al docente por correo electrónico
    teacher = db.query(Teacher).filter(
        Teacher.email == data.email
    ).first()

    # Si el usuario no existe, retorna error
    if not teacher:
        return {"error": "Usuario no encontrado"}

    # Verifica que la contraseña sea correcta
    if not verify_password(data.password, teacher.password):
        return {"error": "Contraseña incorrecta"}

    # Genera el token JWT del usuario autenticado
    token = create_access_token({
        "sub": teacher.email,
        "id": teacher.teacher_id
    })

    # Retorna mensaje de bienvenida y token de acceso
    return {
        "message": f"Bienvenid@ al sistema {teacher.name}",
        "access_token": token,
        "token_type": "bearer"
    }