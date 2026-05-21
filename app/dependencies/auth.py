# Importa herramientas necesarias de FastAPI
from fastapi import Depends, HTTPException

# Importa la función encargada de verificar el token JWT
from app.utils.jwt import verify_token


# Dependencia utilizada para obtener el docente autenticado
def get_current_teacher(
    payload: dict = Depends(verify_token)
):

    # Verifica que el token sea válido
    if payload is None:

        # Genera error si el token es inválido
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    # Retorna la información contenida en el token
    return payload