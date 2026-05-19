from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_teacher

from app.services.report_service import (
    get_dashboard_summary,
    get_course_attendance,
    get_student_history,
    get_daily_report,
    get_weekly_report,
    get_monthly_report,
    get_semester_report,
    get_report_by_sections
)

router = APIRouter(prefix="/reports", tags=["Reports"])


# Dashboard
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_dashboard_summary(db, current_teacher["id"])


# Por curso
@router.get("/course/{course_id}")
def course_report(
    course_id: int,
    db: Session = Depends(get_db)
):
    return get_course_attendance(db, course_id)


# Historial estudiante
@router.get("/student/{student_id}")
def student_history(
    student_id: int,
    db: Session = Depends(get_db)
):
    return get_student_history(db, student_id)

# Diario
@router.get("/daily")
def daily_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_daily_report(db, current_teacher["id"])


# Semanal
@router.get("/weekly")
def weekly_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_weekly_report(db, current_teacher["id"])


# Mensual
@router.get("/monthly")
def monthly_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_monthly_report(db, current_teacher["id"])


# Semestral
@router.get("/semester")
def semester_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_semester_report(db, current_teacher["id"])


# Por secciones
@router.get("/by-sections")
def by_sections_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    return get_report_by_sections(db, current_teacher["id"])