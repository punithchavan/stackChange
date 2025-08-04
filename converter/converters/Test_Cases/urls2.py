from django.urls import path
from . import views

urlpatterns = [
    # Routes for the Post model
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # Routes for the User model
    path('users/', views.UserListView.as_view(), name='user-list'),

    # A function-based view that won't have a model mapping
    path('stats/', views.api_statistics, name='api-stats'),
]