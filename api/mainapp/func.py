import base64
import io
import cv2
import numpy
from PIL import Image
import numpy as np
from imgbeddings import imgbeddings
from scipy.spatial.distance import cosine





def getEmbeddingFromBase64(base64_string: str):
    try:
        """Декодирует Base64 строку в изображение PIL."""
        alg = "photoscan/files/haarcascade_frontalface_default.xml"
        haar_cascade = cv2.CascadeClassifier(alg)
        ibed = imgbeddings()
        image_data = Image.open(io.BytesIO(base64.b64decode(base64_string)))
        image_np = np.array(image_data)
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        faces = haar_cascade.detectMultiScale(
            image=gray_image, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100)
        )
        if len(faces) > 1:
            return "More than 1 face"
        elif len(faces) == 0:
            return "No faces detected"
        embedding = np.array(ibed.to_embeddings(image_data)).ravel()
        return embedding
    except Exception as e:
        return e


def checkEquality(embeddings: dict, targetEmbedding: np.ndarray):
    if not embeddings:  # Если база пустая, возвращаем None (новое лицо)
        return None

    threshold = 0.23
    closest_distance = float("inf")  # Инициализируем большим значением
    closest_face = None

    for file, embedding in embeddings.items():
        if embedding.shape == targetEmbedding.shape:
            distance = cosine(targetEmbedding, embedding)
            if distance < closest_distance:  # Обновляем ближайшее расстояние
                closest_distance = distance
                closest_face = file

    # Проверяем, попадает ли ближайшее расстояние в порог
    if closest_distance < threshold:
        return closest_face

    return None  # Если лицо уникальное



import base64

def encode_image_to_base64(image_path):
    """Читает изображение и кодирует его в Base64"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None

image_path = "../files/faces/ryan/ryan_cap.jpg"
base64_string = encode_image_to_base64(image_path)

if base64_string:
    print("Base64 код изображения:")
    print(base64_string)
