from pydantic import BaseModel
from datetime import date, time

class ClassSessionCreate(BaseModel):
    course_id: int
    session_date: date
    start_time: time | None = None
    end_time: time | None = None