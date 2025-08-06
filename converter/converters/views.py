from django.http import JsonResponse
from .models import HelloMessage

def hello_view(request):
    return JsonResponse({"message": "Hello from Django API!"})

def db_hello_view(request):
    # Create or fetch a message from DB
    obj, created = HelloMessage.objects.get_or_create(message="Hello from DB!")
    return JsonResponse({"message": obj.message, "created": created})
