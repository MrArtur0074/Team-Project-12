from rest_framework.exceptions import ValidationError
import base64
import io
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    """
    Serializer field for handling base64 encoded files.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                decoded_data = base64.b64decode(data)

                # TODO FILE NAME AND TYPE
        #         output_file_path = f'templates/'
        #
        #         with open(output_file_path, 'wb') as output_file:
        #             output_file.write(decoded_data)
        #
        #         return output_file_path
            except (TypeError, ValueError, base64.binascii.Error) as e:
                raise ValidationError("Invalid base64 data")
        # else:
        #     return super().to_internal_value(data)

    # def to_representation(self, value):
    #     if value:
    #         file = io.BytesIO(value.read())
    #         return 'data:{0};base64,{1}'.format('application/octet-stream', base64.b64encode(file.getvalue()).decode())
    #     return ''

class FileUploadSerializer(serializers.Serializer):
    file = Base64FileField()


class SettingsSerializer(serializers.Serializer):

    file = Base64FileField(
        required=True,
        help_text="Файл должен быть картинкой."
    )
