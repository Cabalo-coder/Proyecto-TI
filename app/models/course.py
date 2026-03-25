from sqlalchemy import Column, Integer, String, ForeignKey
from app.config.database import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))