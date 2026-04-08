import face_recognition
import numpy as np
from PIL import Image
import io


# 🔥 FUNCIÓN ORIGINAL (NO TOCAR - individual)
def generate_face_descriptor(file_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image = np.array(image)
    except:
        return None

    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return None

    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_encodings[0].tolist()


# 🚀 NUEVA FUNCIÓN (GRUPAL)
def generate_multiple_descriptors(file_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image = np.array(image)
    except:
        return []

    # 🔎 detectar todos los rostros
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        return []

    # 🧠 generar encodings para cada rostro
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # 🔥 convertir todos a lista (JSON friendly)
    descriptors = [encoding.tolist() for encoding in face_encodings]

    return descriptors