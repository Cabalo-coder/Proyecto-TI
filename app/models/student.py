# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base

# Importa datetime para registrar automáticamente la fecha y hora actual
from datetime import datetime


# Define el modelo Student que representa la tabla "student"
class Student(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "student"

    # Llave primaria de la tabla estudiante
    student_id = Column(Integer, primary_key=True, index=True)

    # Nombre del estudiante
    first_name = Column(String(100), nullable=False)

    # Apellido del estudiante
    last_name = Column(String(100), nullable=False)

    # Número de carné único del estudiante
    carne = Column(String(50), unique=True, nullable=False)

    # Llave foránea que relaciona al estudiante con una sección
    section_id = Column(Integer, ForeignKey("section.section_id"))

    # Fecha y hora de registro del estudiante
    # Se asigna automáticamente la fecha actual en UTC
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)