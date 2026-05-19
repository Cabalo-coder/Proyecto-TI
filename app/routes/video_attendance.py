import os
import tempfile
import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.services.attendance_service import mark_attendance
from app.services.face_recognition_service import recognize_face_with_score
from app.utils.face_utils import generate_multiple_descriptors

# Inicialización del router de FastAPI para el módulo de video
router = APIRouter(prefix="/video", tags=["Video Recognition"])


def build_confidence(distance: float, threshold: float) -> float:
    """Calcula el porcentaje de confianza basado en la distancia y un umbral.

    A menor distancia (más similitud), mayor es el porcentaje de confianza.

    Args:
        distance (float): Distancia matemática devuelta por el modelo facial.
        threshold (float): Umbral límite para validar la coincidencia.

    Returns:
        float: Porcentaje de confianza redondeado a 2 decimales en un rango de
          0.0 a 100.0.
    """
    if distance is None or not threshold:
        return 0.0

    # Calcula la relación inversa; si distancia es 0, el ratio es 1 (100% confianza)
    ratio = 1 - (distance / threshold)
    # Restringe el valor estrictamente entre el rango de 0.0 y 1.0
    bounded = max(0.0, min(1.0, ratio))

    return round(bounded * 100, 2)


@router.post("/recognize")
def recognize_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Endpoint HTTP POST para procesar un archivo de video, reconocer rostros de

    estudiantes y registrar su asistencia de manera automática.

    - Lee el video de forma optimizada (procesando 1 de cada 5 frames).
    - Reduce la resolución a la mitad para acelerar el procesamiento.
    - Compara los rostros detectados con los registros de la base de datos.
    - Evita registros duplicados y falsos positivos mediante filtros de
    confianza.

    Args:
        file (UploadFile): Archivo de video enviado por el cliente (.mp4, .avi,
          etc.).
        db (Session): Sesión de la base de datos inyectada por SQLAlchemy.

    Returns:
        dict: Resumen estadístico del procesamiento y lista de alumnos cuya
        asistencia fue marcada.
    """

    # =========================================================================
    # 1. GESTIÓN Y GUARDADO DE ARCHIVO TEMPORAL
    # =========================================================================
    # OpenCV requiere un path real en disco para leer el archivo de video de forma eficiente.
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

    temp_video.write(file.file.read())
    temp_video.close()

    # =========================================================================
    # 2. INICIALIZACIÓN DE OPENCV Y ESTRUCTURAS DE CONTROL
    # =========================================================================
    cap = cv2.VideoCapture(temp_video.name)

    # Si OpenCV falla al abrir el contenedor de video, se limpia el disco y se aborta.
    if not cap.isOpened():
        os.unlink(temp_video.name)
        return {"message": "No se pudo abrir el video"}

    frame_count = 0  # Contador total de frames leídos
    recognized_students = set()  # Set para evitar procesar al mismo alumno más de una vez
    detections_counter = {}  # Historial/Contador de apariciones por cada student_id
    results = []  # Payload de salida con los resultados exitosos

    # =========================================================================
    # 3. BUCLE PRINCIPAL DE PROCESAMIENTO DE IMÁGENES (FRAMES)
    # =========================================================================
    while True:
        ret, frame = cap.read()

        # Si no hay más frames disponibles o el video terminó, se rompe el ciclo
        if not ret:
            break

        # Reducción de escala (50% en ancho y alto) para aliviar la carga computacional
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame_count += 1

        # FILTRO TEMPORAL: Solo se analiza un frame cada 5 iteraciones (Ahorro del 80% de procesamiento)
        if frame_count % 5 != 0:
            continue

        try:
            # =================================================================
            # 4. EXTRACCIÓN BIOMÉTRICA DE ROSTROS
            # =================================================================
            # Conversión del frame crudo de OpenCV a bytes JPG en memoria comprimida
            _, buffer = cv2.imencode(".jpg", frame)
            image_bytes = buffer.tobytes()

            # Extracción de descriptores vectoriales (embeddings) de todos los rostros en el frame
            descriptors = generate_multiple_descriptors(image_bytes)

            if not descriptors:
                continue

            # =================================================================
            # 5. RECONOCIMIENTO INDIVIDUAL Y VALIDACIÓN DE NEGOCIO
            # =================================================================
            for descriptor in descriptors:
                # Búsqueda de coincidencia del embedding en la base de datos
                result = recognize_face_with_score(db, descriptor)

                student = result["student"]
                distance = result["distance"]
                threshold = result["threshold"]

                # Umbral local estricto asignado para la analítica de este video
                VIDEO_THRESHOLD = 0.75
                confidence = build_confidence(distance, VIDEO_THRESHOLD)

                # Logs de depuración en consola para monitorear el comportamiento del modelo
                print("====================")
                print(f"Distance: {distance}")
                print(f"Threshold: {threshold}")
                print(f"Student: {student}")

                # Filtro 1: Si no se mapeó ningún estudiante en la base de datos, se ignora
                if not student:
                    continue

                # Filtro 2: Validación de umbral de confianza mínimo (Corta rostros dudosos)
                if confidence < 45:
                    continue

                student_id = student.student_id

                # Incrementa el contador de detecciones válidas para este alumno específico
                detections_counter[student_id] = (
                    detections_counter.get(student_id, 0) + 1
                )

                # Filtro 3: Control de frecuencia. El usuario debe aparecer al menos una vez (siempre pasa por ser < 1)
                # NOTA: Si requieres que aparezca mínimo 2 veces, cambia el operador a: < 2
                if detections_counter[student_id] < 1:
                    continue

                # Filtro 4: Anti-duplicados. Si el alumno ya fue registrado en este video, se salta.
                if student_id in recognized_students:
                    continue

                # Bloqueo del estudiante para congelar futuras inserciones redundantes
                recognized_students.add(student_id)

                # =================================================================
                # 6. PERSISTENCIA DE ASISTENCIA Y PASO AL REPORTE
                # =================================================================
                attendance = mark_attendance(db, student_id)

                results.append(
                    {
                        "student_id": student.student_id,
                        "name": f"{student.first_name} {student.last_name}",
                        "confidence": confidence,
                        "distance": distance,
                        "attendance": attendance,
                    }
                )

        except Exception as e:
            # Captura de errores por frame para que fallos aislados no tumben todo el procesamiento del video
            print(f"Error procesando frame {frame_count}: {e}")

    # =========================================================================
    # 7. CIERRE Y LIBERACIÓN DE RECURSOS DEL SISTEMA
    # =========================================================================
    cap.release()  # Libera el puntero del video en OpenCV
    os.unlink(temp_video.name)  # Elimina físicamente el archivo .mp4 temporal del disco

    # =========================================================================
    # 8. RESPUESTA FINAL API
    # =========================================================================
    return {
        "message": "Video procesado correctamente",
        "frames_processed": frame_count,
        "students_recognized": len(results),
        "results": results,
    }