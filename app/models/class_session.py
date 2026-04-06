from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from app.config.database import Base

class ClassSession(Base):
    __tablename__ = "class_session"

    session_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.course_id"))
    session_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)