from django.urls import path
from .views import UploadAndConvertView, DownloadConvertedZip

urlpatterns = [
    path('upload/', UploadAndConvertView.as_view(), name='upload_and_convert'),
    path('download/<str:job_id>/', DownloadConvertedZip.as_view(), name='download_converted'),
]
