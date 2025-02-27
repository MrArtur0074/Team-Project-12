from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from admins.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import transaction


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = request.data
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=data.get('email'),
                surname = data['surname'],
                name=data['name'],
                email=data.get('email'),
                password=data['password'],
                is_active=False,
            )
            confirmation_code = get_random_string(length=4, allowed_chars='0123456789')

            user.confirmation_code = confirmation_code
            user.save()

            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = 'pythonalgorythgame@gmail.com'
            recipient_list = [user.email]

            # Отправка на почту закомментирована
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Вместо отправки на почту возвращаем код в Response
            response_data = {
                'id': user.id,
                'email': user.email,
                'surname' : user.surname,
                'name': user.name,
                'created_at': user.created_at,
                'is_active': user.is_active,
                'confirmation_code': confirmation_code,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomUserLoginView(TokenObtainPairView):
    # permission_classes = [AllowAny]
    pass


class CustomUserTokenRefreshView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access': access_token,
                             'refresh':token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            confirmation_code = get_random_string(4, allowed_chars='0123456789')
            user.confirmation_code = confirmation_code
            user.save()
            confirmation_code = user.confirmation_code
            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = 'pythonalgorythm@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response({'message': 'Confirmation code sent successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            confirmation_code = request.data.get('confirmation_code')
            new_password = request.data.get('new_password')

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if user.confirmation_code != confirmation_code:
                return Response({'error': 'Confirmation code is not match'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'success': 'Password successfully updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            user = request.user
            if not user.check_password(old_password):
                return Response({'error': 'Old password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'success': 'Password is changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ConfirmEmailView(APIView):
    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({"message": "Email confirmed. Awaiting admins approval."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminApprovalView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        with transaction.atomic():
            new_user = User.objects.create_user(
                username=user.email,
                email=user.email,
                password=user.password,
                first_name=user.name,
                last_name=user.surname,
                is_active=True
            )
            new_user.set_password(user.password)
            new_user.save()

            user.delete()

        return Response({"message": "User approved and moved to User table."}, status=status.HTTP_200_OK)


class AdminUserListView(APIView):
    def get(self, request):
        approved_users = CustomUser.objects.filter(is_active=True)
        pending_users = CustomUser.objects.filter(is_active=False)
        approved_serializer = AdminUserListSerializer(approved_users, many=True)
        pending_serializer = AdminUserListSerializer(pending_users, many=True)
        return Response({
            "approved_users": approved_serializer.data,
            "pending_users": pending_serializer.data
        }, status=status.HTTP_200_OK)

class AdminRejectUserView(APIView):
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return Response({"message": "User rejected and removed from database."}, status=status.HTTP_200_OK)
