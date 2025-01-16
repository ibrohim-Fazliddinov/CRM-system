from django.urls import path

from users.views.auth import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(), name='create-token'),
    path('auth/jwt/refresh', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('auth/jwt/verify', CustomTokenVerifyView.as_view(), name='verify-token'),
]