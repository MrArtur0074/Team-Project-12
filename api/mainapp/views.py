from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer, SettingsSerializer
from .send_request import request

class FileUploadView(APIView):
    serializer_class = SettingsSerializer

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            # TODO SEND AND RECEIVE REQUEST TO AI
            # print(request.data)
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

