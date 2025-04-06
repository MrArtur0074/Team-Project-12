from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Applicant, BlackList
from .serializers import BlackListSerializer


class ApplicantToBlackListAPIView(APIView):
    def post(self, request, pk):
        applicant = get_object_or_404(Applicant, applicant_id=pk)

        blacklisted = BlackList(
            applicant_id=applicant.applicant_id,
            name=applicant.name,
            surname=applicant.surname,
            phone_num=applicant.phone_num,
            school=applicant.school,
            base64=applicant.base64
        )
        blacklisted.set_array(applicant.get_array())
        blacklisted.save()
        applicant.delete()

        return Response({"message": "Студент перенесён в BlackList"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        applicant = get_object_or_404(Applicant, applicant_id=pk)
        applicant.delete()
        return Response({"message": "Студент удалён"}, status=status.HTTP_204_NO_CONTENT)

class BlackListListAPIView(APIView):
    def get(self, request):
        blacklisted = BlackList.objects.all()
        serializer = BlackListSerializer(blacklisted, many=True)
        return Response(serializer.data)

class BlackListDetailAPIView(APIView):
    def get(self, request, pk):
        person = get_object_or_404(BlackList, applicant_id=pk)
        serializer = BlackListSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk):
        person = get_object_or_404(BlackList, applicant_id=pk)
        serializer = BlackListSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlackListToApplicantAPIView(APIView):
    def post(self, request, pk):
        person = get_object_or_404(BlackList, applicant_id=pk)
        data = request.data

        applicant = Applicant(
            applicant_id=person.applicant_id,
            name=data.get("name", person.name),
            surname=data.get("surname", person.surname),
            phone_num=data.get("phone_num", person.phone_num),
            school=data.get("school", person.school),
            base64=person.base64,
            attempt=0,
            status=data.get("status", "restored"),
        )
        applicant.set_array(person.get_array())
        applicant.save()
        person.delete()

        return Response({"message": "Переведено обратно в Applicant"}, status=status.HTTP_201_CREATED)
