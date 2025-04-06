import base64
import io
import cv2
import dlib
import numpy as np
from PIL import Image
import traceback

def getEmbeddingFromBase64(base64_string: str):
    try:
        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor("files/shape_predictor_5_face_landmarks.dat")
        facerec = dlib.face_recognition_model_v1("files/dlib_face_recognition_resnet_model_v1.dat")

        image_data = Image.open(io.BytesIO(base64.b64decode(base64_string)))
        image_np = np.array(image_data)
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        faces = detector(gray_image)

        if len(faces) > 1:
            return "More than 1 face"
        elif len(faces) == 0:
            return "No faces detected"

        shape = sp(gray_image, faces[0])
        embedding = np.array(facerec.compute_face_descriptor(gray_image, shape))
        return embedding

    except Exception as e:
        print("❌ Ошибка в get_embedding_from_base64:")
        # print(traceback.format_exc())
        return str(e)


def checkEquality(embeddings_dict: dict, embedding: np.ndarray, threshold: float = 0.6):
    if not embeddings_dict:
        return False  # Если база пустая, нет смысла проверять

    similarities = {
        applicant_id: 1 - np.linalg.norm(embedding - emb)
        for applicant_id, emb in embeddings_dict.items()
        if embedding.shape == emb.shape  # Проверяем, что формы совпадают
    }

    if not similarities:
        return False  # Нет совпадающих по форме эмбеддингов

    best_match_id, best_similarity = max(similarities.items(), key=lambda x: x[1])

    if best_similarity >= threshold:
        return best_match_id, f"Похожи ({best_similarity:.2f})"

    return False

def checkEquality2(embeddings_dict, target_embedding, threshold=0.6, return_id=False):
    for applicant_id, embedding in embeddings_dict.items():
        distance = np.linalg.norm(embedding - target_embedding)
        if distance < threshold:
            return applicant_id if return_id else True
    return None if return_id else False
