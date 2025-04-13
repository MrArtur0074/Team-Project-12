import base64
import pandas as pd
from io import BytesIO
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Applicant, BlackList, Error
from exam.models import Exam, ExamResult


class ExportDataByYearView(APIView):
    def get(self, request, pk):
        try:
            year = int(pk)

            # Получаем студентов за указанный год
            applicants = Applicant.objects.filter(created_at__year=year)
            applicant_data = [{
                "applicant_id": a.applicant_id,
                "name": a.name,
                "surname": a.surname,
                "phone_num": a.phone_num,
                "school": a.school,
                "status": a.status,
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M"),
            } for a in applicants]
            df_applicants = pd.DataFrame(applicant_data)

            # Создание Excel-файла в памяти
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Студенты
                df_applicants.to_excel(writer, sheet_name="Applicants", index=False)

                # Экзамены за год
                exams = Exam.objects.filter(date__year=year)
                for exam in exams:
                    results = ExamResult.objects.filter(exam=exam)
                    data = []
                    for result in results:
                        a = result.applicant
                        data.append({
                            "applicant_id": a.applicant_id,
                            "name": a.name,
                            "surname": a.surname,
                            "status": a.status,
                            "score": getattr(result, "score", None),
                        })
                    df_result = pd.DataFrame(data)
                    df_result.to_excel(writer, sheet_name=str(exam.date), index=False)

                writer.close()

            output.seek(0)
            base64_excel = base64.b64encode(output.read()).decode("utf-8")

            return Response({"file_base64": base64_excel}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Ошибка при экспорте данных: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClearAllDataView(APIView):
    def delete(self, request):
        try:
            Applicant.objects.all().delete()
            BlackList.objects.all().delete()
            Error.objects.all().delete()
            Exam.objects.all().delete()
            ExamResult.objects.all().delete()

            return Response({"message": "Все данные успешно удалены"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Ошибка при удалении данных: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClearDataByYearView(APIView):
    def delete(self, request, pk):
        try:
            year = int(pk)

            # Удаляем по году создания
            Applicant.objects.filter(created_at__year=year).delete()
            BlackList.objects.filter(created_at__year=year).delete()
            Error.objects.filter(created_at__year=year).delete()

            # Удаляем экзамены и результаты по дате
            Exam.objects.filter(date__year=year).delete()
            ExamResult.objects.filter(created_at__year=year).delete()

            return Response({"message": f"Данные за {year} год успешно удалены"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Ошибка при удалении данных: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

