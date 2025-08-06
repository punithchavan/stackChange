from django.urls import path
from .views import hello_view, db_hello_view

urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('db-hello/', db_hello_view, name='db_hello'),
]
