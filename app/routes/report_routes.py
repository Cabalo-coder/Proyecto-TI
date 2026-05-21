# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la dependencia para obtener el docente autenticado
from app.dependencies.auth import get_current_teacher

# Importa los servicios encargados de generar reportes
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


# Crea el router para las rutas relacionadas con reportes
router = APIRouter(
    prefix="/reports",   # Prefijo principal de las rutas
    tags=["Reports"]     # Etiqueta para documentación automática
)


# Ruta para obtener el resumen general del dashboard
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el resumen del sistema para el docente autenticado
    return get_dashboard_summary(
        db,
        current_teacher["id"]
    )


# Ruta para obtener reporte de asistencia por curso
@router.get("/course/{course_id}")
def course_report(
    course_id: int,
    db: Session = Depends(get_db)
):

    # Retorna el reporte de asistencia del curso indicado
    return get_course_attendance(
        db,
        course_id
    )


# Ruta para obtener historial de asistencia de un estudiante
@router.get("/student/{student_id}")
def student_history(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Retorna el historial del estudiante indicado
    return get_student_history(
        db,
        student_id
    )


# Ruta para generar reporte diario
@router.get("/daily")
def daily_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el reporte diario del docente autenticado
    return get_daily_report(
        db,
        current_teacher["id"]
    )


# Ruta para generar reporte semanal
@router.get("/weekly")
def weekly_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el reporte semanal del docente autenticado
    return get_weekly_report(
        db,
        current_teacher["id"]
    )


# Ruta para generar reporte mensual
@router.get("/monthly")
def monthly_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el reporte mensual del docente autenticado
    return get_monthly_report(
        db,
        current_teacher["id"]
    )


# Ruta para generar reporte semestral
@router.get("/semester")
def semester_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el reporte semestral del docente autenticado
    return get_semester_report(
        db,
        current_teacher["id"]
    )


# Ruta para generar reporte agrupado por secciones
@router.get("/by-sections")
def by_sections_report(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Retorna el reporte organizado por secciones
    return get_report_by_sections(
        db,
        current_teacher["id"]
    )