from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.class_section import Section
from app.models.course import Course

from app.schemas.student_schema import StudentCreate

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_teacher

router = APIRouter(prefix="/students", tags=["Students"])


# CREAR ESTUDIANTE (PROTEGIDO POR TEACHER)
@router.post("/")
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    # 1. Buscar sección
    section = db.query(Section).filter(
        Section.section_id == data.section_id
    ).first()

    if not section:
        raise HTTPException(status_code=404, detail="La sección no existe")

    # 2. Buscar curso de esa sección
    course = db.query(Course).filter(
        Course.course_id == section.course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    # 3. Validar que el curso pertenece al teacher logueado
    if course.teacher_id != current_teacher["id"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para agregar estudiantes a esta sección"
        )

    # 4. Crear estudiante
    new_student = Student(
        first_name=data.first_name,
        last_name=data.last_name,
        carne=data.carne,
        section_id=data.section_id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Estudiante creado correctamente",
        "student": {
            "id": new_student.student_id,
            "name": f"{new_student.first_name} {new_student.last_name}",
            "carne": new_student.carne,
            "section_id": new_student.section_id
        }
    }

# OBTENER TODO EL ÁRBOL DEL TEACHER
@router.get("/my-structure")
def get_teacher_structure(
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    # 1. Obtener cursos del teacher
    courses = db.query(Course).filter(
        Course.teacher_id == current_teacher["id"]
    ).all()

    result = []

    for course in courses:
        course_data = {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "sections": []
        }

        # 2. Obtener secciones del curso
        sections = db.query(Section).filter(
            Section.course_id == course.course_id
        ).all()

        for section in sections:
            section_data = {
                "section_id": section.section_id,
                "section_name": section.section_name,
                "students": []
            }

            # 3. Obtener estudiantes de la sección
            students = db.query(Student).filter(
                Student.section_id == section.section_id
            ).all()

            for student in students:
                section_data["students"].append({
                    "id": student.student_id,
                    "name": f"{student.first_name} {student.last_name}",
                    "carne": student.carne
                })

            course_data["sections"].append(section_data)

        result.append(course_data)

    return {
        "courses": result
    }