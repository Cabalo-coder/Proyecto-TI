from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.face_recognition_service import recognize_face

router = APIRouter(prefix="/recognition", tags=["Recognition"])

@router.post("/")
def recognize(data: dict, db: Session = Depends(get_db)):
    descriptor = data["descriptor"]

    student = recognize_face(db, descriptor)

    if student:
        return {
            "message": "Estudiante reconocido",
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.last_name}"
        }
    else:
        return {"message": "No reconocido"}