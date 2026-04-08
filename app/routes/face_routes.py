from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.models.face import Face
from app.models.student import Student
from app.models.class_section import Section
from app.models.course import Course

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_teacher

from app.config.supabase import supabase
from app.utils.face_utils import generate_face_descriptor

router = APIRouter(prefix="/faces", tags=["Faces"])


@router.post("/upload")
def upload_face(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    # Validar estudiante
    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Validar relación teacher
    section = db.query(Section).filter(
        Section.section_id == student.section_id
    ).first()

    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    course = db.query(Course).filter(
        Course.course_id == section.course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if course.teacher_id != current_teacher["id"]:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    # Generar nombre único
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = file_name

    # Leer archivo
    file_bytes = file.file.read()

    # Generar descriptor facial
    descriptor = generate_face_descriptor(file_bytes)

    if descriptor is None:
        raise HTTPException(
            status_code=400,
            detail="No se detectó ningún rostro en la imagen"
        )

    # IMPORTANTE: convertir a lista (por si viene como numpy array)
    descriptor_list = descriptor.tolist() if hasattr(descriptor, "tolist") else descriptor

    # Subir a Supabase
    supabase.storage.from_("faces").upload(file_path, file_bytes)

    # Obtener URL pública
    image_url = supabase.storage.from_("faces").get_public_url(file_path)

    # Guardar en DB (JSON limpio, SIN str)
    new_face = Face(
        student_id=student_id,
        image_url=image_url,
        facial_descriptor=descriptor_list   
    )

    db.add(new_face)
    db.commit()
    db.refresh(new_face)

    return {
        "message": "Imagen subida correctamente",
        "image_url": image_url,
        "face_id": new_face.face_id
    }