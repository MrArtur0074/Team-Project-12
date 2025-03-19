import base64
import cv2
import numpy as np
from paddleocr import PaddleOCR
from ultralytics import YOLO


def extract_number_from_base64(base64_string):
    image_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Ошибка: не удалось декодировать изображение")

    model = YOLO("files/best.pt")
    results = model.predict(image, conf=0.5)

    ocr = PaddleOCR(lang="en")
    result = ocr.ocr(image, cls=False)

    recognized_numbers = []

    for line in result:
        for word_info in line:
            text, confidence = word_info[1]
            recognized_numbers.append((text, confidence))

    if recognized_numbers:
        best_match = max(recognized_numbers, key=lambda x: x[1])
        return best_match[0]
    else:
        return "Не удалось распознать число"
