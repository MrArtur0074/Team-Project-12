
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
import base64
from io import BytesIO
from PIL import Image


class Base64ImageValidator(serializers.Serializer):
    image = serializers.CharField()

    def validate_image(self, value):
        try:
            decoded_data = base64.b64decode(value)
            image = Image.open(BytesIO(decoded_data))
            image.verify()
        except Exception as e:
            print(e)
            raise ValidationError("Image is nor coded with Base64")
        return value
