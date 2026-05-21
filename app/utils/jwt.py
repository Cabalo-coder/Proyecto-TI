# Importa jwt y JWTError desde python-jose para manejo de tokens JWT
from jose import jwt, JWTError

# Importa herramientas para trabajar con fechas y tiempos
from datetime import datetime, timedelta

# Importa dependencias y excepciones de FastAPI
from fastapi import Depends, HTTPException

# Importa herramientas de autenticación HTTP Bearer
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)


# Clave secreta utilizada para firmar los tokens JWT
SECRET_KEY = "tu_clave_secreta"

# Algoritmo utilizado para cifrar y verificar tokens
ALGORITHM = "HS256"

# Tiempo de expiración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Configura el esquema de autenticación Bearer
security = HTTPBearer()


# Función para generar un token JWT
def create_access_token(data: dict):

    # Crea una copia de los datos recibidos
    to_encode = data.copy()

    # Define la fecha y hora de expiración del token
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Agrega la fecha de expiración al payload
    to_encode.update({"exp": expire})

    # Genera y retorna el token JWT firmado
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Función para verificar y decodificar un token JWT
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    # Obtiene el token enviado en el encabezado Authorization
    token = credentials.credentials

    try:

        # Decodifica y valida el token JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Retorna el contenido del token
        return payload

    # Si el token es inválido o expiró
    except JWTError:

        # Genera error de autenticación
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )