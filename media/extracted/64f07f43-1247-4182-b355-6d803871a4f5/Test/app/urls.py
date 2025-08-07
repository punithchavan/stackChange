from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('posts/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.get_post, name='get_post'),
    path('comments/', views.add_comment, name='add_comment'),
]
