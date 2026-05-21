# Importa CryptContext para manejar el cifrado y verificación de contraseñas
from passlib.context import CryptContext

# Importa la excepción para manejar hashes desconocidos
from passlib.exc import UnknownHashError


# Configura el contexto de cifrado utilizando pbkdf2_sha256
# Este algoritmo evita conflictos comunes de bcrypt y es compatible
# con diferentes plataformas y entornos
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


# Función para cifrar una contraseña
def hash_password(password: str):

    # Retorna la contraseña cifrada
    return pwd_context.hash(password)


# Función para verificar una contraseña
def verify_password(plain_password, hashed_password):

    try:

        # Compara la contraseña ingresada con el hash almacenado
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    # Maneja errores relacionados con hashes inválidos
    except (UnknownHashError, ValueError, TypeError):

        # Retorna False si ocurre algún error
        return False