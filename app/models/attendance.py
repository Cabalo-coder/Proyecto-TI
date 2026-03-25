from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from app.config.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    session_id = Column(Integer, ForeignKey("class_sessions.session_id"))
    check_in_time = Column(TIMESTAMP)
    status = Column(String(20), default="Present")