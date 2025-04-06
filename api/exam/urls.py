from django.urls import path
from .views import ExamListCreateAPIView, ExamResultListCreateAPIView, ExamDetailAPIView, AddPoints

urlpatterns = [
    path('exam-result/', ExamResultListCreateAPIView.as_view()),
    path('exams/', ExamListCreateAPIView.as_view()),
    path('exam-detail/<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail'),
    path('exam-marks/<int:pk>/', AddPoints.as_view())
]