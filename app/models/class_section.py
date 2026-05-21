# Importa los tipos de datos y herramientas necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

# Importa la clase Base desde la configuración de la base de datos
from app.config.database import Base


# Define el modelo Section que representa la tabla "section"
class Section(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "section"

    # Llave primaria de la tabla sección
    section_id = Column(Integer, primary_key=True, index=True)

    # Nombre o identificador de la sección
    section_name = Column(String(20), nullable=False)

    # Llave foránea que relaciona la sección con un curso
    course_id = Column(Integer, ForeignKey("course.course_id"))