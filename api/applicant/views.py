import pickle
import datetime
from io import BytesIO
import pandas as pd
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .num_rec import *
from django.utils import timezone
from .serializers import Base64ImageValidator
from .models import Applicant, Error, BlackList
from exam.models import Exam, ExamResult
from .face import getEmbeddingFromBase64, checkEquality
from rest_framework.permissions import AllowAny, IsAdminUser


class FileUploadView(APIView):
    permission_classes = [AllowAny]

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

                if BlackList.objects.filter(applicant_id=applicant_id).exists():
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Студент находится в черном списке"
                    )
                    return Response({"error": "Студент находится в черном списке"}, status=status.HTTP_400_BAD_REQUEST)

                if not isinstance(embedding, np.ndarray):
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Ошибка при распозновании лица"
                    )
                    return Response({"error": "Ошибка при распозновании лица"}, status=status.HTTP_400_BAD_REQUEST)

                current_year = timezone.now().year

                existing_faces = Applicant.objects.filter(created_at__year=current_year)
                existing_faces_black_list = BlackList.objects.filter(created_at__year=current_year)

                embeddings_dict = {face.applicant_id: face.get_array() for face in existing_faces}
                embeddings_dict_black_list = {face.applicant_id: face.get_array() for face in existing_faces_black_list}

                if checkEquality(embeddings_dict_black_list, embedding):
                    print(applicant_id, pickle.dumps(embedding))
                    Error.objects.create(
                        applicant_id=applicant_id,
                        base64=base64_image,
                        array_data=pickle.dumps(embedding),
                        error="Студент в черном списке"
                    )
                    return Response({"error": "Студент в черном списке"}, status=status.HTTP_400_BAD_REQUEST)

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

class AddStudentsData(APIView):
    def post(self, request):
        base64_file = request.data.get("file")

        if not base64_file:
            return Response({"error": "Файл не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = base64.b64decode(base64_file)
            excel_data = pd.read_excel(BytesIO(decoded_file))

            missing_students = []
            empty_records = []
            found_ids = set()

            for _, row in excel_data.iterrows():
                applicant_id = row["student_id"]
                name = row["name"]
                surname = row["surname"]
                phone_num = row["phone_num"]
                school = row["school"]
                found_ids.add(applicant_id)

                try:
                    applicant = Applicant.objects.get(applicant_id=applicant_id)
                    applicant.name = name
                    applicant.surname = surname
                    applicant.phone_num = phone_num
                    applicant.school = school
                    applicant.save()

                except Applicant.DoesNotExist:
                    missing_students.append(applicant_id)
                except Exception:
                    empty_records.append(applicant_id)

            all_ids = set(Applicant.objects.values_list("applicant_id", flat=True))
            not_in_excel = list(all_ids - found_ids)

            response_data = {"message": "Данные студентов обновлены"}
            if missing_students:
                response_data["missing_students"] = missing_students
            if empty_records:
                response_data["empty_records"] = empty_records
            if not_in_excel:
                response_data["not_in_excel"] = not_in_excel

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Ошибка обработки файла: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)