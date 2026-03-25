from sqlalchemy import Column, Integer, String, ForeignKey
from app.config.database import Base

class Section(Base):
    __tablename__ = "section"

    section_id = Column(Integer, primary_key=True, index=True)
    section_name = Column(String(20), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"))