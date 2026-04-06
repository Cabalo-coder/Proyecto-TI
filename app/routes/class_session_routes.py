from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_teacher
from app.models.class_session import ClassSession
from app.models.course import Course
from app.schemas.class_session_schema import ClassSessionCreate

router = APIRouter(prefix="/sessions", tags=["Class Sessions"])

@router.post("/")
def create_class_session(
    session: ClassSessionCreate,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(get_current_teacher)
):
    teacher_id = teacher_data["id"]

    # 1️. Validar que el curso pertenece al maestro
    course = db.query(Course).filter(
        Course.course_id == session.course_id,
        Course.teacher_id == teacher_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado o no autorizado")

    # 2️. Validar horas
    if session.start_time and session.end_time:
        if session.end_time <= session.start_time:
            raise HTTPException(
                status_code=400,
                detail="La hora de finalización debe ser mayor que la de inicio"
            )

    # 3️. Obtener sesiones del mismo día
    existing_sessions = db.query(ClassSession).filter(
        ClassSession.course_id == session.course_id,
        ClassSession.session_date == session.session_date
    ).all()

    # 4️. Validar solapamiento de horarios
    for existing in existing_sessions:
        if (
            session.start_time and session.end_time and
            existing.start_time and existing.end_time
        ):
            if (
                session.start_time < existing.end_time and
                session.end_time > existing.start_time
            ):
                raise HTTPException(
                    status_code=400,
                    detail="La sesión se solapa con otra existente"
                )

    # 5️. Crear sesión
    new_session = ClassSession(
        course_id=session.course_id,
        session_date=session.session_date,
        start_time=session.start_time,
        end_time=session.end_time
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Clase creada correctamente",
        "session_id": new_session.session_id
    }