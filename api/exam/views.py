from rest_framework.permissions import IsAdminUser
from .models import Exam, ExamResult
from applicant.models import Applicant
from .serializers import ExamSerializer, ExamResultSerializer
import pandas as pd
import base64
from io import BytesIO
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class ExamListCreateAPIView(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        serializer = ExamSerializer(exam)

        exam_results = ExamResult.objects.filter(exam=exam)
        results_serializer = ExamResultSerializer(exam_results, many=True)

        return Response({
            "exam": serializer.data,
            "results": results_serializer.data
        })

    def delete(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        exam.delete()
        return Response({"message": "Exam deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ExamResultListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        exam_id = request.data.get('exam_id')
        applicant_id = request.data.get('applicant_id')

        exam = get_object_or_404(Exam, id=exam_id)
        applicant = get_object_or_404(Applicant, id=applicant_id)
        exam_result = ExamResult.objects.create(exam=exam, applicant=applicant)

        return Response(ExamResultSerializer(exam_result).data, status=status.HTTP_201_CREATED)


class AddPoints(APIView):

    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        exam_results = ExamResult.objects.filter(exam=exam)
        base64_file = request.data.get("file")

        if not base64_file:
            return Response({"error": "Файл не предоставлен"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = base64.b64decode(base64_file)
            excel_data = pd.read_excel(BytesIO(decoded_file))

            missing_applicants = []
            empty_records = []

            for _, row in excel_data.iterrows():
                applicant_id = row["student_id"]
                english_score = row["english"]
                math_score = row["math"]

                try:
                    exam_result = ExamResult.objects.get(exam=exam, applicant__applicant_id=applicant_id)
                    exam_result.english = english_score
                    exam_result.math = math_score
                    exam_result.passed = (
                        english_score >= exam.english_min and math_score >= exam.math_min
                    )
                    exam_result.save()

                    applicant = exam_result.applicant
                    applicant.status = "pass" if exam_result.passed else "fail"
                    applicant.save()

                except ExamResult.DoesNotExist:
                    missing_applicants.append(applicant_id)

                except Exception:
                    empty_records.append(applicant_id)

            response_data = {"message": "Оценки обновлены"}
            if missing_applicants:
                response_data["missing_applicants"] = missing_applicants
            if empty_records:
                response_data["empty_records"] = empty_records

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Ошибка обработки файла: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


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

            for _, row in excel_data.iterrows():
                applicant_id = row["student_id"]
                name = row["name"]
                surname = row["surname"]
                phone_num = row["phone_num"]
                school = row["school"]

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

            response_data = {"message": "Данные студентов обновлены"}
            if missing_students:
                response_data["missing_students"] = missing_students
            if empty_records:
                response_data["empty_records"] = empty_records

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Ошибка обработки файла: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
