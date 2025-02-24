import base64
import io
import dlib
import numpy as np
import cv2
from PIL import Image
from scipy.spatial.distance import cosine

# Загрузка модели dlib
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")


def getEmbeddingFromBase64(base64_string: str):
    try:
        # Декодируем изображение
        image_data = Image.open(io.BytesIO(base64.b64decode(base64_string)))
        image_np = np.array(image_data)

        # Преобразуем изображение в оттенки серого
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        # Обнаружение лиц
        faces = face_detector(gray_image)

        if len(faces) > 1:
            return "More than 1 face"
        elif len(faces) == 0:
            return "No faces detected"

        # Извлечение признаков лица
        shape = shape_predictor(gray_image, faces[0])
        face_embedding = np.array(face_rec_model.compute_face_descriptor(image_np, shape))

        return face_embedding
    except Exception as e:
        return str(e)


def checkEquality(embeddings: dict, target_embedding: np.ndarray, threshold=0.6):
    if not embeddings:
        return None  # База данных пуста, значит лицо новое

    closest_distance = float("inf")
    closest_face = None

    for file, embedding in embeddings.items():
        if embedding.shape == target_embedding.shape:
            distance = cosine(target_embedding, embedding)
            if distance < closest_distance:
                closest_distance = distance
                closest_face = file

    if closest_distance < threshold:
        return closest_face  # Лицо найдено в базе

    return None  # Лицо уникальное
