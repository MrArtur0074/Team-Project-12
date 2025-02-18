from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Base64ImageValidator
from .models import NumpyArrayModel
from photoscan.func import getEmbeddingFromBase64, checkEquality
import numpy as np


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Base64ImageValidator(data=request.data)
        if serializer.is_valid():
            base64_image = serializer.validated_data["image"]
            embedding = getEmbeddingFromBase64(base64_image)

            if not isinstance(embedding, np.ndarray):  # Проверяем, что это не строка ошибки
                return Response({"error": str(embedding)}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем все сохраненные лица
            existing_faces = NumpyArrayModel.objects.all()
            embeddings_dict = {face.image_name: face.get_array() for face in existing_faces}

            # Проверяем, есть ли совпадение
            matched_face = checkEquality(embeddings_dict, embedding)

            if matched_face:
                return Response({"match": matched_face}, status=status.HTTP_200_OK)

            # Если в БД пусто или не найдено совпадение — сохраняем новое лицо
            new_face = NumpyArrayModel(
                image_name=f"face_{len(existing_faces) + 1}",
                base64=base64_image
            )
            new_face.set_array(np.array(embedding))
            new_face.save()

            return Response({"message": "New face saved"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
