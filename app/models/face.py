# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base

# Importa el tipo JSON específico para PostgreSQL
from sqlalchemy.dialects.postgresql import JSON

# Importa datetime para registrar la fecha y hora actual automáticamente
from datetime import datetime


# Define el modelo Face que representa la tabla "face"
class Face(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "face"

    # Llave primaria de la tabla rostro
    face_id = Column(Integer, primary_key=True, index=True)

    # Llave foránea que relaciona el rostro con un estudiante
    student_id = Column(Integer, ForeignKey("student.student_id"))

    # Descriptor facial almacenado en formato JSON
    facial_descriptor = Column(JSON)

    # URL de la imagen facial almacenada en Supabase u otro servicio
    image_url = Column(Text)

    # Fecha y hora de registro del rostro
    # Se asigna automáticamente la fecha actual en UTC
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)