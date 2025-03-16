from django.urls import path
from .views import ExamListCreateAPIView, ExamResultListCreateAPIView, ExamDetailAPIView

urlpatterns = [
    path('exam-result/', ExamResultListCreateAPIView.as_view()),
    path('exams/', ExamListCreateAPIView.as_view()),
    path('exam-detail/<int:pk>/', ExamDetailAPIView.as_view(), name='exam-detail')
]