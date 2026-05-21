# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa el modelo Course
from app.models.course import Course

# Importa el esquema para validar datos de creación de cursos
from app.schemas.course_schema import CourseCreate

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la dependencia para obtener el docente autenticado
from app.dependencies.auth import get_current_teacher

# Importa la función para verificar el token JWT
from app.utils.jwt import verify_token


# Crea el router para las rutas relacionadas con cursos
router = APIRouter(
    prefix="/courses",   # Prefijo principal de las rutas
    tags=["Courses"]     # Etiqueta para documentación automática
)


# Ruta para crear un nuevo curso
@router.post("/")
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Crea una nueva instancia del curso
    new_course = Course(
        course_name=data.course_name,
        teacher_id=current_teacher["id"]
    )

    # Guarda el curso en la base de datos
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    # Retorna mensaje de éxito y datos del curso creado
    return {
        "message": "Curso creado correctamente",
        "course": {
            "id": new_course.course_id,
            "name": new_course.course_name
        }
    }


# Ruta para obtener todos los cursos del docente autenticado
@router.get("/")
def get_courses(
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):

    # Obtiene el ID del docente desde el token
    teacher_id = user["id"]

    # Consulta todos los cursos asociados al docente
    courses = db.query(Course).filter(
        Course.teacher_id == teacher_id
    ).all()

    # Retorna la lista de cursos encontrados
    return courses