# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la dependencia para validar y obtener el docente autenticado
from app.dependencies.auth import get_current_teacher

# Importa el modelo ClassSession
from app.models.class_session import ClassSession

# Importa el modelo Course
from app.models.course import Course

# Importa el esquema para validar datos de creación de sesiones
from app.schemas.class_session_schema import ClassSessionCreate


# Crea el router para las rutas relacionadas con sesiones de clase
router = APIRouter(
    prefix="/sessions",        # Prefijo principal de las rutas
    tags=["Class Sessions"]    # Etiqueta para documentación automática
)


# Ruta para crear una nueva sesión de clase
@router.post("/")
def create_class_session(
    session: ClassSessionCreate,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(get_current_teacher)
):

    # Obtiene el ID del docente autenticado
    teacher_id = teacher_data["id"]

    # Verifica que el curso pertenezca al docente
    course = db.query(Course).filter(
        Course.course_id == session.course_id,
        Course.teacher_id == teacher_id
    ).first()

    # Si el curso no existe o no pertenece al docente, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado o no autorizado"
        )

    # Valida que la hora de finalización sea mayor a la de inicio
    if session.start_time and session.end_time:
        if session.end_time <= session.start_time:
            raise HTTPException(
                status_code=400,
                detail="La hora de finalización debe ser mayor que la de inicio"
            )

    # Obtiene sesiones existentes del mismo curso y fecha
    existing_sessions = db.query(ClassSession).filter(
        ClassSession.course_id == session.course_id,
        ClassSession.session_date == session.session_date
    ).all()

    # Verifica que no existan solapamientos de horarios
    for existing in existing_sessions:

        # Valida únicamente si ambas sesiones poseen horario definido
        if (
            session.start_time and session.end_time and
            existing.start_time and existing.end_time
        ):

            # Comprueba si los horarios se traslapan
            if (
                session.start_time < existing.end_time and
                session.end_time > existing.start_time
            ):
                raise HTTPException(
                    status_code=400,
                    detail="La sesión se solapa con otra existente"
                )

    # Crea una nueva sesión de clase
    new_session = ClassSession(
        course_id=session.course_id,
        session_date=session.session_date,
        start_time=session.start_time,
        end_time=session.end_time
    )

    # Guarda la nueva sesión en la base de datos
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Retorna mensaje de éxito y el ID de la sesión creada
    return {
        "message": "Clase creada correctamente",
        "session_id": new_session.session_id
    }


# Ruta para obtener las sesiones de un curso específico
@router.get("/course/{course_id}")
def get_sessions_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(get_current_teacher)
):

    # Obtiene el ID del docente autenticado
    teacher_id = teacher_data["id"]

    # Verifica que el curso pertenezca al docente
    course = db.query(Course).filter(
        Course.course_id == course_id,
        Course.teacher_id == teacher_id
    ).first()

    # Si el curso no pertenece al docente, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="No autorizado"
        )

    # Obtiene todas las sesiones del curso
    sessions = db.query(ClassSession).filter(
        ClassSession.course_id == course_id
    ).all()

    # Retorna las sesiones encontradas
    return sessions


# Ruta para obtener todas las sesiones de los cursos del docente
@router.get("/")
def get_all_sessions(
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(get_current_teacher)
):

    # Obtiene el ID del docente autenticado
    teacher_id = teacher_data["id"]

    # Realiza un JOIN para obtener únicamente sesiones
    # pertenecientes a cursos del docente autenticado
    sessions = db.query(ClassSession).join(Course).filter(
        Course.teacher_id == teacher_id
    ).all()

    # Retorna todas las sesiones encontradas
    return sessions