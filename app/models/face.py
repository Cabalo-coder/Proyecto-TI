from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from app.config.database import Base

class Face(Base):
    __tablename__ = "faces"

    face_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    facial_descriptor = Column(Text)
    image_url = Column(Text)
    registration_date = Column(TIMESTAMP)