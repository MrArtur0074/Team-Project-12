import base64
import cv2
import numpy as np
import os
from ultralytics import YOLO
from paddleocr import PaddleOCR


def extract_and_recognize_number(base64_image: str) -> str:
    image_data = base64.b64decode(base64_image)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    model = YOLO("best.pt")

    results = model.predict(image, conf=0.5)

    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cropped_img = image[y1:y2, x1:x2]

            temp_path = "temp_digit.jpg"
            cv2.imwrite(temp_path, cropped_img)

            ocr = PaddleOCR(lang="en")

            result = ocr.ocr(temp_path, cls=False)

            os.remove(temp_path)

            for line in result:
                for word_info in line:
                    text, confidence = word_info[1]
                    return text

    return None
