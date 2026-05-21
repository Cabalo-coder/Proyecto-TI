# Importa herramientas necesarias de FastAPI
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

# Importa Session para manejar consultas a la base de datos
from sqlalchemy.orm import Session

# Importa uuid para generar nombres únicos de archivos
import uuid

# Importa el modelo Face
from app.models.face import Face

# Importa el modelo Student
from app.models.student import Student

# Importa el modelo Section
from app.models.class_section import Section

# Importa el modelo Course
from app.models.course import Course

# Importa la dependencia para obtener la conexión a la base de datos
from app.dependencies.database import get_db

# Importa la dependencia para obtener el docente autenticado
from app.dependencies.auth import get_current_teacher

# Importa la conexión configurada con Supabase
from app.config.supabase import supabase

# Importa la función encargada de generar el descriptor facial
from app.utils.face_utils import generate_face_descriptor


# Crea el router para las rutas relacionadas con rostros
router = APIRouter(
    prefix="/faces",   # Prefijo principal de las rutas
    tags=["Faces"]     # Etiqueta para documentación automática
)


# Ruta para subir y registrar un rostro
@router.post("/upload")
def upload_face(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):

    # Busca al estudiante en la base de datos
    student = db.query(Student).filter(
        Student.student_id == student_id
    ).first()

    # Si el estudiante no existe, genera error
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    # Busca la sección asociada al estudiante
    section = db.query(Section).filter(
        Section.section_id == student.section_id
    ).first()

    # Si la sección no existe, genera error
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Sección no encontrada"
        )

    # Busca el curso asociado a la sección
    course = db.query(Course).filter(
        Course.course_id == section.course_id
    ).first()

    # Si el curso no existe, genera error
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    # Verifica que el curso pertenezca al docente autenticado
    if course.teacher_id != current_teacher["id"]:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    # Obtiene la extensión del archivo enviado
    file_extension = file.filename.split(".")[-1]

    # Genera un nombre único para evitar archivos duplicados
    file_name = f"{uuid.uuid4()}.{file_extension}"

    # Define la ruta del archivo en Supabase Storage
    file_path = file_name

    # Lee el contenido del archivo en bytes
    file_bytes = file.file.read()

    # Genera el descriptor facial utilizando reconocimiento facial
    descriptor = generate_face_descriptor(file_bytes)

    # Si no se detecta un rostro, genera error
    if descriptor is None:
        raise HTTPException(
            status_code=400,
            detail="No se detectó ningún rostro en la imagen"
        )

    # Convierte el descriptor a lista si proviene de un numpy array
    descriptor_list = (
        descriptor.tolist()
        if hasattr(descriptor, "tolist")
        else descriptor
    )

    # Sube la imagen al bucket "faces" en Supabase Storage
    supabase.storage.from_("faces").upload(
        file_path,
        file_bytes
    )

    # Obtiene la URL pública de la imagen almacenada
    image_url = supabase.storage.from_("faces").get_public_url(file_path)

    # Crea un nuevo registro facial en la base de datos
    new_face = Face(
        student_id=student_id,
        image_url=image_url,
        facial_descriptor=descriptor_list
    )

    # Guarda el rostro en la base de datos
    db.add(new_face)
    db.commit()
    db.refresh(new_face)

    # Retorna mensaje de éxito y datos registrados
    return {
        "message": "Imagen subida correctamente",
        "image_url": image_url,
        "face_id": new_face.face_id
    }