# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base


# Define el modelo Attendance que representa la tabla "attendance"
class Attendance(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "attendance"

    # Llave primaria de la tabla de asistencia
    attendance_id = Column(Integer, primary_key=True, index=True)

    # Llave foránea que relaciona la asistencia con un estudiante
    student_id = Column(Integer, ForeignKey("student.student_id"))

    # Llave foránea que relaciona la asistencia con una sesión de clase
    session_id = Column(Integer, ForeignKey("class_session.session_id"))

    # Fecha y hora en la que el estudiante registró su asistencia
    check_in_time = Column(TIMESTAMP)

    # Estado de la asistencia (por defecto será "Present")
    status = Column(String(20), default="Present")