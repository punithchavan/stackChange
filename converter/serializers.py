from rest_framework import serializers
from .models import ConversionJob

class ConversionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionJob
        fields = '__all__'
        read_only_fields = ['id', 'status', 'created_at', 'output_file']
