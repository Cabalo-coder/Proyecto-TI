from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.utils.face_utils import generate_multiple_descriptors
from app.services.face_recognition_service import recognize_face
from app.services.attendance_service import mark_attendance

router = APIRouter(prefix="/group", tags=["Group Recognition"])


@router.post("/recognize")
def recognize_group(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = file.file.read()

    descriptors = generate_multiple_descriptors(image_bytes)

    if not descriptors:
        return {"message": "No se detectaron rostros"}

    results = []

    for descriptor in descriptors:
        student = recognize_face(db, descriptor)

        if student:
            attendance = mark_attendance(db, student.student_id)

            results.append({
                "student_id": student.student_id,
                "name": f"{student.first_name} {student.last_name}",
                "attendance": attendance
            })

    return {
        "total_faces_detected": len(descriptors),
        "recognized": results
    }