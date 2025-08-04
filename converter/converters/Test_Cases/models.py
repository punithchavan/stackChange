from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('ACTIVE', 'Active'),
    ('ARCHIVED', 'Archived'),
]

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_at = models.DateTimeField(auto_now=True)