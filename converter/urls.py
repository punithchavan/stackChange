from django.urls import path
from .views import ConversionJobCreateView, ConversionJobDetailView, ConversionJobListView

urlpatterns = [
    path('api/convert/', ConversionJobCreateView.as_view(), name='job-create'),
    path('api/jobs/<uuid:id>/', ConversionJobDetailView.as_view(), name='job-detail'),
    path('api/jobs/', ConversionJobListView.as_view(), name='job-list'),
]
