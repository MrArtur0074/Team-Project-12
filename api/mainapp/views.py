from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Base64ImageValidator
from .models import NumpyArrayModel
from mainapp.func import getEmbeddingFromBase64, checkEquality
import numpy as np

import logging

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = Base64ImageValidator(data=request.data)
            if serializer.is_valid():
                base64_image = serializer.validated_data["image"]
                embedding = getEmbeddingFromBase64(base64_image)

                if not isinstance(embedding, np.ndarray):
                    error_message = f"Ошибка при создании эмбеддинга: {embedding}"
                    print(error_message)  # Лог в консоль
                    return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

                # Получаем существующие эмбеддинги
                existing_faces = NumpyArrayModel.objects.all()
                embeddings_dict = {face.image_name: face.get_array() for face in existing_faces}

                # Проверяем, есть ли совпадение
                matched_face = checkEquality(embeddings_dict, embedding)

                if matched_face:
                    error_message = "Лицо уже существует в базе"
                    print(f"Ошибка: {error_message}")  # Лог в консоль
                    return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

                # Если лицо уникальное — сохраняем
                new_face = NumpyArrayModel(
                    image_name=f"face_{len(existing_faces) + 1}",
                    base64=base64_image
                )
                new_face.set_array(embedding)
                new_face.save()

                print("✅ Новое лицо успешно добавлено")  # Лог успеха
                return Response({"message": "Новое лицо добавлено"}, status=status.HTTP_201_CREATED)

            print(f"Ошибка валидации: {serializer.errors}")  # Лог ошибок валидации
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"❌ Ошибка обработки запроса: {str(e)}")  # Лог исключений
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
