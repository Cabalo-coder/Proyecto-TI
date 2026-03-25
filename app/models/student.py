from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from app.config.database import Base

class Student(Base):
    __tablename__ = "student"

    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    carne = Column(String(50), unique=True, nullable=False)
    section_id = Column(Integer, ForeignKey("sections.section_id"))
    registration_date = Column(TIMESTAMP)