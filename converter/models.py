from django.db import models
import os
import uuid

def upload_to(instance, filename):
    return f"uploads/{uuid.uuid4()}_{filename}"

def output_to(instance, filename):
    return f"converted/{uuid.uuid4()}_{filename}"

class ConversionJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    uploaded_file = models.FileField(upload_to=upload_to)
    converted_file = models.FileField(upload_to=output_to, blank=True, null=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    error_message = models.TextField(blank=True, null=True)

    def _str_(self):
        return f"Job {self.id} - {self.status}"