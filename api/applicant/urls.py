from django.urls import path

from .BlackListView import ApplicantToBlackListAPIView, BlackListListAPIView, BlackListDetailAPIView, BlackListToApplicantAPIView
from .ErrorView import ErrorListAPIView, ErrorDetailAPIView
from .views import FileUploadView, AddStudentsData
from .ApplicantView import ApplicantListAPIView, ApplicantDetailAPIView, ApplicantSearchAPIView
from .DatabaseView import ExportDataByYearView, ClearAllDataView, ClearDataByYearView



urlpatterns = [
    path('applicants/', ApplicantListAPIView.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantDetailAPIView.as_view(), name='applicant-detail'),
    path('applicants/search/', ApplicantSearchAPIView.as_view(), name='applicant-search'),
    path('applicants/upload/', FileUploadView.as_view(), name='file-upload'),
    path('applicants/data/', AddStudentsData.as_view(), name='add-students-data'),
    path('applicants/<int:pk>/blacklist/', ApplicantToBlackListAPIView.as_view(), name='applicant-to-blacklist'),

    path('errors/', ErrorListAPIView.as_view(), name='error-list'),
    path('errors/<int:pk>/', ErrorDetailAPIView.as_view(), name='error-detail'),

    path('blacklist/', BlackListListAPIView.as_view(), name='blacklist-list'),
    path('blacklist/<int:pk>/', BlackListDetailAPIView.as_view(), name='blacklist-detail'),
    path('blacklist/<int:pk>/restore/', BlackListToApplicantAPIView.as_view(), name='blacklist-to-applicant'),

    path('export/<int:pk>/', ExportDataByYearView.as_view(), name='export-data-by-year'),
    path('clear/all/', ClearAllDataView.as_view(), name='clear-all-data'),
    path('clear/year/<int:pk>/', ClearDataByYearView.as_view(), name='clear-year-data'),

]
