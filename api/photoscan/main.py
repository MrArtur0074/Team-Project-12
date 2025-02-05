import os
from PIL import Image
from imgbeddings import imgbeddings
import cv2
from scipy.spatial.distance import cosine
import numpy as np

# Haar Cascade для детекции лиц
alg = "files/haarcascade_frontalface_default.xml"
file_path = "faces/template/img.png"
haar_cascade = cv2.CascadeClassifier(alg)

# Чтение и конвертация изображения
image = cv2.imread(file_path, 0)
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Детекция лиц
faces = haar_cascade.detectMultiScale(
    image=gray_image, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100)
)

# Обрезка и сохранение лиц
os.makedirs("faces/result", exist_ok=True)
i = 0
for x, y, w, h in faces:
    cropped_image = image[y:y + h, x:x + w]
    target_file_name = f"faces/result/{i}.jpg"
    cv2.imwrite(target_file_name, cropped_image)
    i += 1

print(f"Количество найденных лиц: {len(faces)}")

# Инициализация модели и получение эмбеддингов
ibed = imgbeddings()
result_embeddings = {}

for file in os.listdir("faces/result/"):
    img_path = f"faces/result/{file}"
    img = Image.open(img_path)

    # Получение эмбеддинга и проверка типа данных
    embedding = np.array(ibed.to_embeddings(img)).ravel()
    result_embeddings[file] = embedding

# Загружаем и обрабатываем лицо для поиска
try:
    img_to_check = Image.open("faces/template/img_4.png")
    target_embedding = np.array(ibed.to_embeddings(img_to_check)).ravel()
except FileNotFoundError:
    print("Файл для сравнения не найден.")
    exit()

# Поиск самого похожего лица
closest_face = None
closest_distance = float("inf")
threshold = 0.2  # Порог для совпадения

for file, embedding in result_embeddings.items():
    # Проверка размеров эмбеддингов перед расчетом
    if embedding.shape == target_embedding.shape:
        distance = cosine(target_embedding, embedding)
        if distance < closest_distance:
            closest_face = file
            closest_distance = distance

# Вывод результата
if closest_distance < threshold:
    print(f"Самое похожее лицо: {closest_face}, расстояние: {closest_distance}")
else:
    print("Ошибка: похожее лицо не найдено.")
