import numpy as np
from sqlalchemy.orm import Session
from app.models.face import Face
from app.models.student import Student


def recognize_face(db: Session, new_descriptor):
    faces = db.query(Face).all()

    best_match = None
    min_distance = float("inf")

    for face in faces:
        try:
            # ya no necesitamos eval
            stored_descriptor = face.facial_descriptor

            # Validación
            if not stored_descriptor:
                continue

            distance = np.linalg.norm(
                np.array(stored_descriptor) - np.array(new_descriptor)
            )

            if distance < min_distance:
                min_distance = distance
                best_match = face

        except Exception as e:
            print(f"Error con face_id {face.face_id}: {e}")
            continue

    # validación extra
    if best_match is None:
        return None

    # umbral (puedes ajustarlo)
    if min_distance < 0.6:
        student = db.query(Student).filter(
            Student.student_id == best_match.student_id
        ).first()
        return student

    return None