from django.db import models
from applicant.models import Applicant

class Exam(models.Model):
    date = models.DateField()
    english_max = models.IntegerField()
    english_min = models.IntegerField()
    math_max = models.IntegerField()
    math_min = models.IntegerField()


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    english = models.IntegerField(null=True, blank=True)
    math = models.IntegerField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)

    def get_english(self):
        return self.english

    def set_english(self, value):
        if value is not None and (value < 0 or value > 100):
            raise ValueError("English score must be between 0 and 100")
        self.english = value

    def get_math(self):
        return self.math

    def set_math(self, value):
        if value is not None and (value < 0 or value > 100):
            raise ValueError("Math score must be between 0 and 100")
        self.math = value

    def save(self, *args, **kwargs):
        if not self.pk:
            self.applicant.attempt += 1
            self.applicant.save()
        super().save(*args, **kwargs)
