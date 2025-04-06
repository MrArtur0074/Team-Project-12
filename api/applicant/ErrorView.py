from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Applicant, Error
from .serializers import ErrorSerializer


class ErrorListAPIView(APIView):
    def get(self, request):
        errors = Error.objects.all().order_by('-created_at')
        serializer = ErrorSerializer(errors, many=True)
        return Response(serializer.data)

class ErrorDetailAPIView(APIView):
    def get(self, request, pk):
        error = get_object_or_404(Error, pk=pk)
        serializer = ErrorSerializer(error)
        return Response(serializer.data)

    def delete(self, request, pk):
        error = get_object_or_404(Error, pk=pk)
        error.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        error = get_object_or_404(Error, pk=pk)
        data = request.data

        new_applicant = Applicant(
            applicant_id=data.get("applicant_id", error.applicant_id),
            name=data.get("name"),
            surname=data.get("surname"),
            phone_num=data.get("phone_num"),
            school=data.get("school"),
            base64=error.base64,
            attempt=0,
            status=data.get("status", "active"),
        )
        new_applicant.set_array(error.get_array())
        new_applicant.save()
        error.delete()

        return Response({"message": "Переведено в Applicant"}, status=status.HTTP_201_CREATED)

