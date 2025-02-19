from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Base64ImageValidator
from .models import NumpyArrayModel
from mainapp.func import getEmbeddingFromBase64, checkEquality
import numpy as np

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Base64ImageValidator(data=request.data)
        if serializer.is_valid():
            base64_image = serializer.validated_data["image"]
            embedding = getEmbeddingFromBase64(base64_image)

            if not isinstance(embedding, np.ndarray):
                return Response({"error": str(embedding)}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем существующие эмбеддинги
            existing_faces = NumpyArrayModel.objects.all()
            embeddings_dict = {face.image_name: face.get_array() for face in existing_faces}

            # Проверяем, есть ли совпадение
            matched_face = checkEquality(embeddings_dict, embedding)

            if matched_face:
                return Response({"error": "Лицо уже существует в базе"}, status=status.HTTP_400_BAD_REQUEST)

            # Если лицо уникальное — сохраняем
            new_face = NumpyArrayModel(
                image_name=f"face_{len(existing_faces) + 1}",
                base64=base64_image
            )
            new_face.set_array(embedding)
            new_face.save()

            return Response({"message": "Новое лицо добавлено"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
