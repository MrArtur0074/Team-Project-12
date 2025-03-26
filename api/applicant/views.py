import pickle
import datetime
import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .num_rec import *
from .serializers import Base64ImageValidator
from .models import Applicant, Error
from exam.models import Exam, ExamResult
from .face import getEmbeddingFromBase64, checkEquality


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = Base64ImageValidator(data=request.data)
            if serializer.is_valid():
                base64_image = serializer.validated_data["image"]
                applicant_id = request.data.get("applicant_id")
                embedding = getEmbeddingFromBase64(base64_image)

                if not applicant_id:
                    applicant_id = extract_number_from_base64(base64_image)


                if not applicant_id or not applicant_id.isdigit():
                    Error.objects.create(
                        applicant_id=0,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Не удалось определить ID студента"
                    )
                    return Response({"error": "Не удалось определить ID студента"}, status=status.HTTP_400_BAD_REQUEST)

                if Applicant.objects.filter(applicant_id=applicant_id).exists():
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Студент с таким ID уже зарегистрирован"
                    )
                    return Response({"error": "Студент с таким ID уже зарегистрирован"}, status=status.HTTP_400_BAD_REQUEST)


                if not isinstance(embedding, np.ndarray):
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Ошибка при распозновании лица"
                    )
                    return Response({"error": "Ошибка при распозновании лица"}, status=status.HTTP_400_BAD_REQUEST)

                existing_faces = Applicant.objects.all()
                embeddings_dict = {face.applicant_id: face.get_array() for face in existing_faces}

                if checkEquality(embeddings_dict, embedding):
                    print(applicant_id, pickle.dumps(embedding))
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Лицо уже существует в базе"
                    )
                    return Response({"error": "Лицо уже существует в базе"}, status=status.HTTP_400_BAD_REQUEST)

                new_face = Applicant(applicant_id=applicant_id, base64=base64_image, array_data=embedding, attempt=0)
                new_face.set_array(embedding)
                new_face.save()

                today = datetime.date.today()
                exam = Exam.objects.filter(date=today).first()

                exam_result_created = False
                exam_message = ""

                if exam:
                    ExamResult.objects.create(exam=exam, applicant=new_face)
                    exam_result_created = True
                else:
                    exam_message = "Экзамен на сегодня не найден"

                response_data = {
                    "message": "Новое лицо добавлено",
                    "exam_result_created": exam_result_created
                }

                if not exam_result_created:
                    response_data["note"] = exam_message

                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Внутренняя ошибка сервера: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)