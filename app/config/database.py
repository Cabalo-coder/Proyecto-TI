# Importa la función create_engine para crear la conexión con la base de datos
from sqlalchemy import create_engine

# Importa herramientas de SQLAlchemy para manejar sesiones y modelos base
from sqlalchemy.orm import sessionmaker, declarative_base

# Permite acceder a variables de entorno del sistema
import os

# Importa load_dotenv para cargar variables desde el archivo .env
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()

# Obtiene la URL de conexión a la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crea el motor de conexión hacia la base de datos
engine = create_engine(DATABASE_URL)

# Configura la sesión que permitirá realizar operaciones CRUD en la base de datos
SessionLocal = sessionmaker(
    autocommit=False,  # Evita commits automáticos
    autoflush=False,   # Evita sincronizaciones automáticas
    bind=engine        # Vincula la sesión con el motor de conexión
)

# Crea la clase base para definir los modelos/tablas de la base de datos
Base = declarative_base()