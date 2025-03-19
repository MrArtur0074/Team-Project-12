import base64
import cv2
import numpy as np
import os
from ultralytics import YOLO
from paddleocr import PaddleOCR


def extract_and_recognize_number(base64_image: str):

    try:
        image_data = base64.b64decode(base64_image)
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            print("⚠ Ошибка декодирования изображения.")
            return None

        model = YOLO("files/best.pt")
        results = model.predict(image, conf=0.5)

        ocr = PaddleOCR(lang="en")

        text = None
        confidence = 0.0
        for r in results:
            for box in r.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cropped_img = image[y1:y2, x1:x2]

                if cropped_img.size == 0:
                    continue

                temp_path = "temp_digit.jpg"
                cv2.imwrite(temp_path, cropped_img)

                result = ocr.ocr(temp_path, cls=False)
                os.remove(temp_path)
                for line in result:
                    for word_info in line:
                        text, confidence = word_info[1]

        if text:
            print(f"✅ Распознанное число: {text}, Уверенность: {confidence:.2f}")
        else:
            print(f"⚠ Число не удалось распознать.")

        return text

    except Exception as e:
        print(f"❌ Ошибка в extract_and_recognize_number: {e}")
        return None


import base64
import cv2
import numpy as np
import os
from ultralytics import YOLO
from paddleocr import PaddleOCR


def extract_number_from_base64(base64_string):
    # Декодируем Base64 в изображение
    image_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Ошибка: не удалось декодировать изображение")

    # Загружаем модель YOLO для обнаружения чисел
    model = YOLO("files/best.pt")
    results = model.predict(image, conf=0.5)

    # Создаем OCR-модель
    ocr = PaddleOCR(lang="en")

    recognized_numbers = []

    for r in results:
        for i, box in enumerate(r.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box)
            cropped_img = image[y1:y2, x1:x2]

            # Сохраняем временное изображение числа
            temp_path = "temp_number.jpg"
            cv2.imwrite(temp_path, cropped_img)
            # Распознаем число с помощью OCR
            result = ocr.ocr(temp_path, cls=False)
            for line in result:
                for word_info in line:
                    text, confidence = word_info[1]
                    recognized_numbers.append((text, confidence))

            os.remove(temp_path)
    if recognized_numbers:
        best_match = max(recognized_numbers, key=lambda x: x[1])
        return best_match[0]
    else:
        return "Не удалось распознать число"
