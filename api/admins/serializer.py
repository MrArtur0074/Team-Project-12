from rest_framework import serializers
from admins.models import CustomUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'surname', 'email', 'name', 'confirmation_code', 'password',
                  'password_confirm', 'created_at', 'is_active', 'email_confirmed']

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        confirmation_code = get_random_string(length=4, allowed_chars='0123456789')

        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
            email_confirmed=False,
            confirmation_code=confirmation_code,
        )

        subject = 'Confirmation code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = 'python'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return user


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=4)

    def validate(self, data):
        email = data.get("email")
        confirmation_code = data.get("confirmation_code")

        user = CustomUser.objects.filter(email=email, confirmation_code=confirmation_code).first()
        if not user:
            raise serializers.ValidationError("Invalid email or confirmation code.")
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.email_confirmed:
                raise serializers.ValidationError("Email is not confirmed.")
            if not user.is_active:
                raise serializers.ValidationError("Admin has not approved your account.")
            return super().validate({"username": user.username, "password": password})

        raise serializers.ValidationError("Invalid credentials")

class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_active', 'email_confirmed']
