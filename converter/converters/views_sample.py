from django.http import JsonResponse

def user_login(request):
    return JsonResponse({"msg": "Login Successful"})

def user_register(request):
    return JsonResponse({"msg": "User Registered"})

def user_logout(request):
    return JsonResponse({"msg": "Logged Out"})

def tweet_create(request):
    return JsonResponse({"msg": "Tweet Created"})

def tweet_delete(request):
    return JsonResponse({"msg": "Tweet Deleted"})