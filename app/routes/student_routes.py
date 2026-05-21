# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa excepciones de SQLAlchemy para manejo de errores
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Importa el modelo Student
from app.models.student import Student

# Importa el modelo Section
from app.models.class_section import Section

# Importa el modelo Course
from app.models.course import Course

# Importa el esquema para validar datos de creación de estudiantes
from app.schemas.student_schema import StudentCreate

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la dependencia para obtener el docente autenticado
from app.dependencies.auth import get_current_teacher


# Crea el router para las rutas relacionadas con estudiantes
router = APIRouter(
    prefix="/students",   # Prefijo principal de las rutas
    tags=["Students"]     # Etiqueta para documentación automática
)


# Ruta para crear un estudiante
# Solo un docente autenticado puede registrar estudiantes
@router.post("/")
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Obtiene el ID del docente autenticado
    teacher_id = (
        current_teacher.get("id")
        if isinstance(current_teacher, dict)
        else None
    )

    # Valida que el token contenga el ID del docente
    if teacher_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido: id de profesor no encontrado"
        )

    # Busca la sección indicada
    section = db.query(Section).filter(
        Section.section_id == data.section_id
    ).first()

    # Si la sección no existe, genera error
    if not section:
        raise HTTPException(
            status_code=404,
            detail="La sección no existe"
        )

    # Busca el curso relacionado con la sección
    course = db.query(Course).filter(
        Course.course_id == section.course_id
    ).first()

    # Si el curso no existe, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    # Verifica que el curso pertenezca al docente autenticado
    if course.teacher_id != teacher_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para agregar estudiantes a esta sección"
        )

    # Verifica si el carné ya está registrado
    existing_student = db.query(Student).filter(
        Student.carne == data.carne
    ).first()

    # Si el carné ya existe, genera error
    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="El carné ya está registrado"
        )

    # Crea una nueva instancia del estudiante
    new_student = Student(
        first_name=data.first_name,
        last_name=data.last_name,
        carne=data.carne,
        section_id=data.section_id
    )

    try:

        # Guarda el estudiante en la base de datos
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

    # Maneja errores por duplicidad de datos
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="No se pudo crear el estudiante: carné duplicado"
        )

    # Maneja errores generales de base de datos
    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Error de base de datos al crear estudiante"
        )

    # Retorna mensaje de éxito y datos del estudiante creado
    return {
        "message": "Estudiante creado correctamente",
        "student_id": new_student.student_id,
        "name": f"{new_student.first_name} {new_student.last_name}",
        "carne": new_student.carne,
        "section_id": new_student.section_id
    }


# Ruta para obtener toda la estructura académica del docente
# Cursos -> Secciones -> Estudiantes
@router.get("/my-structure")
def get_teacher_structure(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Obtiene todos los cursos del docente autenticado
    courses = db.query(Course).filter(
        Course.teacher_id == current_teacher["id"]
    ).all()

    # Lista que almacenará la estructura final
    result = []

    # Recorre cada curso encontrado
    for course in courses:

        # Estructura base del curso
        course_data = {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "sections": []
        }

        # Obtiene las secciones asociadas al curso
        sections = db.query(Section).filter(
            Section.course_id == course.course_id
        ).all()

        # Recorre cada sección encontrada
        for section in sections:

            # Estructura base de la sección
            section_data = {
                "section_id": section.section_id,
                "section_name": section.section_name,
                "students": []
            }

            # Obtiene los estudiantes de la sección
            students = db.query(Student).filter(
                Student.section_id == section.section_id
            ).all()

            # Recorre cada estudiante encontrado
            for student in students:

                # Agrega los datos del estudiante a la sección
                section_data["students"].append({
                    "id": student.student_id,
                    "name": f"{student.first_name} {student.last_name}",
                    "carne": student.carne
                })

            # Agrega la sección al curso
            course_data["sections"].append(section_data)

        # Agrega el curso al resultado final
        result.append(course_data)

    # Retorna toda la estructura académica del docente
    return {
        "courses": result
    }