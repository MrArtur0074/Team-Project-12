from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .face import getEmbeddingFromBase64, checkEquality2
from .models import Applicant, BlackList
from .serializers import ApplicantSerializer
from rest_framework.permissions import AllowAny



class ApplicantListAPIView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)

class ApplicantDetailAPIView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, pk):
        applicant = get_object_or_404(Applicant, applicant_id=pk)
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    def put(self, request, pk):
        applicant = get_object_or_404(Applicant, applicant_id=pk)
        serializer = ApplicantSerializer(applicant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicantSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        search_term = request.data.get("query")
        base64_image = request.data.get("image")

        if search_term:
            applicants = Applicant.objects.filter(
                Q(name__icontains=search_term) |
                Q(surname__icontains=search_term) |
                Q(applicant_id__icontains=search_term)
            )
            serializer = ApplicantSerializer(applicants, many=True)
            return Response(serializer.data)

        elif base64_image:
            try:
                embedding = getEmbeddingFromBase64(base64_image)

                # Проверка BlackList
                blacklisted = BlackList.objects.all()
                blacklist_embeddings = {b.applicant_id: b.get_array() for b in blacklisted}
                matched_black_id = checkEquality2(blacklist_embeddings, embedding)

                if matched_black_id:
                    return Response(
                        {"message": "Пользователь найден в чёрном списке", "blacklist_id": matched_black_id},
                        status=status.HTTP_403_FORBIDDEN
                    )

                applicants = Applicant.objects.all()
                embeddings_dict = {a.applicant_id: a.get_array() for a in applicants}
                matched_id = checkEquality2(embeddings_dict, embedding)

                if matched_id:
                    applicant = Applicant.objects.get(applicant_id=matched_id)
                    serializer = ApplicantSerializer(applicant)
                    return Response(serializer.data)
                else:
                    return Response({"message": "Совпадений не найдено"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Пустой запрос"}, status=status.HTTP_400_BAD_REQUEST)
