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

class BestResult(models.Model):
    exam = models.ForeignKey(ExamResult, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)