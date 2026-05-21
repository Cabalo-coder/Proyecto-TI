# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, Date, Time, ForeignKey

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base


# Define el modelo ClassSession que representa la tabla "class_session"
class ClassSession(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "class_session"

    # Llave primaria de la tabla sesión de clase
    session_id = Column(Integer, primary_key=True, index=True)

    # Llave foránea que relaciona la sesión con un curso
    course_id = Column(Integer, ForeignKey("course.course_id"))

    # Fecha en la que se realiza la sesión de clase
    session_date = Column(Date, nullable=False)

    # Hora de inicio de la sesión (opcional)
    start_time = Column(Time, nullable=True)

    # Hora de finalización de la sesión (opcional)
    end_time = Column(Time, nullable=True)