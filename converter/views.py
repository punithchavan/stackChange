import os
import uuid
import zipfile
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.http import FileResponse
from django.conf import settings
from .models import ConversionJob

UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads')
EXTRACT_DIR = os.path.join(settings.MEDIA_ROOT, 'extracted')
OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, 'output_project')
CONVERTER_DIR = os.path.join(settings.BASE_DIR, 'converter', 'converters')

class UploadAndConvertView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES['file']
        job_id = str(uuid.uuid4())

        # Save uploaded zip file
        zip_path = os.path.join(UPLOAD_DIR, f"{job_id}.zip")
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(zip_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        # Create job record
        job = ConversionJob.objects.create(
            _id=job_id,
            uploaded_file=zip_path,
            status="processing"
        )

        try:
            # Unzip
            extracted_path = os.path.join(EXTRACT_DIR, job_id)
            os.makedirs(extracted_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_path)

            app_path = os.path.join(extracted_path, 'app')

            models_path = os.path.join(app_path, 'models.py')
            views_path = os.path.join(app_path, 'views.py')
            urls_path = os.path.join(app_path, 'urls.py')

            os.makedirs(OUTPUT_DIR, exist_ok=True)

            # Run conversion scripts
            subprocess.run(['python', os.path.join(CONVERTER_DIR, 'model_converter.py'), models_path], check=True)
            subprocess.run(['python', os.path.join(CONVERTER_DIR, 'views_to_json.py'), views_path], check=True)
            # subprocess.run(['python', os.path.join(CONVERTER_DIR, 'urls_converter.py'), urls_path], check=True)
            subprocess.run(['python', os.path.join(CONVERTER_DIR, 'urls_converter.py'), urls_path, views_path], check=True)

            # Zip output
            output_zip_path = os.path.join(settings.MEDIA_ROOT, f"{job_id}_output.zip")
            with zipfile.ZipFile(output_zip_path, 'w') as zipf:
                for root, _, files in os.walk(OUTPUT_DIR):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, OUTPUT_DIR)
                        zipf.write(file_path, arcname)

            job.status = "completed"
            job.converted_file = output_zip_path
            job.save()

            return Response({'job_id': job_id}, status=200)

        except Exception as e:
            job.status = "error"
            job.error_message = str(e)
            job.save()
            return Response({'error': str(e)}, status=500)


class DownloadConvertedZip(APIView):
    def get(self, request, job_id):
        try:
            job = ConversionJob.objects.get(_id=job_id)
            if job.status != "completed" or not job.converted_file:
                return Response({'error': 'Conversion not complete or failed'}, status=400)

            return FileResponse(open(job.converted_file, 'rb'), as_attachment=True, filename='converted_project.zip')
        except ConversionJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)
