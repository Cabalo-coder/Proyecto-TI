# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, TIMESTAMP

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base

# Importa datetime para registrar automáticamente la fecha y hora actual
from datetime import datetime


# Define el modelo Teacher que representa la tabla "teacher"
class Teacher(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "teacher"

    # Llave primaria de la tabla docente
    teacher_id = Column(Integer, primary_key=True, index=True)

    # Nombre completo del docente
    name = Column(String(100), nullable=False)

    # Correo electrónico único del docente
    email = Column(String(100), unique=True, nullable=False)

    # Contraseña del docente
    password = Column(String, nullable=False)

    # Fecha y hora de creación del registro del docente
    # Se asigna automáticamente la fecha actual en UTC
    created_at = Column(TIMESTAMP, default=datetime.utcnow)