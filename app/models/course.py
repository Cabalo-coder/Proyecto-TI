# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base


# Define el modelo Course que representa la tabla "course"
class Course(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "course"

    # Llave primaria de la tabla curso
    course_id = Column(Integer, primary_key=True, index=True)

    # Nombre del curso
    course_name = Column(String(100), nullable=False)

    # Llave foránea que relaciona el curso con un docente
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"))