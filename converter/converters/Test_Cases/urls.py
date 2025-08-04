from django.urls import path
from . import views

# This is a comprehensive test case for the URL converter.

urlpatterns = [
    # Root path for an API landing page
    path('', views.api_overview, name='api-overview'),

    # --- Product Routes ---
    # A standard RESTful endpoint for a collection of products
    path('products/', views.ProductListView.as_view(), name='product-list'),
    
    # A detail view using a string slug instead of an integer
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),

    # --- Order Routes ---
    # Using a UUID for the primary key
    path('orders/<uuid:id>/', views.order_detail, name='order-detail'),
    
    # A custom action on a specific order, which is not strictly RESTful
    path('orders/<uuid:id>/mark-shipped/', views.mark_order_shipped, name='order-mark-shipped'),

    # --- Authentication Routes ---
    path('auth/login/', views.AuthLoginView.as_view(), name='auth-login'),
    path('auth/logout', views.auth_logout_view, name='auth-logout'), # Note: No trailing slash
]