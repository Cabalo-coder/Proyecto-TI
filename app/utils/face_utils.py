# Importa la librería de reconocimiento facial
import face_recognition

# Importa NumPy para manejo de arreglos y procesamiento de imágenes
import numpy as np

# Importa Image para abrir imágenes con Pillow
from PIL import Image

# Importa io para trabajar con archivos en memoria
import io


# Función para generar el descriptor facial de un único rostro
def generate_face_descriptor(file_bytes: bytes):

    try:
        # Abre la imagen desde bytes
        image = Image.open(io.BytesIO(file_bytes))

        # Convierte la imagen a un arreglo de NumPy
        image = np.array(image)

    # Si ocurre un error al procesar la imagen
    except:
        return None

    # Detecta las ubicaciones de los rostros en la imagen
    face_locations = face_recognition.face_locations(image)

    # Si no se detecta ningún rostro
    if len(face_locations) == 0:
        return None

    # Genera los descriptores faciales de los rostros encontrados
    face_encodings = face_recognition.face_encodings(
        image,
        face_locations
    )

    # Retorna el descriptor del primer rostro encontrado
    # convertido a lista para facilitar almacenamiento en JSON
    return face_encodings[0].tolist()


# Función para generar descriptores faciales de múltiples rostros
def generate_multiple_descriptors(file_bytes: bytes):

    try:
        # Abre la imagen desde bytes
        image = Image.open(io.BytesIO(file_bytes))

        # Convierte la imagen a un arreglo de NumPy
        image = np.array(image)

    # Si ocurre un error al procesar la imagen
    except:
        return []

    # Detecta todos los rostros presentes en la imagen
    face_locations = face_recognition.face_locations(image)

    # Si no se detectan rostros
    if len(face_locations) == 0:
        return []

    # Genera descriptores faciales para cada rostro detectado
    face_encodings = face_recognition.face_encodings(
        image,
        face_locations
    )

    # Convierte todos los descriptores a listas
    # para que puedan almacenarse fácilmente en JSON
    descriptors = [
        encoding.tolist()
        for encoding in face_encodings
    ]

    # Retorna todos los descriptores encontrados
    return descriptors