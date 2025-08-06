from django.http import JsonResponse

def userLogin(request):
    return JsonResponse({"msg": "Login Successful"})

def userRegister(request):
    return JsonResponse({"msg": "User Registered"})

# def user_logout(request):
#     return JsonResponse({"msg": "Logged Out"})

# def tweet_create(request):
#     return JsonResponse({"msg": "Tweet Created"})

# def tweet_delete(request):
#     return JsonResponse({"msg": "Tweet Deleted"})
