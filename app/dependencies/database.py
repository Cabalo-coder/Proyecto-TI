# Importa la sesión local configurada para la base de datos
from app.config.database import SessionLocal


# Dependencia para obtener una conexión a la base de datos
def get_db():

    # Crea una nueva sesión de base de datos
    db = SessionLocal()

    try:

        # Retorna la sesión para ser utilizada en las rutas
        yield db

    finally:

        # Cierra la conexión al finalizar la petición
        db.close()