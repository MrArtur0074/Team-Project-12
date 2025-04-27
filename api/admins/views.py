from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from admins.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered. Please confirm your email.",
                "id": user.id,
                "email": user.email,
                "email_confirmed": user.email_confirmed,
                "is_active": user.is_active,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            user.email_confirmed = True
            user.save()
            return Response({"message": "Email confirmed. Awaiting admin approval."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        print(email, password, user)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class AdminApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        if not user.email_confirmed:
            return Response({"error": "User has not confirmed their email."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"message": "User approved."}, status=status.HTTP_200_OK)


class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        approved_users = CustomUser.objects.filter(is_active=True)
        pending_users = CustomUser.objects.filter(is_active=False, email_confirmed=True)
        unconfirmed_users = CustomUser.objects.filter(email_confirmed=False)

        return Response({
            "approved_users": AdminUserListSerializer(approved_users, many=True).data,
            "pending_users": AdminUserListSerializer(pending_users, many=True).data,
            "unconfirmed_users": AdminUserListSerializer(unconfirmed_users, many=True).data,
        }, status=status.HTTP_200_OK)


class AdminRejectUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return Response({"message": "User rejected and removed from database."}, status=status.HTTP_200_OK)
