from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post, Comment
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            User.objects.create_user(username=data['username'], password=data['password'])
            return JsonResponse({'message': 'User registered successfully'})
        except:
            return JsonResponse({'error': 'User already exists'}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return JsonResponse({'message': 'Login successful', 'user_id': user.id, 'token': 'dummy-jwt-token'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=data['user_id'])
            post = Post.objects.create(author=user, content=data['content'])
            return JsonResponse({'message': 'Post created', 'post_id': post.id})
        except:
            return JsonResponse({'error': 'User not found'}, status=400)

def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return JsonResponse({
            'author': post.author.username,
            'content': post.content,
            'created_at': post.created_at
        })
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=data['post_id'])
            user = User.objects.get(id=data['user_id'])
            comment = Comment.objects.create(post=post, user=user, comment_text=data['comment_text'])
            return JsonResponse({'message': 'Comment added', 'comment_id': comment.id})
        except:
            return JsonResponse({'error': 'Invalid post or user'}, status=400)
