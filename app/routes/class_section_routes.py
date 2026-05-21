# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa el modelo Section
from app.models.class_section import Section

# Importa el modelo Course
from app.models.course import Course

# Importa el esquema para validar datos de creación de secciones
from app.schemas.section_schema import SectionCreate

# Importa la función para verificar autenticación mediante JWT
from app.utils.jwt import verify_token


# Crea el router para las rutas relacionadas con secciones
router = APIRouter(
    prefix="/sections",   # Prefijo principal de las rutas
    tags=["Sections"]     # Etiqueta para documentación automática
)


# Ruta para crear una nueva sección
@router.post("/")
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):

    # Obtiene el ID del profesor autenticado desde el token
    teacher_id = teacher_data["id"]

    # Verifica que el curso pertenezca al profesor autenticado
    course = db.query(Course).filter(
        Course.course_id == section.course_id,
        Course.teacher_id == teacher_id
    ).first()

    # Si el curso no existe o no pertenece al profesor, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado o no autorizado"
        )

    # Crea una nueva sección
    new_section = Section(
        section_name=section.section_name,
        course_id=section.course_id
    )

    # Guarda la nueva sección en la base de datos
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    # Retorna mensaje de éxito y el ID de la sección creada
    return {
        "message": "Sección creada correctamente",
        "section_id": new_section.section_id
    }


# Ruta para obtener las secciones de un curso específico
@router.get("/course/{course_id}")
def get_sections_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):

    # Obtiene el ID del profesor autenticado
    teacher_id = teacher_data["id"]

    # Verifica que el curso pertenezca al profesor
    course = db.query(Course).filter(
        Course.course_id == course_id,
        Course.teacher_id == teacher_id
    ).first()

    # Si el curso no pertenece al profesor, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="No autorizado"
        )

    # Obtiene todas las secciones asociadas al curso
    sections = db.query(Section).filter(
        Section.course_id == course_id
    ).all()

    # Retorna la lista de secciones
    return sections


# Ruta para obtener todas las secciones del profesor autenticado
@router.get("/")
def get_sections(
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):

    # Obtiene el ID del profesor autenticado
    teacher_id = teacher_data["id"]

    # Consulta todas las secciones relacionadas con los cursos del profesor
    sections = db.query(Section, Course).join(Course).filter(
        Course.teacher_id == teacher_id
    ).all()

    # Lista que almacenará el resultado final
    result = []

    # Recorre cada sección encontrada
    for section, course in sections:

        # Agrega información de la sección y su curso relacionado
        result.append({
            "section_id": section.section_id,
            "section_name": section.section_name,
            "course_id": course.course_id,
            "course_name": course.course_name
        })

    # Retorna todas las secciones del profesor
    return result