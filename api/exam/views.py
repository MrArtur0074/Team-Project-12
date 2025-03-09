from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Exam, ExamResult
from applicant.models import Applicant
from .serializers import ExamSerializer, ExamResultSerializer


class ExamListCreateAPIView(APIView):

    # todo
    # split get and post

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

    # todo
    # split get and post

    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        serializer = ExamSerializer(exam)

        # todo
        # add all results of this exam

        return Response(serializer.data)

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

    def post(self, request):

        # todo
        # get xlsx files and updating points of applicants

        return Response(request)