from django.urls import path
from . import views

try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    TokenObtainPairView = None
    TokenRefreshView = None

urlpatterns = [
    path('register/', views.register_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products/', views.get_products, name='get_products'),
    path('products/<int:pk>/', views.get_product, name='get_product'),
    path('categories/', views.get_categories, name='get_categories'),
    path('users/', views.get_users, name='get_users'),
    
    path('cart/', views.get_cart),
    path('cart/add/', views.add_to_cart),
    path('cart/remove/', views.remove_from_cart),
    path('cart/update/', views.update_cart_quantity),
    path('orders/create/', views.create_order),

    path('orders/', views.get_orders, name='get_orders'),
    path('order-items/', views.get_order_items, name='get_order_items'),
    path('payments/', views.get_payments, name='get_payments'),
    path('reviews/', views.get_reviews, name='get_reviews'),
]