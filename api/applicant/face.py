import base64
import io
import cv2
from PIL import Image
import numpy as np
from imgbeddings import imgbeddings
from scipy.spatial.distance import cosine
import traceback
import os


def getEmbeddingFromBase64(base64_string: str):
    try:
        alg = os.path.abspath("files/files/haarcascade_frontalface_default.xml")
        if not os.path.exists(alg):
            raise FileNotFoundError(f"Файл не найден: {alg}")

        haar_cascade = cv2.CascadeClassifier(alg)
        if haar_cascade.empty():
            raise ValueError("File was damaged")

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
        print("❌ Ошибка в getEmbeddingFromBase64:")
        print(traceback.format_exc())
        return str(e)


def checkEquality(embeddings: dict, targetEmbedding: np.ndarray):
    if not embeddings:
        return None

    threshold = 0.1
    closest_distance = float("inf")
    closest_face = None

    for file, embedding in embeddings.items():
        if embedding.shape == targetEmbedding.shape:
            distance = cosine(targetEmbedding, embedding)
            if distance < closest_distance:
                closest_distance = distance
                closest_face = file

    if closest_distance < threshold:
        return closest_face

    return None
