from rest_framework import serializers
from .models import Exam, ExamResult

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'date', 'english_max', 'english_min', 'math_max', 'math_min']

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'exam', 'applicant', 'english', 'math']
