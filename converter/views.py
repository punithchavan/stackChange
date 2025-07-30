from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import ConversionJob
from .serializers import ConversionJobSerializer
import os
import shutil
from django.conf import settings

class ConversionJobCreateView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        job = ConversionJob.objects.create(input_file=file, status='pending')

        try:
            # Simulate conversion by copying file to output_files
            input_path = job.input_file.path
            ext = os.path.splitext(input_path)[1]
            output_filename = f"{job.id}_converted{ext}"
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output_files')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)

            shutil.copy(input_path, output_path)

            # Save relative path to output_file
            job.output_file.name = os.path.join('output_files', output_filename)
            job.status = 'completed'
            job.save()

            return Response(ConversionJobSerializer(job).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            job.status = 'failed'
            job.save()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversionJobDetailView(generics.RetrieveAPIView):
    queryset = ConversionJob.objects.all()
    serializer_class = ConversionJobSerializer
    lookup_field = 'id'

class ConversionJobListView(generics.ListAPIView):
    queryset = ConversionJob.objects.all().order_by('-created_at')
    serializer_class = ConversionJobSerializer
