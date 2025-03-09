import pickle

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Base64ImageValidator
from .models import Applicant, Error
from applicant.face import getEmbeddingFromBase64, checkEquality
import numpy as np
import logging

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = Base64ImageValidator(data=request.data)
            if serializer.is_valid():
                base64_image = serializer.validated_data["image"]
                applicant_id = request.data.get("applicant_id")
                if not applicant_id:
                    return Response({"error": "applicant_id is required"}, status=status.HTTP_400_BAD_REQUEST)

                embedding = getEmbeddingFromBase64(base64_image)

                if not isinstance(embedding, np.ndarray):
                    Error.objects.create(applicant_id=applicant_id, base64=base64_image, array_data=pickle.dumps(embedding), error="Ошибка при создании эмбеддинга")
                    return Response({"error": "Ошибка при создании эмбеддинга"}, status=status.HTTP_400_BAD_REQUEST)

                existing_faces = Applicant.objects.all()
                embeddings_dict = {face.applicant_id: face.get_array() for face in existing_faces}

                if checkEquality(embeddings_dict, embedding):
                    Error.objects.create(applicant_id=applicant_id, base64=base64_image, array_data=pickle.dumps(embedding), error="Лицо уже существует в базе")
                    return Response({"error": "Лицо уже существует в базе"}, status=status.HTTP_400_BAD_REQUEST)

                new_face = Applicant(applicant_id=applicant_id, base64=base64_image, embedding=embedding, attempt=0)
                new_face.set_array(embedding)
                new_face.save()

                return Response({"message": "Новое лицо добавлено"}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
