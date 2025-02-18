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


def checkEquality(embeddings : dict, targetEmbedding : numpy.ndarray):
    if not imgbeddings:
        return None
    threshold = 0.23
    closest_distance = 0
    closest_face = None
    for file, embedding in embeddings.items():
        print(type(embedding))
        if embedding.shape == targetEmbedding.shape:
            distance = cosine(targetEmbedding, embedding)
            if distance < closest_distance and closest_distance < threshold:
                closest_face = file
                closest_distance = distance
    return closest_face


import base64
from io import BytesIO
from PIL import Image


def image_to_base64(image_path):
    """Конвертирует изображение в base64-строку."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def base64_to_image(base64_string):
    """Декодирует base64-строку в изображение."""
    decoded_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(decoded_data))
    image.verify()  # Проверяем, является ли это изображением
    return image


if __name__ == '__main__':
    image_path = "faces/template/img_2.png"
    base64_string = image_to_base64(image_path)

    try:
        decoded_image = base64_to_image(base64_string)
        # print("✅ Изображение успешно закодировано и декодировано!")
    except Exception as e:
        print("❌ Ошибка при декодировании:", e)
    finally:
        print(base64_string)
