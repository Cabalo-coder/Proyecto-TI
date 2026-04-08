from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from app.config.database import Base
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class Face(Base):
    __tablename__ = "face"

    face_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.student_id"))
    facial_descriptor = Column(JSON)
    image_url = Column(Text)
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)