import pickle
import datetime
import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import Base64ImageValidator
from .models import Applicant, Error
from exam.models import Exam, ExamResult
from .face import getEmbeddingFromBase64, checkEquality


class FileUploadView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            serializer = Base64ImageValidator(data=request.data)
            if serializer.is_valid():
                base64_image = serializer.validated_data["image"]
                applicant_id = request.data.get("applicant_id")
                print(applicant_id)

                if not applicant_id:
                    return Response({"error": "applicant_id is required"}, status=status.HTTP_400_BAD_REQUEST)

                embedding = getEmbeddingFromBase64(base64_image)
                print("Embedding создан:", type(embedding),
                      embedding.shape if isinstance(embedding, np.ndarray) else None)

                if not isinstance(embedding, np.ndarray):
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Ошибка при создании эмбеддинга"
                    )
                    return Response({"error": "Ошибка при создании эмбеддинга"}, status=status.HTTP_400_BAD_REQUEST)

                existing_faces = Applicant.objects.all()
                embeddings_dict = {face.applicant_id: face.get_array() for face in existing_faces}

                if checkEquality(embeddings_dict, embedding):
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Лицо уже существует в базе"
                    )
                    return Response({"error": "Лицо уже существует в базе"}, status=status.HTTP_400_BAD_REQUEST)

                # Создаем нового Applicant
                new_face = Applicant(applicant_id=applicant_id, base64=base64_image, array_data=embedding, attempt=0)
                new_face.set_array(embedding)
                new_face.save()

                # Ищем экзамен на текущую дату
                today = datetime.date.today()
                exam = Exam.objects.filter(date=today).first()

                exam_result_created = False
                exam_message = ""

                if exam:
                    ExamResult.objects.create(exam=exam, applicant=new_face)
                    exam_result_created = True
                else:
                    exam_message = "Exam not found"

                response_data = {
                    "message": "Новое лицо добавлено",
                    "exam_result_created": exam_result_created
                }

                if not exam_result_created:
                    response_data["note"] = exam_message

                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Внутренняя ошибка сервера{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
