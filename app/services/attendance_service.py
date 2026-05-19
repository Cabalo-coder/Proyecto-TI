import datetime
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.class_session import ClassSession


def mark_attendance(db: Session, student_id: int):
    now = datetime.datetime.now()

    current_time = now.time()

    # buscar sesión ACTIVA
    session = db.query(ClassSession).filter(
        ClassSession.session_date == now.date(),
        ClassSession.start_time <= current_time,
        ClassSession.end_time >= current_time
    ).first()

    if not session:
        return {"error": "No hay sesión activa en este horario"}

    existing = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.session_id == session.session_id
    ).first()

    if existing:

        diff = (now - existing.check_in_time).total_seconds()

        if diff < 10:
            return {"message": "Ya registrado recientemente"}

        return {"message": "Asistencia ya registrada"}

    new_attendance = Attendance(
        student_id=student_id,
        session_id=session.session_id,
        check_in_time=now,
        status="Present"
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {
        "message": "Asistencia registrada",
        "student_id": student_id,
        "session_id": session.session_id
    }