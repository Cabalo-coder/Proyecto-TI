# Importa el módulo datetime para trabajar con fechas y horas
import datetime

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa el modelo Attendance
from app.models.attendance import Attendance

# Importa el modelo ClassSession
from app.models.class_session import ClassSession


# Función encargada de registrar asistencia
def mark_attendance(db: Session, student_id: int):

    # Obtiene la fecha y hora actual
    now = datetime.datetime.now()

    # Obtiene únicamente la hora actual
    current_time = now.time()

    # Busca una sesión activa según la fecha y hora actual
    session = db.query(ClassSession).filter(
        ClassSession.session_date == now.date(),
        ClassSession.start_time <= current_time,
        ClassSession.end_time >= current_time
    ).first()

    # Si no existe una sesión activa, retorna mensaje de error
    if not session:
        return {
            "error": "No hay sesión activa en este horario"
        }

    # Verifica si el estudiante ya tiene asistencia registrada
    existing = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.session_id == session.session_id
    ).first()

    # Si ya existe una asistencia registrada
    if existing:

        # Calcula la diferencia de tiempo desde el último registro
        diff = (
            now - existing.check_in_time
        ).total_seconds()

        # Si fue registrado hace menos de 10 segundos
        if diff < 10:
            return {
                "message": "Ya registrado recientemente"
            }

        # Si ya existe asistencia previa
        return {
            "message": "Asistencia ya registrada"
        }

    # Crea una nueva asistencia
    new_attendance = Attendance(
        student_id=student_id,
        session_id=session.session_id,
        check_in_time=now,
        status="Present"
    )

    # Guarda la asistencia en la base de datos
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    # Retorna mensaje de éxito y datos de asistencia
    return {
        "message": "Asistencia registrada",
        "student_id": student_id,
        "session_id": session.session_id
    }